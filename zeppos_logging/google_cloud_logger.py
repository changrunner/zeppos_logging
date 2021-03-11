from zeppos_logging.app_logger import AppLogger


class GoogleCloudLogger(AppLogger):
    @staticmethod
    def info(google_cloud_message):
        """
            Args:
                google_cloud_message (GoogleCloudMessage):
                    The message to be send to google cloud logging
        """
        AppLogger.logger.info(google_cloud_message.message, extra={"data": str(google_cloud_message.data_dict)})
