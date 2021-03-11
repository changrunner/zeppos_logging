import unittest
from zeppos_logging.google_cloud_logger import GoogleCloudLogger
from zeppos_logging.google_cloud_message import GoogleCloudMessage
from zeppos_logging.app_logger_json_conifg_name import AppLoggerJsonConfigName
from testfixtures import LogCapture


class test_the_google_cloud_logger_methods(unittest.TestCase):
    def test_initiate_a_logger_method(self):
        GoogleCloudLogger.configure_and_get_logger(
            logger_name='test_google',
            config_section_name=AppLoggerJsonConfigName.default_with_google_cloud_format_1(),
            google_project_name='sandbox'
        )
        self.assertEqual('sandbox', GoogleCloudLogger.get_google_project_name())

    def test_send_hello_world_1_method(self):
        GoogleCloudLogger.configure_and_get_logger(
            logger_name='test_google_1',
            config_section_name=AppLoggerJsonConfigName.default_with_google_cloud_format_1(),
            google_project_name='sandbox'
        )
        with LogCapture() as lc:
            gc_message = GoogleCloudMessage()
            gc_message.message = "hello world"
            gc_message.data_dict["field1"] = "test1"
            GoogleCloudLogger.info(gc_message)

            lc.check(
                ('test_google_1', 'INFO', 'hello world'),
            )

    def test_send_hello_world_2_method(self):
        GoogleCloudLogger.configure_and_get_logger(
            logger_name='test_google_2',
            config_section_name=AppLoggerJsonConfigName.default_with_google_cloud_format_1(),
            google_project_name='sandbox'
        )
        with LogCapture() as lc:
            GoogleCloudLogger.info(GoogleCloudMessage("hello world", {"field1": "test1"}))

            lc.check(
                ('test_google_2', 'INFO', 'hello world'),
            )


    def test_send_hello_world_2_method(self):
        GoogleCloudLogger.configure_and_get_logger(
            logger_name='test_google_2',
            config_section_name=AppLoggerJsonConfigName.default_with_google_cloud_format_1(),
            google_project_name='sandbox'
        )
        GoogleCloudLogger.info(GoogleCloudMessage("hello world 3", {"field1": "test1"}))

if __name__ == '__main__':
    unittest.main()
