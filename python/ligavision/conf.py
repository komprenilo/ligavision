try:
    from pandas._config.config import (
        get_option,
        register_option,
        reset_option,
        set_option,
    )
except ModuleNotFoundError:
    from pandas.core.config import (
        get_option,
        register_option,
        reset_option,
        set_option,
    )

CONF_RIKAI_VIZ_COLOR = "rikai.viz.color"
DEFAULT_RIKAI_VIZ_COLOR = "red"
register_option(CONF_RIKAI_VIZ_COLOR, DEFAULT_RIKAI_VIZ_COLOR)