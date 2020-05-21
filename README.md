# CaiaSoft/Aleph Integration

Middleware for connecting the Aleph ILS to CaiaSoft.

## Introduction

This application acts as middleware, providing a conduit for the Aleph ILS
to CaiaSoft for the following:

* Place Aleph hold requests into the CaiaSoft circulation jobs queue
* Update the CaiaSoft Storage with information about new/updated items

## Command-line Options

Caia is a command-line application. To see the list of available commands:

```
> caia --help
```

A description of individual commands can be found using:

```
> caia <COMMAND> --help
```

where \<COMMAND> is the command. For example:

```
> caia circrequests --help
```
## Environment Configuration

The application requires a ".env" file in the root directory containing
environment variables that configure the application. A sample "env_example"
file has been provided to assist with this process. Simply copy the
"env_example" file to ".env" and fill out the parameters as appropriate.

The configured .env file should not be checked into the Git repository, as it
contains credential information.

## Commands

### circrequests

Example usage:

```
> caia circrequests
```

This command queries Aleph for a list of hold requests, sending new hold
requests to CaiaSoft, using the CaiaSoft API "/circrequests" endpoint.

## Development Setup

See [docs/DevelopmentSetup.md](docs/DevelopmentSetup.md).

## Docker Image

This application provides a "Dockerfile" for generating a Docker image for use
in production. The Dockerfile provides a sample build command.

In order to generate "clean" Docker images, the Docker images should be built
from a fresh clone of the GitHub repository.

## Docker.ci and Jenkinsfile

The "Dockerfile.ci" file is used to encapsulate the environment needed by the
continuous integration (ci) server for building and testing the application.

The "Jenkinsfile" provides the Jenkins pipeline steps for building and testing
the application.

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations
(Apache 2.0).
