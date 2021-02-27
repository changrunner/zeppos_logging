# zeppos_logging

## Purpose
This library makes the logging using python common logging library easy. 
All you have to do is follow some configuration instructions and you will be up and running.

## Setup Instructions

### windows
```python build_venv.py```

### linux
```python3 build_venv.py```

### AWS Logging
- [Install AWS CLI 2](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
- Create AWS IAM user with token and access level of CloudWatch
- Configure AWS


## Usage

- Default root logger
```
from zeppos_logging.app_logger import AppLogger

def main():
    AppLogger.logger.debug("test1")


if __name__ == '__main__':
    AppLogger.configure_and_get_logger()
    main()
```

Sample output: ```root       | DEBUG    | test1```

- Set a specific Logger
```
from zeppos_logging.app_logger import AppLogger
from zeppos_logging.app_logger_json_conifg_name import AppLoggerJsonConfigName

def main():
    AppLogger.logger.debug("test1")


if __name__ == '__main__':
    AppLogger.configure_and_get_logger('try_me', AppLoggerJsonConfigName.default_format_1())
    main()
```

Sample output: ```try_me     | DEBUG    | test1```

- Set an Aws Cloudwatch Logger

```
from zeppos_logging.app_logger import AppLogger
from zeppos_logging.app_logger_json_conifg_name import AppLoggerJsonConfigName

def main():
    AppLogger.logger.info("test1")


if __name__ == '__main__':
    AppLogger.configure_and_get_logger(
        'try_me',
        AppLoggerJsonConfigName.default_with_watchtower_format_1(),
        watchtower_log_group="some_cloud_watch_log_group_name",
        watchtower_stream_name="some_cloud_watch_log_stream_name"
    )
    main()
```

Sample output: ```[2020-11-16T21:39:05.698] | 10.10.10.10 | N12345 | INFO     | try_me     | main       |    5 | test1```

#### Valid AppLoggerJsonConfigName
- AppLoggerJsonConfigName.default_format_1()
- AppLoggerJsonConfigName.default_with_watchtower_format_1()
- AppLoggerJsonConfigName.django_with_watchtower_format_1()
