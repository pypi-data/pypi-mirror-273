import inspect
import logging
import os
import threading
from pathlib import Path

from _pytest.config import Config
from _pytest.logging import get_log_level_for_setting

from pytest_xlsx import _plugin
from pytest_xlsx.file import XlsxFile
from pytest_xlsx.settings import settings

logger = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addini(
        "xlsx_meta_column_name",
        default="标记",
        help="设置标记的列名",
    )


def pytest_addhooks(pluginmanager):
    from . import hooks

    pluginmanager.add_hookspecs(hooks)


def pytest_configure(config: Config):
    log_file = config.getini("log_file")
    worker_id = os.environ.get("PYTEST_XDIST_WORKER")
    use_xdist = bool(config.getoption("tx", False))

    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(exist_ok=True)

    if use_xdist:
        config.option.dist = "loadscope"
        try:
            from xdist.dsession import DSession

            delattr(DSession, "pytest_collection")
        except (ImportError, AssertionError):
            pass

    if worker_id and log_file:  # Compatible with multiple processes
        new_filename = f"{log_file.stem}_{worker_id}{log_file.suffix}"
        log_file = log_file.parent / new_filename

        logging.basicConfig(
            format=config.getini("log_file_format"),
            filename=log_file,
            encoding="utf-8",
            level=get_log_level_for_setting(config.getini("log_file_level")),
        )

    xlsx_settings_dict = {
        "meta_column_name": config.getini("xlsx_meta_column_name"),
    }

    settings.reload_settings(xlsx_settings_dict)

    for klass_name, klass in inspect.getmembers(
        _plugin,
        lambda x: isinstance(x, type)
        and issubclass(x, _plugin.XlsxPlugin)
        and x is not _plugin.XlsxPlugin,
    ):
        config.pluginmanager.register(klass(config))


def pytest_collect_file(parent, file_path: Path):
    if file_path.suffix == ".xlsx" and file_path.name.startswith("test"):
        logger.debug(f"XlsxFile: {file_path.absolute()}")
        return XlsxFile.from_parent(parent, path=file_path)


def async_feedback(**kwargs):
    import importlib.metadata
    import platform
    import sys
    import time
    from urllib import parse, request

    name = str(__name__).split(".")[0]
    data = {
        "topic_id": "f5ba37dc-dd20-44aa-94be-cc0abbed251b",
        "name": name,
        "version": importlib.metadata.version(name),
        "python_version": sys.winver,
        "os": platform.uname()[0],
        "os_release": platform.uname()[2],
        "time": str(
            int(
                time.time() * 100,
            )
        ),
        # 'time_zone': time.timezone,
        # 'language': locale.getlocale(),
    }
    data.update(kwargs)

    url = "https://ap-chongqing.cls.tencentcs.com/track" + "?" + parse.urlencode(data)
    request.urlopen(url)


# threading.Thread(daemon=True, target=async_feedback).start()
