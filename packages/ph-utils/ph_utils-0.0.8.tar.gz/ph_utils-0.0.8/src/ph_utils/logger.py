# Copyright (c) [2023] [Tenny]
# [ph-utils] is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#         http://license.coscl.org.cn/MulanPSL2
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.
from logging import config, Formatter, LogRecord
import logging
import json
import os
from pathlib import Path
import sys


class JsonFormatter(Formatter):
    """将日志记录为 json 格式

    Args:
        Formatter (logging.Formatter): 日志格式化
    """

    def format(self, record: LogRecord) -> str:
        return json.dumps(
            {
                "message": super().format(record),
                "name": record.name,
                "levelname": record.levelname,
                "lineno": record.lineno,
                "asctime": self.formatTime(record),
            }
        )

    def formatMessage(self, record: LogRecord) -> str:
        return record.getMessage()


def logger_config(
    filename=None, dir_path=None, level="DEBUG", formatter="basic", loggers=None
):
    """日志配置

    Args:
        filename (str): 日志文件名称, 如果为 None 则不记录日志到文件, 该名称不能带上后缀名
        dir (str): 日志文件记录路径, 默认为: cwd() + 'logs'
        level (str): 日志记录的等级, 默认为: DEBUG, DEBUG、INFO
        formatter (str): 日志格式化形式, basic、json
        loggers (dict): 日志记录器, 原生的 loggers
    """
    lsformatter = "logging.Formatter"
    if formatter == "json":
        lsformatter = "libs.logging.JsonFormatter"
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "app.error": {
                "level": "ERROR",
                "handlers": ["error_console"],
                "propagate": False,
                "qualname": "app.error",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": sys.stdout,
            },
            "error_console": {
                "class": "logging.StreamHandler",
                "formatter": "generic",
                "stream": sys.stderr,
            },
            "access_console": {
                "class": "logging.StreamHandler",
                "formatter": "access",
                "stream": sys.stdout,
            },
        },
        "formatters": {
            "generic": {
                "format": "[%(asctime)s] (%(name)s) [%(levelname)s] [%(lineno)d]: %(message)s",
                "class": lsformatter,
            },
            "access": {
                "format": "[%(asctime)s] (%(name)s) [%(levelname)s] [%(host)s]: %(request)s %(message)s %(status)s %(byte)s",
                "class": "logging.Formatter",
            },
        },
        "root": {"handlers": ["console"], "level": level},
    }
    if loggers:
        log_config["loggers"].update(loggers)
    if filename is not None:  # 记录日志到文件
        # 解析目录
        if not dir_path:
            dir_path = Path(os.getcwd(), "logs")
        else:
            dir_path = Path(dir_path)
        # 目录不存在, 则新建
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
        # 存储目录必须为目录
        if dir_path.is_file():
            raise Exception("dir must be director")
        dir_path = dir_path.joinpath(filename)
        dir_path = dir_path.as_posix()
        file_handler = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "generic",
            "filename": f"{dir_path}.log",
            "backupCount": 2,
            "maxBytes": 10485760,  # 10M
            "encoding": "utf-8",
        }
        err_file_handler = {}
        err_file_handler.update(file_handler)
        err_file_handler["filename"] = f"{dir_path}_error.log"
        err_file_handler["level"] = "ERROR"
        err_file_handler["backupCount"] = 7
        # 配置记录到文件
        log_config["handlers"].setdefault("file_handler", file_handler)
        log_config["handlers"].setdefault("file_err_handler", err_file_handler)
        sanic_error = log_config["loggers"].get("sanic.error")
        if sanic_error:
            sanic_error["handlers"].append("file_err_handler")
        log_config["loggers"]["app.error"]["handlers"].append("file_err_handler")
        log_config["root"]["handlers"].append("file_handler")
        log_config["root"]["handlers"].append("file_err_handler")
    return log_config


def init_logger(
    filename=None, dir_path=None, level="DEBUG", formatter="basic", loggers=None
):
    """初始化日志记录

    Args:
        filename (str, optional): 日志文件名称. Defaults to None.
        dir_path (str, optional): 日志记录文件夹. Defaults to cwd() + logs.
        level (str, optional): 记录的日志等级. Defaults to "DEBUG".
        formatter (str, optional): 日志格式, basic、json; json - JSON格式的日志. Defaults to "basic".
        loggers (dict, optional): 日志记录器. Defaults to None.
    """
    config.dictConfig(logger_config(filename, dir_path, level, formatter, loggers))


def sanic_logger_config(filename=None, dir_path=None, level="DEBUG", formatter="basic"):
    """Sanic框架的日志配置

    Args:
        filename (str, optional): 日志文件名称. Defaults to None.
        dir_path (str, optional): 日志记录文件夹. Defaults to cwd() + logs.
        level (str, optional): 记录的日志等级. Defaults to "DEBUG".
        formatter (str, optional): 日志格式, basic、json; json - JSON格式的日志. Defaults to "basic".

    Returns:
        dict: 日志配置
    """
    return logger_config(
        filename,
        dir_path,
        level,
        formatter,
        {
            "sanic.access": {
                "level": "INFO",
                "handlers": ["access_console"],
                "propagate": False,
                "qualname": "sanic.access",
            },
            "sanic.error": {
                "level": "ERROR",
                "handlers": ["error_console"],
                "propagate": False,
                "qualname": "sanic.error",
            },
        },
    )


def log(msg=None, name=None, exception=None, level="info", prefix=None):
    """日志记录

    Args:
        msg (str, optional): 记录的日志信息. Defaults to None.
        name (str, optional): 日志 name 标记. Defaults to None.
        exception (Exception, optional): 异常信息. Defaults to None.
        level (str, optional): 日志等级. Defaults to 'info'.
        prefix (str, optional): 日志的基础信息, 用于拼接在日志信息的前面, default: None
    """
    except_error = exception
    if not except_error and isinstance(msg, Exception):
        except_error = msg
    if except_error:
        logging.getLogger("app.error").exception(exception)
    else:
        logger = logging if name is None else logging.getLogger(name)
        msg_txt = f"{prefix}: " if prefix else ""
        msg = str(msg) if msg else "None"
        fn = getattr(logger, level, None)
        if fn:
            fn(f"{msg_txt}{msg}")


def debug(msg=None, name=None, prefix=None):
    """记录 debug 日志

    Args:
        msg (str, optional): 日志信息. Defaults to None.
        name (str, optional): 日志名称 name 标记. Defaults to None.
        prefix (str, optional): 日志前缀. Defaults to None.
    """
    log(msg, name, None, "debug", prefix)


def info(msg=None, name=None, prefix=None):
    """记录 info 日志

    Args:
        msg (str, optional): 日志信息. Defaults to None.
        name (str, optional): 日志名称 name 标记. Defaults to None.
        prefix (str, optional): 日志前缀. Defaults to None.
    """
    log(msg, name, None, "info", prefix)


def warning(msg=None, name=None, prefix=None):
    """记录 warning 日志

    Args:
        msg (str, optional): 日志信息. Defaults to None.
        name (str, optional): 日志名称 name 标记. Defaults to None.
        prefix (str, optional): 日志前缀. Defaults to None.
    """
    log(msg, name, None, "warning", prefix)


def error(msg=None, name=None, prefix=None):
    """记录 error 日志

    Args:
        msg (str, optional): 日志信息. Defaults to None.
        name (str, optional): 日志名称 name 标记. Defaults to None.
        prefix (str, optional): 日志前缀. Defaults to None.
    """
    log(msg, name, None, "error", prefix)
