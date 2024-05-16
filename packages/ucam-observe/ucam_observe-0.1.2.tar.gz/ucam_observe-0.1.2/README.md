# Observability Python Library

Currently a POC in the Wilson team. Python library to aid consistent configuration of logging,
metrics (future) and tracing (further in future). Packaging and wiring existing open tooling
to work effortlessly on UIS DevOps managed cloud infrastructure.

## Install this module

```bash
pip install ucam-observe
```

## Usage

### Logging

NOTE: Currently only vanilla python is supported, not Django.

Usage is similar to using `structlog` directly with the function `get_structlog_logger` returning
an object compatible with that returned by `structlog`'s `get_logger` function. No further
configuration is needed.

```bash
logger = get_structlog_logger(__name__)

logger.info("some_event")

logger.info("some_other_event", foo=bar)
```

### Metrics and Tracing

`raise NotImplemented`


## Include Gunicorn structlog configuration in your project

### Adapt Gunicorn configuration
In the root of your project, create/amend a gunicorn.conf.py. Add the following code to the file.

```py
from ucam_observe.gunicorn_conf import configure_logging
configure_logging()
```

### Environment Configuration

#### Log Level

Set the `LOG_LEVEL` environment variable to control the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL). This setting adjusts the verbosity of the log outputs:

```bash
export LOG_LEVEL=DEBUG
```

#### Console Logging

Set the `CONSOLE_LOGGING` environment variable to control whether logs should be output in a console-friendly format. Set it to `True` to use console-friendly formatting:

```bash
export CONSOLE_LOGGING=True
```

### Example Docker Compose Configuration

When using Docker Compose for local development, you can set the environment variables in your `docker-compose.yml` file:

```yaml
version: '3.8'
services:
  your_service:
    build: .
    environment:
      - LOG_LEVEL=DEBUG
      - CONSOLE_LOGGING=True
```

## Developer quickstart

Firstly, [install docker-compose](https://docs.docker.com/compose/install/).
Install poethepoet
```bash
pip install poethepoet
```
Then, most tasks can be performed via the poe command.

E.g.

```bash
# Build the containers
$ poe build
```

Run the follow command to see available commands:
```bash
$ poe
```

### Optional extras

NOTE: The Django optional extra is currently empty with a ticket open to add the required
functionality

This library includes optional extras, e.g. `ucam-observe[django]`. Some
tests will require these optional dependencies to pass. The following command
will install all optional dependencies.

```bash
$ poe install-all-extras
```

Some tests require the absence of dependencies and these are excluded by
default. See the tox.ini file for how these tests are run.
