from ph_utils.logger import init_logger, log, sanic_logger_config


def test_logger():
    init_logger("app")
    print(sanic_logger_config("app"))
    log("logger")
    log("logger", "NAME")
    log("logger", "NAME", prefix="params")
    log(exception="fdsafds")


test_logger()
