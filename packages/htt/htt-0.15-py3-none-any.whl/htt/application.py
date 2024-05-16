import datetime
import json
import logging
import logging.handlers
import multiprocessing
import os
import pathlib
import re
import signal
import socket
import sys

import google.protobuf.json_format
import google.protobuf.message
import logging_loki


class Application:
    _terminating = False

    def __init__(self) -> None:
        pass

    @staticmethod
    def is_terminating() -> bool:
        """Return true if the user asks the application to terminate

        Returns:
            bool: True if application is terminating
        """
        return Application._terminating

    @staticmethod
    def _set_terminating(*args):
        Application._terminating = True

    @staticmethod
    def read_config_from_file(
        config: google.protobuf.message,
        file: os.PathLike,
    ):
        """Read json-based config file into protobuf message

        Args:
            config (google.protobuf.message): Protobuf message to merge into
            file (os.PathLike): Config file to read
        """
        configFile = pathlib.Path(file)
        with configFile.open(mode="r") as configStream:
            configText = configStream.read()
            return google.protobuf.json_format.Parse(configText, config, ignore_unknown_fields=True)

    @staticmethod
    def write_config_to_file(
        config: google.protobuf.message,
        file: os.PathLike,
    ):
        """Write json-based config file from protobuf message

        Args:
            config (google.protobuf.message): Protobuf message to write
            file (os.PathLike): Config file to write
        """
        configText = google.protobuf.json_format.MessageToJson(
            config,
            including_default_value_fields=True,
        )
        configFile = pathlib.Path(file)
        configFile.parent.mkdir(parents=True, exist_ok=True)
        with configFile.open(mode="w") as configFile:
            configFile.write(configText)

    @staticmethod
    def read_config_from_environ(
        config: google.protobuf.message,
        environ_mapping: dict,
    ):
        """Read environ variables into protobuf message

        Args:
            config (google.protobuf.message): Protobuf message to merge into
            environ_mapping (dict): Environ mapping in { "env_name", ("field_name", "field_type") }
        """
        for env_name, (field_name, field_type) in environ_mapping.items():
            env_value = os.getenv(env_name)
            if env_value is not None:
                converted_value = Application._convert_environ_value(env_value, field_type)
                if hasattr(config, field_name):
                    setattr(config, field_name, converted_value)

    @staticmethod
    def _convert_environ_value(value, type):
        if type == "int":
            return int(value)
        elif type == "float":
            return float(value)
        elif type == "bool":
            return value.lower() in ("true")
        return value

    @staticmethod
    def create_logger(
        name: str = None,
        stderr_enabled: bool = False,
        stderr_level: int = logging.NOTSET,
        file_enabled: bool = False,
        file_level: int = logging.NOTSET,
        file_name: os.PathLike = None,
        file_size: int = 10,
        file_count: int = 30,
        syslog_enabled: bool = False,
        syslog_level: int = logging.NOTSET,
        syslog_address: str = None,
        syslog_socket_kind: socket.SocketKind = socket.SOCK_DGRAM,
        loki_enabled: bool = False,
        loki_level: int = logging.NOTSET,
        loki_endpoint: str = None,
        loki_user: str = None,
        loki_pass: str = None,
        loki_labels: dict = None,
    ):
        """Create logger with the specified handlers

        Args:
            name (str, optional): Logger name. Defaults to None.
            stderr_enabled (bool, optional): Enable logging to stderr. Defaults to False.
            stderr_level (int, optional): Logging level of stderr handler. Defaults to logging.NOTSET.
            file_enabled (bool, optional): Enable logging to file. Defaults to False.
            file_level (int, optional): Logging level of file handler. Defaults to logging.NOTSET.
            file_name (os.PathLike, optional): File name of the log files. Defaults to None.
            file_size (int, optional): Rotation size of the log files in MB. Defaults to 10.
            file_count (int, optional): Rotation count of the log files. Defaults to 30.
            syslog_enabled (bool, optional): Enable logging to syslog. Defaults to False.
            syslog_level (int, optional): Logging level of syslog handler. Defaults to logging.NOTSET.
            syslog_address (str, optional): Address of the syslog server in "{ip}:{port}". Defaults to None.
            syslog_sockettype (socket.SocketKind, optional): Socket type of the syslog server. Defaults to socket.SOCK_DGRAM.
            loki_enabled (bool, optional): Enable logging to loki. Defaults to False.
            loki_level (int, optional): Logging level of loki handler. Defaults to logging.NOTSET.
            loki_endpoint (str, optional): Push endpoint of the loki server in "{protocol}://{ip}:{port}/loki/api/v1/push". Defaults to None.
            loki_user (str, optional): User of the loki server. Defaults to None.
            loki_pass (str, optional): Pass of the loki server. Defaults to None.
            loki_labels (dict, optional): Labels describing the log stream. Defaults to None.

        Returns:
            Logger: Logger created with specified handlers
        """
        logger = logging.getLogger(name=name)
        if name:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.NOTSET)
        if stderr_enabled:
            stderr_handler = Application._create_stderr_handler()
            stderr_handler.setLevel(stderr_level)
            logger.addHandler(stderr_handler)
        if file_enabled:
            pathlib.Path(file_name).parent.mkdir(parents=True, exist_ok=True)
            file_handler = Application._create_file_handler(
                file_name,
                file_size,
                file_count,
            )
            file_handler.setLevel(file_level)
            logger.addHandler(file_handler)
        if syslog_enabled:
            syslog_handler = Application._create_syslog_handler(
                syslog_address,
                syslog_socket_kind,
            )
            syslog_handler.setLevel(syslog_level)
            logger.addHandler(syslog_handler)
        if loki_enabled:
            loki_handler = Application._create_loki_handler(
                loki_endpoint,
                loki_user,
                loki_pass,
                loki_labels,
            )
            loki_handler.setLevel(loki_level)
            logger.addHandler(loki_handler)
        return logger

    @staticmethod
    def get_logger(
        name: str = None,
    ):
        """Return a logger of the specified name. Logger must be created by create_logger() first.

        Returns:
            Logger: Logger of the specified name
        """
        return logging.getLogger(name=name)

    @staticmethod
    def _create_stderr_handler():
        formatter = _InlineFormatter()
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(formatter)
        return handler

    @staticmethod
    def _create_file_handler(
        file_name: os.PathLike,
        file_size: int,
        file_count: int,
    ):
        handler = logging.handlers.RotatingFileHandler(
            file_name,
            maxBytes=1048756 * file_size,
            backupCount=file_count,
            encoding="UTF-8",
        )
        formatter = _InlineFormatter()
        handler.setFormatter(formatter)
        return handler

    @staticmethod
    def _create_syslog_handler(
        syslog_address: str,
        syslog_socket_kind: socket.SocketKind,
    ):
        handler = logging.handlers.SysLogHandler(
            Application._split_address(syslog_address),
            socktype=syslog_socket_kind,
        )
        return handler

    @staticmethod
    def _create_loki_handler(
        loki_endpoint: str,
        loki_user: str,
        loki_pass: str,
        loki_labels: dict,
    ):
        kwargs = dict()
        if loki_endpoint:
            kwargs["url"] = loki_endpoint
        else:
            raise Exception("invalid loki_address")
        if loki_user:
            kwargs["auth"] = (loki_user, loki_pass)
        if loki_labels:
            kwargs["tags"] = loki_labels
        handler = logging_loki.LokiQueueHandler(
            multiprocessing.Queue(-1),
            **kwargs,
        )
        handler.formatter = _JsonFormatter()
        return handler

    @staticmethod
    def _split_address(address: str):
        match = re.match(r"^(.+):(\d+)$", address)
        if match:
            host = match.group(1)
            port = int(match.group(2))
        else:
            host = address
            port = None
        return (host, port)


