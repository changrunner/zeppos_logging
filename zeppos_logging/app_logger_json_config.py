class AppLoggerJsonConfig:

    @staticmethod
    def default_format_1():
        return {
            "version": 1,
            "disable_existing_loggers": "false",
            "formatters": {
                "default-single-line": {
                    "style": "{",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "{name:<10s} | {levelname:8s} | {message:s}"
                }
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "default-single-line",
                    "stream": "ext://sys.stdout"
                }
            },
            "loggers": {},
            "root": {
                "handlers": ["console"],
                "level": "DEBUG"
            }
        }

    @staticmethod
    def default_with_watchtower_format_1():
        return {
                "version": 1,
                "disable_existing_loggers": "false",
                "formatters": {
                    "default-single-line": {
                        "style": "{",
                        "datefmt": "%Y-%m-%dT%H:%M:%S",
                        "format": "[{asctime:s}.{msecs:3.0f}] | {client_ip} | {host_name} | {levelname:8s} | {name:<10s} | {funcName:<10s} | {lineno:4d} | {message:s}"
                    }
                },
                "handlers": {
                    "console": {
                        "level": "INFO",
                        "class": "logging.StreamHandler",
                        "formatter": "default-single-line",
                        "stream": "ext://sys.stdout"
                    },
                    "watchtower": {
                        "level": "INFO",
                        "class": "watchtower.CloudWatchLogHandler",
                        "formatter": "default-single-line",
                        "log_group": "default_with_watchtower_format_1",
                        "stream_name": "default",
                        "send_interval": 1,
                        "create_log_group": "True"
                    }
                },
                "loggers": {},
                "root": {
                    "handlers": ["console", "watchtower"],
                    "level": "INFO"
                }
            }

    @staticmethod
    def django_with_watchtower_format_1():
        return {
                "version": 1,
                "disable_existing_loggers": "false",
                "formatters": {
                    "json": {
                        "class": "logging.Formatter",
                        "style": "{",
                        "datefmt": "%Y-%m-%dT%H:%M:%S",
                        "format": "[{asctime:s}.{msecs:3.0f}] | {client_ip} | {host_name} | {levelname:8s} | {name:<10s} | {funcName:<10s} | {lineno:4d} | {message:s}"
                    },
                    "single-line": {
                         "style": "{",
                         "datefmt": "%Y-%m-%dT%H:%M:%S",
                         "format": "[{asctime:s}.{msecs:3.0f}] | {client_ip} | {host_name} |  {levelname:8s} | {name:<10s} | {funcName:<10s} | {lineno:4d} | {message:s}"
                    }
                },
                "filters": {
                   "require_debug_true": {
                       "()": "django.utils.log.RequireDebugTrue"
                   },
                   "app_logger_filter": {
                       "()": "audit_trail.app_logger_filter.AppLoggerFilter"
                   }
                },
                "handlers": {
                    "console": {
                        "level": "INFO",
                        "filters": ["require_debug_true", "app_logger_filter"],
                        "class": "logging.StreamHandler",
                        "formatter": "single-line"
                    },
                    "watchtower": {
                        "level": "INFO",
                        "filters": ["app_logger_filter"],
                        "class": "watchtower.CloudWatchLogHandler",
                        "formatter": "json",
                        "log_group": "django_with_aws_format_1",
                        "stream_name" : "local",
                        "send_interval" : 1,
                        "create_log_group": "True"
                    }
                },
                "root": {
                    "handlers": ["console", "watchtower"],
                    "level": "INFO"
                }
            }
