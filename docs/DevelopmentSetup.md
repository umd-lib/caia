# Development Setup

## Introduction

This page describes how to set up a development environment, and other
information useful for developers to be aware of.

## Architecture Decision Records (ADRs)

This project uses Architecture Decision Records to record significant
architecture/project decisions. See [docs/adr](docs/adr/).

## Prerequisites

The following instructions assume that "pyenv" and "pyenv-virtualenv" are
installed to enable the setup of an isolated Python environment.

See the following for setup instructions:

* https://github.com/pyenv/pyenv
* https://github.com/pyenv/pyenv-virtualenv

Once "pyenv" and "pyenv-virtualenv" have been installed, install Python 3.8.2:

```
> pyenv install 3.8.2
```

## Installation for development 

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

## Running the tests

Some tests use the Mountebank [http://www.mbtest.org/](http://www.mbtest.org/)
server virtualization tool to simulate server API calls and responses. This
is a JavaScript application that can be installed as follows:

1) Using Brew, install "node":

```
> brew install node
```

2) NPM (which comes with Node) can then be used to install Mountebank in the
project root directory:

    a) Switch to the project root directory.
    
    b) Run the following command:
    
    ```
    > npm install mountebank
    ```
4) The tests now can be run via "pytest" (included in "test" dependencies) using
the following command:

```
> pytest
```

## Code Style

Application code style should generally conform to the guidelines in
[PEP 8](https://www.python.org/dev/peps/pep-0008/). The "pycodestyle" tool
to check compliance with the guidelines can be run using:

```
> pycodestyle .
```
