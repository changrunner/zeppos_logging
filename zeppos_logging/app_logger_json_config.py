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
                "handlers": ["console"]
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
                        "level": "DEBUG",
                        "class": "logging.StreamHandler",
                        "formatter": "default-single-line",
                        "stream": "ext://sys.stdout"
                    },
                    "watchtower": {
                        "level": "DEBUG",
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
                        "level": "DEBUG",
                        "filters": ["require_debug_true", "app_logger_filter"],
                        "class": "logging.StreamHandler",
                        "formatter": "single-line"
                    },
                    "watchtower": {
                        "level": "DEBUG",
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
                }
            }

    @staticmethod
    def default_with_google_cloud_format_1():
        return {
            "version": 1,
            "disable_existing_loggers": "false",
            "formatters": {
                "single-line": {
                    "style": "{",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "[{asctime:s}.{msecs:3.0f}] | {client_ip} | {host_name} |  {levelname:8s} | {name:<10s} | {funcName:<10s} | {lineno:4d} | {message:s} | {data:s}"
                },
                "google-single-line": {
                    "style": "{",
                    "datefmt": "%Y-%m-%dT%H:%M:%S",
                    "format": "{{\"message\":\"{message:s}\",\"data\":\"{data:s}\",\"client_ip\":\"{client_ip:s}\",\"host_name\":\"{host_name:s}\" }}"
                }
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "single-line",
                    "stream": "ext://sys.stdout"
                },
                "google_cloud": {
                    "level": "DEBUG",
                    "class": "zeppos_log_handler_google_cloud.GoogleCloudLogHandler",
                    "formatter": "google-single-line",
                    "project": "default",
                    "log_name": "unknown"
                }
            },
            "loggers": {},
            "root": {
                "handlers": ["console", "google_cloud"],
            }
        }