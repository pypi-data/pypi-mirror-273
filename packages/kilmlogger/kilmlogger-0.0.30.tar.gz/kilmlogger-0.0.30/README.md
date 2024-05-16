# KiLM Logger library

[![PyPI version](https://img.shields.io/pypi/v/aiplatform.svg)](https://pypi.org/project/aiplatform/)

The KiLM Logger library provides convenient log to for metrics, monitoring, and structure log.

## Installation

```sh
pip install kilmlogger
```

## Usage

Use the KiLM Logger's Default Configuration

```python
import os

from kilmlogger import KilmLoggerConfiguration


LOG_PATH = os.getenv("LOG_PATH")
APP_NAME = os.getenv("APP_NAME")

# Logging's level that will be sent to scribe
SCRIBE_LOGGING_LEVEL

# Logging's level that will show only console
CONSOLE_LOGGING_LEVEL

# Accepted levels that will actually sent metrics to
ACCEPTED_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


# Setup your file to store logging records
def get_logging_file_path() -> str:
    log_file_name: str = f"{APP_NAME}.log"
    log_path: str = os.path.join(LOG_PATH, APP_NAME)
    if not os.path.exists(log_path):
        os.makedirs(log_path)
    return os.path.join(log_path, log_file_name)


# Setup logging level, file, scribe level,...
def use_default_logging():
    kilm_logger_config: KilmLoggerConfiguration = KilmLoggerConfiguration(
        logging_filename=get_logging_file_path(),
        logging_level=SCRIBE_LOGGING_LEVEL,
        console_logging_level=CONSOLE_LOGGING_LEVEL,
        accepted_levels=ACCEPTED_LEVELS,
        # use_async=True,
    )
    kilm_logger_config.use_default_configuration()

```

Send metrics to Scribe
```python
import functools
import kilmlogger as logging

from enum import Enum
from typing import Awaitable
from datetime import datetime as dt


logger = logging.get_logger("kilmlogger")

# Scribe category
SCRIBE_LOGGING_CATEGORY


class MetricCommandEnum(int, Enum):
    METRIC_COMMAND = 1111
    ...



class MetricSubCommandEnum(int, Enum):
    METRIC_SUB_COMMAND = 0
    ...


class MetricResultEnum(int, Enum):
    METRIC_SUCCESS = 0
    METRIC_FAILURE = 1
    ...


def async_send_metric(func: Awaitable):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        command: MetricCommandEnum = kwargs.get("command")
        category: str = kwargs.get("category", SCRIBE_LOGGING_CATEGORY)
        sub_command: MetricSubCommandEnum = kwargs.get("sub_command")
        try:
            start_time: float = int(dt.now().timestamp() * 1000)
            result: MetricResultEnum = MetricResultEnum.SUCCESS
            return await func(*args, **kwargs)
        except Exception as e:
            result = MetricResultEnum.FAILURE
            logger.error(
                f"Error when executing function {func.__name__}",
            )
            raise e
        finally:
            logger.debug(
                f"Finish executing {command.name}",
                start_time=start_time,
                category=category,
                command=command,
                sub_command=sub_command,
                result=result,
                metric_only=True,
            )

    return wrapper


def async_metric_sender(
    command: MetricCommandEnum,
    category: str = SCRIBE_LOGGING_CATEGORY,
    sub_command: MetricSubCommandEnum = MetricSubCommandEnum.DEFAULT,
):
    def decorator(func: Awaitable):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                start_time: float = int(dt.utcnow().timestamp() * 1000)
                result: MetricResultEnum = MetricResultEnum.SUCCESS
                return await func(*args, **kwargs)
            except BaseApplicationException as e:
                raise e
            except Exception as e:
                result = MetricResultEnum.FAILURE
                logger.error(
                    f"Error when executing function {func.__name__}",
                )
                raise e
            finally:
                logger.debug(
                    f"Finish executing {command.name}",
                    start_time=start_time,
                    category=category,
                    command=command,
                    sub_command=sub_command,
                    result=result,
                    metric_only=True,
                )

        return wrapper

    return decorator


def sync_metric_sender(
    command: MetricCommandEnum,
    category: str = SCRIBE_LOGGING_CATEGORY,
    sub_command: MetricSubCommandEnum = MetricSubCommandEnum.DEFAULT,
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                start_time: float = int(dt.utcnow().timestamp() * 1000)
                result: MetricResultEnum = MetricResultEnum.SUCCESS
                return func(*args, **kwargs)
            except BaseApplicationException as e:
                raise e
            except Exception as e:
                result = MetricResultEnum.FAILURE
                logger.error(
                    f"Error when executing function {func.__name__}",
                    correlation_id="",
                )
                raise e
            finally:
                logger.debug(
                    f"Finish executing {command.name}",
                    start_time=start_time,
                    category=category,
                    command=command,
                    sub_command=sub_command,
                    result=result,
                    metric_only=True,
                    correlation_id="",
                )

        return wrapper

    return decorator

```

Examples:

```python
import asyncio
import kilmlogger as logging

from httpx import AsyncClient, Response, Timeout, TimeoutException

from app.utils.metric import async_send_metric


logger = logging.get_logger("kilmlogger")


@async_send_metric
async def make_request(
    *,
    client: AsyncClient,
    url: str,
    method: str = "GET",
    data: dict | None = None,
    json: dict | None = None,
    params: dict | None = None,
    headers: dict | None = None,
    timeout: float | None = 5.0,
    connect_timeout: float | None = 5.0,
    **kwargs,
) -> Response:
    try:
        return await client.request(
            method=method,
            url=url,
            data=data,
            json=json,
            params=params,
            headers=headers,
            timeout=Timeout(timeout=timeout, connect=connect_timeout),
        )
    except TimeoutException as e:
        logger.error(f"Timeout when request {url} with error: {type(e)}")
        raise e
    except Exception as e:
        logger.error(f"Error when request {url} with error: {e}")
        raise e


asyncio.run(
    make_request(
        ...
        command=MetricCommandEnum.RETRIEVE_DOC,
    )
)
```

This example use decorator as a middle layer that will wrap the method make_request() to sent the metrics to the Scribe Log

We also need some environments config:
```bash
ENVIRONMENT=staging
SCRIBE_HOST=kiki-scribelog-forward-grpc-headless-svc.kiki-infras
SCRIBE_PORT=9080
# DP Cate Name
DP_CATEGORY=KILM_EVENT_LOG
# To push log to Central Log (Data Platform Cate)
# The order needs to be the same as the DP Cate order
DP_LOG=app_name,app_mode,event_category,correlation_id,message,metrics,extra_data
```

or ArgoCD env:
```bash
...
  - name: ENVIRONMENT
    value: staging
  - name: SCRIBE_HOST
    value: "kiki-scribelog-forward-grpc-headless-svc.kiki-infras"
  - name: SCRIBE_PORT
    value: "9080"
  - name: DP_CATEGORY
    value: "KILM_EVENT_LOG"
  - name: DP_LOG
    value: "app_name,app_mode,event_category,correlation_id,message,metrics,extra_data"
```



## Requirements

Python 3.12 or higher.
