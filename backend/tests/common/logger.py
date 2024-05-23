import logging
import time
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

LOG_PATH = os.path.join(BASE_PATH, "log")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


class Logger:

    def __init__(self):
        self.log_name = os.path.join(LOG_PATH, "{}.log".format(time.strftime("%Y%m%d")))
        self.logger = logging.getLogger("log")
        self.logger.setLevel(logging.DEBUG)

        self.formatter = logging.Formatter(
            '[%(asctime)s][%(filename)s %(lineno)d][%(levelname)s]: %(message)s')

        self.file_logger = logging.FileHandler(self.log_name, mode='a', encoding="UTF-8")
        self.console = logging.StreamHandler()
        self.console.setLevel(logging.DEBUG)
        self.file_logger.setLevel(logging.DEBUG)
        self.file_logger.setFormatter(self.formatter)
        self.console.setFormatter(self.formatter)
        self.logger.addHandler(self.file_logger)
        self.logger.addHandler(self.console)


logger = Logger().logger


def logger_info_base(http_code: str, http_status: str, res):
    logger.info("http_code ==>> except_res：{}， real_res： {}".format(http_code, res.status_code))
    logger.info("http_status ==>> except_res：{}， real_res： {}".format(http_status, res.json()["status"]))


def logger_info(http_code: str, http_status: str, res):
    logger_info_base(http_code, http_status, res)
    logger.info("total_count ==>> real_res： {}".format(res.json()["total_count"]))
    logger.info("fetched_count ==>> real_res： {}".format(res.json()["fetched_count"]))


def logger_ready_or_creating_info(http_code: str, http_status: str, res):
    logger_info_base(http_code, http_status, res)
    logger.info("data_status ==>> real_res： {}".format(res.json()["data"]["status"]))


def logger_success_info(http_code: str, http_status: str, data_status, res):
    logger_info_base(http_code, http_status, res)
    logger.info("data_status ==>> except_res：{}， real_res： {}".format(data_status, res.json()["data"]["status"]))


def logger_error_info(http_code: str, http_status: str, data_status, res):
    logger_info_base(http_code, http_status, res)
    logger.info("data_status ==>> except_res：{}， real_res： {}".format(data_status, res.json()["error"]["code"]))
