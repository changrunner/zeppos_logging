import logging
import socket


class AppLoggerFilter(logging.Filter):
    def filter(self, record):
        record.client_ip = self.get_client_ip()
        record.host_name = self.get_host_name()
        return True

    def get_client_ip(self):
        hostname = self.get_host_name()
        ip_address = socket.gethostbyname(hostname)
        return ip_address

    def get_host_name(self):
        return socket.gethostname()
