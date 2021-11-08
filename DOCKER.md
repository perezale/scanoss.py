# SCANOSS Docker Repository
The SCANOSS python package provides a simple easy to consume library for interacting with SCANOSS APIs/Engine.

This docker repo provides this package in an easy to install/run image.

## Installation
To install (from [Docker Hub](https://hub.docker.com/search?type=image)), please run:
```bash
docker pull scanoss/scanoss-py:latest
```

## Usage
The Python CLI is exposed from the image and can be run using:
```bash
docker run -it scanoss/scanoss-py
```
To scan the current folder run:
```bash
docker run -it -v "$(pwd)":"/scanoss" scanoss/scanoss-py scan .
```
To output the results to a file run:
```bash
docker run -it -v "$(pwd)":"/scanoss" scanoss/scanoss-py scan -o results.json .
```
To redirect output to a file run:
```bash
docker run -i -v "$(pwd)":"/scanoss" scanoss/scanoss-py scan . > output.json
```

## Source code
The source for this repo can be found [here](https://github.com/scanoss/scanoss.py).

## Changelog
Details of each release can be found [here](https://github.com/scanoss/scanoss.py/blob/main/CHANGELOG.md).

## Docker image tags
Image tag/version details can be found [here](????).