class _DateTimeFormatter(logging.Formatter):
    default_time_format = "%Y-%m-%dT%H:%M:%S.%f%z"

    def formatTime(self, record, datefmt=None) -> str:
        ct = datetime.datetime.fromtimestamp(record.created, datetime.datetime.now().astimezone().tzinfo)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.strftime(self.default_time_format)
        return s


class _LevelFormatter(logging.Formatter):
    default_formatter = _DateTimeFormatter
    default_notset_format = "%(levelname).1s %(asctime)s | %(message)s"
    default_debug_format = "%(levelname).1s %(asctime)s | %(message)s"
    default_info_format = "%(levelname).1s %(asctime)s | %(message)s"
    default_warning_format = "%(levelname).1s %(asctime)s | %(message)s"
    default_error_format = "%(levelname).1s %(asctime)s | %(message)s (%(module)s:%(lineno)d)"
    default_critical_format = "%(levelname).1s %(asctime)s | %(message)s (%(module)s:%(lineno)d)"

    def __init__(self, formats=None, **kwargs):
        if "fmt" in kwargs:
            raise ValueError("format string must be passed by formats")
        if formats:
            if not isinstance(formats, dict):
                raise ValueError("formats must be a level to format string dictionary")
            self.formatters = {}
            for loglevel in formats:
                self.formatters[loglevel] = self.default_formatter(fmt=formats[loglevel], **kwargs)
        else:
            self.formatters = {
                logging.NOTSET: self.default_formatter(fmt=self.default_notset_format, **kwargs),
                logging.DEBUG: self.default_formatter(fmt=self.default_debug_format, **kwargs),
                logging.INFO: self.default_formatter(fmt=self.default_info_format, **kwargs),
                logging.WARNING: self.default_formatter(fmt=self.default_warning_format, **kwargs),
                logging.ERROR: self.default_formatter(fmt=self.default_error_format, **kwargs),
                logging.CRITICAL: self.default_formatter(fmt=self.default_critical_format, **kwargs),
            }

    def format(self, record: logging.LogRecord) -> str:
        formatter = self.formatters.get(record.levelno, self.formatters.get(logging.NOTSET))
        return formatter.format(record)


