import logging
import logging.config
from watchtower import CloudWatchLogHandler
from zeppos_logging.app_logger_json_config import AppLoggerJsonConfig
from zeppos_logging.app_logger_json_conifg_name import AppLoggerJsonConfigName
from zeppos_logging.app_logger_filter import AppLoggerFilter

class AppLogger:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.addHandler(logging.NullHandler())
    config_dict = None

    @staticmethod
    def configure_and_get_logger(logger_name=None, config_section_name=AppLoggerJsonConfigName.default_format_1(),
                                 watchtower_log_group=None, watchtower_stream_name=None,
                                 logging_level=logging.INFO):
        AppLogger.logger.debug(f"Configuring and getting logger: {logger_name}")
        AppLogger._configure_logger(config_section_name, watchtower_log_group, watchtower_stream_name)
        AppLogger.get_logger(logger_name)
        AppLogger.set_level(logging_level)
        return AppLogger.logger

    @staticmethod
    def _configure_logger(config_section_name=AppLoggerJsonConfigName.default_format_1(),
                          watchtower_log_group=None, watchtower_stream_name=None):
        AppLogger._set_config_dict_for_config_section(config_section_name)
        AppLogger._overwrite_logging_config_section_values(watchtower_log_group, watchtower_stream_name)
        logging.config.dictConfig(AppLogger.config_dict)

    @staticmethod
    def _set_config_dict_for_config_section(config_section_name):
        AppLogger.logger.debug(f"Getting Config Section for [{config_section_name}]")

        try:
            if config_section_name:
                if config_section_name.lower().strip() == AppLoggerJsonConfigName.default_format_1():
                    AppLogger._set_config_dict(AppLoggerJsonConfig.default_format_1())
                    return  # Circuit Breaker
                if config_section_name.lower().strip() == AppLoggerJsonConfigName.default_with_watchtower_format_1():
                    AppLogger._set_config_dict(AppLoggerJsonConfig.default_with_watchtower_format_1())
                    return  # Circuit Breaker
                if config_section_name.lower().strip() == AppLoggerJsonConfigName.django_with_watchtower_format_1():
                    AppLogger._set_config_dict(AppLoggerJsonConfig.django_with_watchtower_format_1())
                    return  # Circuit Breaker
        except:
            pass

        AppLogger.logger.debug('Default fall-back logging enabled.')
        AppLogger._set_config_dict(AppLoggerJsonConfig.default_format_1())
        AppLogger.logger.config_section_name = AppLoggerJsonConfig.default_format_1()

    @staticmethod
    def _set_config_dict(config_dict):
        AppLogger.logger.debug(f"Set logging configuration to: {config_dict}")
        AppLogger.config_dict = config_dict
        return config_dict

    @staticmethod
    def _overwrite_logging_config_section_values(watchtower_log_group=None, watchtower_stream_name=None):
        AppLogger._set_log_group(watchtower_log_group)
        AppLogger._set_stream_name(watchtower_stream_name)

    @staticmethod
    def get_logger(logger_name):
        AppLogger._set_logger(logger_name)
        return AppLogger.logger

    @staticmethod
    def _set_logger(logger_name):
        if not AppLogger.logger or AppLogger.logger.name != logger_name:
            AppLogger.logger = logging.getLogger(logger_name)
            AppLogger._add_handler()
            AppLogger._add_filter()
            AppLogger.logger.debug(f"set the logger to: {logger_name}")

    @staticmethod
    def get_log_group():
        if AppLogger._log_group_exists():
            return AppLogger.config_dict['handlers']['watchtower']['log_group']
        return None

    @staticmethod
    def _set_log_group(watchtower_log_group):
        if watchtower_log_group and AppLogger.logger and AppLogger._log_group_exists():
            AppLogger.config_dict['handlers']['watchtower']['log_group'] = watchtower_log_group

    @staticmethod
    def _log_group_exists():
        if AppLogger.config_dict:
            if isinstance(AppLogger.config_dict, dict):
                if 'handlers' in AppLogger.config_dict:
                    if 'watchtower' in AppLogger.config_dict['handlers']:
                        if 'log_group' in AppLogger.config_dict['handlers']['watchtower']:
                            return True
        return False

    @staticmethod
    def get_stream_name():
        if AppLogger._stream_name_exists():
            return AppLogger.config_dict['handlers']['watchtower']['stream_name']
        return None

    @staticmethod
    def _set_stream_name(watchtower_stream_name):
        if watchtower_stream_name and AppLogger._stream_name_exists():
            AppLogger.config_dict['handlers']['watchtower']['stream_name'] = watchtower_stream_name

    @staticmethod
    def _stream_name_exists():
        if AppLogger.config_dict:
            if isinstance(AppLogger.config_dict, dict):
                if 'handlers' in AppLogger.config_dict:
                    if 'watchtower' in AppLogger.config_dict['handlers']:
                        if 'stream_name' in AppLogger.config_dict['handlers']['watchtower']:
                            return True
        return False

    @staticmethod
    def _add_handler():
        AppLogger.logger.debug("Add Handler")
        AppLogger.logger.addHandler(CloudWatchLogHandler())

    @staticmethod
    def _add_filter():
        AppLogger.logger.debug("Add Filter")
        AppLogger.logger.addFilter(AppLoggerFilter())

    @staticmethod
    def set_level(logging_level):
        AppLogger.logger.setLevel(logging_level)

    @staticmethod
    def set_debug_level():
        AppLogger.set_level(logging.DEBUG)

    @staticmethod
    def set_info_level():
        AppLogger.set_level(logging.INFO)

    @staticmethod
    def set_error_level():
        AppLogger.set_level(logging.ERROR)

    @staticmethod
    def set_warning_level():
        AppLogger.set_level(logging.WARNING)

    @staticmethod
    def set_critical_level():
        AppLogger.set_level(logging.CRITICAL)