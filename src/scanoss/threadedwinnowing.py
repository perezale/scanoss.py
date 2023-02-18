"""
 SPDX-License-Identifier: MIT

   Copyright (c) 2023, SCANOSS

   Permission is hereby granted, free of charge, to any person obtaining a copy
   of this software and associated documentation files (the "Software"), to deal
   in the Software without restriction, including without limitation the rights
   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
   copies of the Software, and to permit persons to whom the Software is
   furnished to do so, subject to the following conditions:

   The above copyright notice and this permission notice shall be included in
   all copies or substantial portions of the Software.

   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
   THE SOFTWARE.
"""
import os
import sys
import threading
import queue
import time

from typing import Dict, List
from dataclasses import dataclass
from progress.spinner import Spinner
from progress.bar import Bar

from .scanossbase import ScanossBase
from .winnowing import Winnowing

WFP_FILE_START = "file="
MAX_ALLOWED_THREADS = int(os.environ.get("SCANOSS_MAX_ALLOWED_THREADS")) if os.environ.get(
    "SCANOSS_MAX_ALLOWED_THREADS") else 30


@dataclass
class ThreadedWinnowing(ScanossBase):
    """
    Threaded class for running Winnowing in parallel (from a queue)
    File winnowing requests are loaded into the input queue.
    Multiple threads pull messages off this queue, process the request and put the results into an output queue
    """
    inputs: queue.Queue = queue.Queue()
    output: queue.Queue = queue.Queue()
    spinner: Spinner = None
    bar: Bar = None

    def __init__(self, debug: bool = False, trace: bool = False, quiet: bool = False, nb_threads: int = 5,
                 winnowing: Winnowing = None, scan_dir: str = None) -> None:
        """
        Initialise the ThreadedWinnowing class
        :param debug: enable debug (default False)
        :param trace: enable trace (default False)
        :param quiet: enable quiet mode (default False)
        :param nb_threads: Number of thread to run (default 5)
        """
        super().__init__(debug, trace, quiet)
        self.nb_threads = nb_threads
        self.winnowing = winnowing
        self.scan_dir = scan_dir
        self.scan_dir_len = len(scan_dir) if scan_dir.endswith(os.path.sep) else len(scan_dir) + 1
        self._isatty = sys.stderr.isatty()
        self._bar_count = 0
        self._errors = False
        self._lock = threading.Lock()
        self._stop_event = threading.Event()  # Control when winnowing threads should terminate
        self._stop_winnowing = threading.Event()  # Control if the parent process should abort winnowing
        self._threads = []
        if nb_threads > MAX_ALLOWED_THREADS:
            self.print_msg(f'Warning: Requested threads too large: {nb_threads}. Reducing to {MAX_ALLOWED_THREADS}')
            self.nb_threads = MAX_ALLOWED_THREADS

    def create_bar(self, file_count: int):
        if not self.quiet and self._isatty and not self.bar:
            self.bar = Bar('Winnowing', max=file_count)
            self.bar.next(self._bar_count)

    def complete_bar(self):
        if self.bar:
            self.bar.finish()

    def set_bar(self, bar: Bar) -> None:
        """
        Set the Progress Bar to display progress while winnowing
        :param bar: Progress Bar object
        """
        self.bar = bar

    def update_bar(self, amount: int = 0, create: bool = False, file_count: int = 0) -> None:
        """
        Update the Progress Bar progress
        :param amount: amount of progress to update
        :param create: create the bar if requested
        :param file_count: file count
        """
        try:
            self._lock.acquire()
            try:
                if create and not self.bar:
                    self.create_bar(file_count)
                elif self.bar:
                    self.bar.next(amount)
                self._bar_count += amount
            finally:
                self._lock.release()
        except Exception as e:
            self.print_debug(f'Warning: Update status bar lock failed: {e}. Ignoring.')

    def create_spinner(self):
        if not self.quiet and self._isatty and not self.spinner:
            self.spinner = Spinner('Fingerprinting ')

    def complete_spinner(self):
        if self.spinner:
            self.spinner.finish()

    def set_spinner(self, spinner: Spinner) -> None:
        """
        Set the Progress Bar to display progress while winnowing
        :param spinner: Spinner object
        """
        self.spinner = spinner

    def update_spinner(self, create: bool = False) -> None:
        """
        Update the Progress Spinner
        :param create: create the bar if requested
        """
        try:
            # self._lock.acquire()
            # try:
            if create and not self.spinner:
                self.create_spinner()
            elif self.spinner:
                self.spinner.next()
            # finally:
            # self._lock.release()
        except Exception as e:
            self.print_debug(f'Warning: Update status bar lock failed: {e}. Ignoring.')

    def queue_add(self, file: str) -> None:
        """
        Add requests to the queue
        :param file: file to add to the queue
        """
        if file is None or file == '':
            self.print_stderr(f'Warning: empty filename. Skipping from winnowing...')
        else:
            self.inputs.put(file)

    def get_queue_size(self) -> int:
        return self.inputs.qsize()

    def stop_winnowing(self) -> bool:
        """
        Check if we should keep winnowing or not
        """
        return self._stop_winnowing.is_set()

    @property
    def responses(self) -> List[str]:
        """
        Get all responses back from the completed threads
        :return: List of string objects
        """
        return list(self.output.queue)

    def run(self, wait: bool = True) -> bool:
        """
        Initiate the threads and process all pending requests
        :return: True if successful, False if error encountered
        """
        qsize = self.inputs.qsize()
        if qsize < self.nb_threads:
            self.print_debug(f'Input queue ({qsize}) smaller than requested threads: {self.nb_threads}. '
                             f'Reducing to queue size.')
            self.nb_threads = qsize
        else:
            self.print_debug(f'Starting {self.nb_threads} threads to process {qsize} requests...')
        try:
            for i in range(0, self.nb_threads):
                t = threading.Thread(target=self.worker_post, daemon=True)
                self._threads.append(t)
                t.start()
        except Exception as e:
            self.print_stderr(f'ERROR: Problem running threaded winnowing: {e}')
            self._errors = True
        if wait:  # Wait for all inputs to complete
            self.complete()
        return False if self._errors else True

    def complete(self) -> bool:
        """
        Wait for input queue to complete processing and complete the worker threads
        """
        self.inputs.join()
        self._stop_event.set()  # Tell the worker threads to stop
        try:
            for t in self._threads:  # Complete the threads
                t.join(timeout=5)
        except Exception as e:
            self.print_stderr(f'WARNING: Issue encountered terminating winnowing worker threads: {e}')
            self._errors = True
        self.complete_bar()
        return False if self._errors else True

    def worker_post(self) -> None:
        """
        Take each request and process it
        :return: None
        """
        current_thread = threading.get_ident()
        self.print_trace(f'Starting worker {current_thread}...')
        while not self._stop_event.is_set():
            file = None
            if not self.inputs.empty():  # Only try to get a message if there is one on the queue
                try:
                    file = self.inputs.get(timeout=5)
                    self.print_trace(f'Processing input request ({current_thread})...')
                    if file is None or file == '':
                        self.print_stderr(f'Warning: Empty File in request input: {file}')
                    wfps = self.winnowing.wfp_for_file(file, self.strip_path(self.scan_dir, self.scan_dir_len, file))
                    if wfps:
                        self.output.put(wfps)  # Store the output response to later collection
                        self.update_bar(1)
                    self.inputs.task_done()
                    self.print_trace(f'Request complete ({current_thread}).')
                except queue.Empty:
                    self.print_stderr(f'No message available to process ({current_thread}). Checking again...')
                except Exception as e:
                    self.print_stderr(f'ERROR: Problem encountered running winnowing: {e}. Aborting current thread.')
                    self._errors = True
                    if file:
                        self.inputs.task_done()  # If there was a WFP being processed, remove it from the queue
                    self._stop_winnowing.set()  # Tell the parent process to abort winnowing
            else:
                time.sleep(1)  # Sleep while waiting for the queue depth to build up
        self.print_trace(f'Thread complete ({current_thread}).')

#
# End of ThreadedWinnowing Class
#
