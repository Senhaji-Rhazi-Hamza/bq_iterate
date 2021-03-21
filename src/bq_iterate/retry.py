from bq_iterate import config

from tenacity import (
    retry as _retry,
    wait_exponential,
    before_sleep_log,
    before_log,
    stop_after_attempt,
)


def default_retry(fn):
    return _retry(
        wait=wait_exponential(
            multiplier=config.RETRY_CONF.get("wait_multiplier", 2),
            min=config.RETRY_CONF.get("wait_min", 4),
            max=config.RETRY_CONF.get("wait_max", 20),
        ),
        stop=stop_after_attempt(config.RETRY_CONF.get("stop_after_attempt", 5)),
        reraise=True,
        before=before_log(config.logger, config.logging.INFO),
        before_sleep=before_sleep_log(config.logger, config.logging.INFO),
    )(fn)


tn_retry = _retry
