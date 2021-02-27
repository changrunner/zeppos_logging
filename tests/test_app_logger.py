import unittest
from zeppos_logging.app_logger import AppLogger
from zeppos_logging.app_logger_json_conifg_name import AppLoggerJsonConfigName
from testfixtures import LogCapture
import logging
import logging.config

class test_the_app_logger_methods(unittest.TestCase):
    def test_simple_logging_method(self):
        AppLogger.configure_and_get_logger(
            logger_name='test_simple')

        with LogCapture() as lc:
            AppLogger.logger.info("test_me_simple")
            lc.check(
                ('test_simple', 'INFO', 'test_me_simple'),
            )

    # We are leaving this unittest commented because pytest seems to hang when it runs
    #   because we are going out to aws.
    def test_cloud_watch_logging_method(self):
        AppLogger.configure_and_get_logger(
            logger_name='test_cloud_watch',
            config_section_name=AppLoggerJsonConfigName.default_with_watchtower_format_1(),
            watchtower_log_group='test_log_group',
            watchtower_stream_name='local'
        )
        with LogCapture() as lc:
            AppLogger.logger.info("test_me_aws")
            lc.check(
                ('test_cloud_watch', 'INFO', 'test_me_aws'),
            )

    def test_1__configure_logger_method(self):
        AppLogger.logger = logging.getLogger('test_configure_1')
        AppLogger.logger.level = logging.DEBUG
        AppLogger.config_dict = None

        with LogCapture() as lc:
            AppLogger._configure_logger()
            lc.check(
                ('test_configure_1', 'DEBUG', 'Getting Config Section for [default_format_1]'),
                ('test_configure_1', 'DEBUG', "Set logging configuration to: {'version': 1, 'disable_existing_loggers': 'false', 'formatters': {'default-single-line': {'style': '{', 'datefmt': '%Y-%m-%dT%H:%M:%S', 'format': '{name:<10s} | {levelname:8s} | {message:s}'}}, 'handlers': {'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler', 'formatter': 'default-single-line', 'stream': 'ext://sys.stdout'}}, 'loggers': {}, 'root': {'handlers': ['console']}}"),
            )


    def test_2__configure_logger_method(self):
        AppLogger.logger = logging.getLogger('test_configure_2')
        AppLogger.logger.level = logging.DEBUG
        AppLogger.config_dict = None

        with LogCapture() as lc:
            AppLogger._configure_logger(AppLoggerJsonConfigName.default_with_watchtower_format_1()) #, 'test_log_group', 'test_log_stream')
            lc.check_present(
                ('test_configure_2', 'DEBUG', 'Getting Config Section for [default_with_watchtower_format_1]'),
                ('test_configure_2', 'DEBUG', "Set logging configuration to: {'version': 1, 'disable_existing_loggers': 'false', 'formatters': {'default-single-line': {'style': '{', 'datefmt': '%Y-%m-%dT%H:%M:%S', 'format': '[{asctime:s}.{msecs:3.0f}] | {client_ip} | {host_name} | {levelname:8s} | {name:<10s} | {funcName:<10s} | {lineno:4d} | {message:s}'}}, 'handlers': {'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler', 'formatter': 'default-single-line', 'stream': 'ext://sys.stdout'}, 'watchtower': {'level': 'DEBUG', 'class': 'watchtower.CloudWatchLogHandler', 'formatter': 'default-single-line', 'log_group': 'default_with_watchtower_format_1', 'stream_name': 'default', 'send_interval': 1, 'create_log_group': 'True'}}, 'loggers': {}, 'root': {'handlers': ['console', 'watchtower']}}"),
            )
            self.assertEqual('default_with_watchtower_format_1', AppLogger.get_log_group())
            self.assertEqual('default', AppLogger.get_stream_name())

    def test_3__configure_logger_method(self):
        AppLogger.logger = logging.getLogger('test_configure_3')
        AppLogger.logger.level = logging.DEBUG
        AppLogger.config_dict = None

        with LogCapture() as lc:
            AppLogger._configure_logger(AppLoggerJsonConfigName.default_with_watchtower_format_1(), 'test_log_group', 'test_log_stream')
            lc.check_present(
                ('test_configure_3', 'DEBUG', 'Getting Config Section for [default_with_watchtower_format_1]'),
                ('test_configure_3', 'DEBUG', "Set logging configuration to: {'version': 1, 'disable_existing_loggers': 'false', 'formatters': {'default-single-line': {'style': '{', 'datefmt': '%Y-%m-%dT%H:%M:%S', 'format': '[{asctime:s}.{msecs:3.0f}] | {client_ip} | {host_name} | {levelname:8s} | {name:<10s} | {funcName:<10s} | {lineno:4d} | {message:s}'}}, 'handlers': {'console': {'level': 'DEBUG', 'class': 'logging.StreamHandler', 'formatter': 'default-single-line', 'stream': 'ext://sys.stdout'}, 'watchtower': {'level': 'DEBUG', 'class': 'watchtower.CloudWatchLogHandler', 'formatter': 'default-single-line', 'log_group': 'default_with_watchtower_format_1', 'stream_name': 'default', 'send_interval': 1, 'create_log_group': 'True'}}, 'loggers': {}, 'root': {'handlers': ['console', 'watchtower']}}"),
            )
            self.assertEqual('test_log_group', AppLogger.get_log_group())
            self.assertEqual('test_log_stream', AppLogger.get_stream_name())

    def test_4__configure_logger_method(self):
        AppLogger.logger = logging.getLogger('test_configure_3')
        AppLogger.logger.level = logging.DEBUG
        AppLogger.config_dict = None

        AppLogger._configure_logger(AppLoggerJsonConfigName.default_with_watchtower_format_1(), 'test_log_group', 'test_log_stream')
        AppLogger.set_debug_level()
        AppLogger.logger.debug('This is a test')

    def test__set_config_dict_method(self):
        AppLogger._set_config_dict('123')
        self.assertEqual('123', AppLogger.config_dict)

    def test__overwrite_logging_config_section_values_method(self):
        AppLogger.logger = logging.getLogger('test_overwrite')
        AppLogger.config_dict = {'handlers': {'watchtower': {'log_group': 'test1', 'stream_name': 'test2'}}}
        AppLogger._overwrite_logging_config_section_values('log_group_test1', 'stream_name_test1')
        self.assertEqual(
            {'handlers': {'watchtower': {'log_group': 'log_group_test1', 'stream_name': 'stream_name_test1'}}},
            AppLogger.config_dict)

        AppLogger.logger = logging.getLogger('test_overwrite')
        AppLogger.config_dict = {'handlers': {'watchtower': {'log_group': 'test1', 'stream_name': 'test2'}}}
        AppLogger._overwrite_logging_config_section_values(None, None)
        self.assertEqual(
            {'handlers': {'watchtower': {'log_group': 'test1', 'stream_name': 'test2'}}},
            AppLogger.config_dict)

    def test_get_logger_method(self):
        AppLogger.logger = logging.getLogger('test_get_logger')
        self.assertEqual('test_get_logger', AppLogger.logger.name)

    def test__set_logger_method(self):
        AppLogger.logger = None
        AppLogger._set_logger('test_set_logger1')
        self.assertEqual('test_set_logger1', AppLogger.logger.name)

        AppLogger.logger = logging.getLogger('test_set_logger2')
        AppLogger._set_logger('test_set_logger2')
        self.assertEqual('test_set_logger2', AppLogger.logger.name)

        AppLogger.logger = logging.getLogger('test_set_logger2')
        AppLogger._set_logger('test_set_logger3')
        self.assertEqual('test_set_logger3', AppLogger.logger.name)

    def test_get_log_group_method(self):
        AppLogger.config_dict = None
        self.assertEqual(None, AppLogger.get_log_group())

        AppLogger.config_dict = {'handlers': {'watchtower': {'log_group': 'test'}}}
        self.assertEqual('test', AppLogger.get_log_group())

        AppLogger.config_dict = {'handlers': ''}
        self.assertEqual(None, AppLogger.get_log_group())

        AppLogger.config_dict = {'handlers': {'watchtower': ''}}
        self.assertEqual(None, AppLogger.get_log_group())

        AppLogger.config_dict = {'handlers': {'watchtower': {'log_group': 'test2'}}}
        self.assertNotEqual('test', AppLogger.get_log_group())

    def test__set_log_group_method(self):
        AppLogger.logger = None
        AppLogger.config_dict = {'handlers': {'watchtower': {'log_group': 'test1'}}}
        AppLogger._set_log_group('test2')
        self.assertEqual({'handlers': {'watchtower': {'log_group': 'test1'}}}, AppLogger.config_dict)

        AppLogger.logger = logging.getLogger('test_set_logger')
        AppLogger.config_dict = None
        AppLogger._set_log_group('test')
        self.assertEqual(None, AppLogger.config_dict)

        AppLogger.config_dict = {'handlers': {'watchtower': {'log_group': 'test1'}}}
        AppLogger._set_log_group('test2')
        self.assertEqual({'handlers': {'watchtower': {'log_group': 'test2'}}}, AppLogger.config_dict)

        AppLogger.config_dict = {'handlers': {'watchtower': {'log_group': 'test1'}}}
        AppLogger._set_log_group(None)
        self.assertEqual({'handlers': {'watchtower': {'log_group': 'test1'}}}, AppLogger.config_dict)

    def test__log_group_exists_method(self):
        AppLogger.config_dict = None
        self.assertEqual(False, AppLogger._log_group_exists())

        AppLogger.config_dict = {'handlers': {'watchtower': {'log_group': 'test'}}}
        self.assertEqual(True, AppLogger._log_group_exists())

        AppLogger.config_dict = {'handlers': ''}
        self.assertEqual(False, AppLogger._log_group_exists())

        AppLogger.config_dict = {'handlers': {'watchtower': ''}}
        self.assertEqual(False, AppLogger._log_group_exists())

        AppLogger.config_dict = {'handlers': {'watchtower': {'log_group': 'test2'}}}
        self.assertNotEqual(False, AppLogger._log_group_exists())

    def test_get_stream_name_method(self):
        AppLogger.config_dict = None
        self.assertEqual(None, AppLogger.get_stream_name())

        AppLogger.config_dict = {'handlers': {'watchtower': {'stream_name': 'test'}}}
        self.assertEqual('test', AppLogger.get_stream_name())

        AppLogger.config_dict = {'handlers': ''}
        self.assertEqual(None, AppLogger.get_stream_name())

        AppLogger.config_dict = {'handlers': {'watchtower': ''}}
        self.assertEqual(None, AppLogger.get_stream_name())

        AppLogger.config_dict = {'handlers': {'watchtower': {'stream_name': 'test2'}}}
        self.assertNotEqual('test', AppLogger.get_stream_name())

    def test__set_stream_name_method(self):
        AppLogger.config_dict = None
        AppLogger._set_stream_name('test')
        self.assertEqual(None, AppLogger.config_dict)

        AppLogger.config_dict = {'handlers': {'watchtower': {'stream_name': 'test1'}}}
        AppLogger._set_stream_name('test2')
        self.assertEqual({'handlers': {'watchtower': {'stream_name': 'test2'}}}, AppLogger.config_dict)

        AppLogger.config_dict = {'handlers': {'watchtower': {'stream_name': 'test1'}}}
        AppLogger._set_stream_name(None)
        self.assertEqual({'handlers': {'watchtower': {'stream_name': 'test1'}}}, AppLogger.config_dict)

    def test__stream_name_exists_method(self):
        AppLogger.config_dict = None
        self.assertEqual(False, AppLogger._stream_name_exists())

        AppLogger.config_dict = {'handlers': {'watchtower': {'stream_name': 'test'}}}
        self.assertEqual(True, AppLogger._stream_name_exists())

        AppLogger.config_dict = {'handlers': ''}
        self.assertEqual(False, AppLogger._stream_name_exists())

        AppLogger.config_dict = {'handlers': {'watchtower': ''}}
        self.assertEqual(False, AppLogger._stream_name_exists())

        AppLogger.config_dict = {'handlers': {'watchtower': {'stream_name': 'test2'}}}
        self.assertNotEqual(False, AppLogger._stream_name_exists())

    # We are leaving this unittest commented because pytest seems to hang when it runs
    def test_set_logging_level_method(self):
        AppLogger.configure_and_get_logger(
            logger_name='test_logging_level',
            logging_level=logging.INFO)

        with LogCapture() as lc:
            AppLogger.logger.debug("debug test1")
            AppLogger.logger.info("info test1")
            AppLogger.logger.error("error test1")
            AppLogger.set_level(logging.DEBUG)
            AppLogger.logger.debug("debug test2")
            AppLogger.logger.info("info test2")
            AppLogger.logger.error("error test2")
            lc.check(
                ('test_logging_level', 'INFO', 'info test1'),
                ('test_logging_level', 'ERROR', 'error test1'),
                ('test_logging_level', 'DEBUG', 'debug test2'),
                ('test_logging_level', 'INFO', 'info test2'),
                ('test_logging_level', 'ERROR', 'error test2'),
            )

    def test_set_logging_level_with_aws_logging_method(self):
        AppLogger.configure_and_get_logger(
            logger_name='test_logging_level',
            config_section_name=AppLoggerJsonConfigName.default_with_watchtower_format_1(),
            watchtower_log_group="test_log_group",
            watchtower_stream_name="test_log_stream")

        AppLogger.logger.debug("debug test1")
        AppLogger.logger.info("info test1")
        AppLogger.logger.error("error test1")
        AppLogger.set_level(logging.DEBUG)
        AppLogger.logger.debug("debug test2")
        AppLogger.logger.info("info test2")
        AppLogger.logger.error("error test2")


if __name__ == '__main__':
    unittest.main()
