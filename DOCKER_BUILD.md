# SCANOSS Python Docker Repo
The SCANOSS python package provides a simple, easy to consume library for interacting with SCANOSS APIs/Engine.

## Usage
The image can be run from the command line, or from within a pipeline.

For more details, please look in [DOCKER.md](DOCKER.md).

## Development
Before starting with development of this project, please read our [CONTRIBUTING](CONTRIBUTING.md) and [CODE OF CONDUCT](CODE_OF_CONDUCT.md).

### Requirements
Docker client needs to be installed locally.

A login to GitHub Packages is also needed, should you wish to publish the image.
Details of generating a personal access token can be found [here](https://docs.github.com/en/packages/learn-github-packages/about-permissions-for-github-packages).

### Repo Development
More details on Docker build/deployment can be found [here](https://docs.docker.com/get-started/).

### Build
To build a local image from the [Dockerfile](Dockerfile) please use:
```bash
make docker_build
```
To test this image please run:
```bash
docker run -it scanoss-py 
```
For more details execution options, please look in [DOCKER.md](DOCKER.md).

#### Versioning
The version of the package is defined in the [scanoss init](src/scanoss/__init__.py) file. Please update this version before packaging/releasing an update.

To tag the latest build, please run:
```bash
make docker_tag
```

#### Deployment
In order to deploy the image, a user needs to be registered on Docker Hub and have access to the correct repo.

Once the credentials have been stored in $HOME/.docker, the following command can be run:
```bash
make docker_push
```
This will deploy the image to [Docker Hub](????).

The image will then be available to install using:
```bash
docker pull scanoss/scanoss-py:latest
```

## Bugs/Features
To request features or alert about bugs, please do so [here](https://github.com/scanoss/scanoss.py/issues).

## Changelog
Details of major changes to the library can be found in [CHANGELOG.md](CHANGELOG.md).