class _InlineFormatter(logging.Formatter):
    default_time_format = "%Y-%m-%dT%H:%M:%S.%f%z"

    def format(self, record: logging.LogRecord) -> str:
        time = datetime.datetime.fromtimestamp(record.created, datetime.datetime.now().astimezone().tzinfo).strftime(
            _JsonFormatter.default_time_format
        )
        merged_tags = dict()
        record_tags = getattr(record, "tags", None)
        if record_tags and isinstance(record_tags, dict):
            merged_tags |= record_tags
        record_lite_tags = getattr(record, "liteTags", None)
        if record_lite_tags and isinstance(record_lite_tags, dict):
            merged_tags |= record_lite_tags
        if record.levelno == logging.ERROR or record.levelno == logging.CRITICAL:
            merged_tags["caller"] = f"{record.module}:{record.lineno}"
        if merged_tags:
            if record.exc_info:
                return f"{time} {record.levelname[0]} | {record.msg} {json.dumps(merged_tags)}\n{self.formatException(record.exc_info)}"
            else:
                return f"{time} {record.levelname[0]} | {record.msg} {json.dumps(merged_tags)}"
        else:
            if record.exc_info:
                return f"{time} {record.levelname[0]} | {record.msg}\n{self.formatException(record.exc_info)}"
            else:
                return f"{time} {record.levelname[0]} | {record.msg}"


class _JsonFormatter(logging.Formatter):
    default_time_format = "%Y-%m-%dT%H:%M:%S.%f%z"

    def __init__(self, indent=None, **kwargs):
        self._indent = indent

    def format(self, record: logging.LogRecord) -> str:
        merged_tags = dict()
        record_tags = getattr(record, "tags", None)
        if record_tags and isinstance(record_tags, dict):
            merged_tags |= record_tags
        record_lite_tags = getattr(record, "liteTags", None)
        if record_lite_tags and isinstance(record_lite_tags, dict):
            merged_tags |= record_lite_tags
        json_record = dict()
        json_record["message"] = record.msg
        json_record["level"] = record.levelname
        json_record["time"] = datetime.datetime.fromtimestamp(
            record.created, datetime.datetime.now().astimezone().tzinfo
        ).strftime(_JsonFormatter.default_time_format)
        json_record["server"] = socket.gethostname()
        json_record["tags"] = merged_tags
        if record.levelno == logging.ERROR or record.levelno == logging.CRITICAL:
            json_record["caller"] = f"{record.module}:{record.lineno}"
        if record.exc_info:
            json_record["exception"] = self.formatException(record.exc_info)
        return json.dumps(json_record, indent=self._indent)


signal.signal(signal.SIGINT, Application._set_terminating)
signal.signal(signal.SIGTERM, Application._set_terminating)
