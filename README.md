# CaiaSoft/Aleph Integration

Middleware for connecting the Aleph ILS to CaiaSoft.

## Introduction

This application acts as middleware, providing a conduit for the Aleph ILS
to CaiaSoft for the following:

* Place Aleph hold requests into the CaiaSoft circulation jobs queue
* Update the CaiaSoft Storage with information about new/updated items

## Architecture Decision Records (ADRs)

This project uses Architecture Decision Records to record significant
architecture/project decisions. See [docs/adrs](docs/adr/).

## Development Setup

### Prerequsites

The following instructions assume that "pyenv" and "pyenv-virtualenv" are
installed to enable the setup of an isolated Python environment.

See the following for setup instructions:

* https://github.com/pyenv/pyenv
* https://github.com/pyenv/pyenv-virtualenv

Once "pyenv" and "pyenv-virtualenv" have been installed, install Python 3.8.2:

```
> pyenv install 3.8.2
```

### Installation for development 

1) Clone the "caia" Git repository:

```
> git clone git@github.com:umd-lib/caia.git
```

2) Switch to the "caia" directory:

```
> cd caia
```

3) Set up the virtual environment:

```
> pyenv virtualenv 3.8.2 caia
> pyenv shell caia
```

4) Run "pip install", including the "dev" and "test" dependencies:

```
> pip install -e .[dev,test]
```

### Running the tests

The tests can be run via "pytest" (included in "test" dependencies) using the
following command:

```
> pytest
```

### Code Style

Application code style should generally conform to the guidelines in
[PEP 8](https://www.python.org/dev/peps/pep-0008/). The "pycodestyle" tool
to check compliance with the guidelines can be run using:

```
> pycodestyle .
```

## Command-line Options

Caia is a command-line application. To see the list of available commands:

```
> caia --help
```

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations
(Apache 2.0).
