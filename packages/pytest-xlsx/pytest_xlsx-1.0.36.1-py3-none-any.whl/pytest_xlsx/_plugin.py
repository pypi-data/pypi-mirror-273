from abc import ABCMeta, abstractmethod

import allure
import pytest
from pytest import FixtureRequest

from pytest_xlsx.file import XlsxItem


class XlsxPlugin(metaclass=ABCMeta):
    def __init__(self, config: pytest.Config):
        self.config = config

        self.__name__ = self.__class__.__name__  # 每个插件类，只能注册一次

    @abstractmethod
    def pytest_xlsx_run_step(self, item: XlsxItem, request: FixtureRequest): ...


class PrintXlsxPlugin(XlsxPlugin):
    @pytest.hookimpl(trylast=True)
    def pytest_xlsx_run_step(self, item: XlsxItem, request: FixtureRequest):
        print("-" * 10)
        print(f"当前用例id：{item.nodeid}")
        print(f"当前用例名称：{item.name}")
        print(f"当前用例步骤：{item.current_step}")
        print(f"当前用例步骤序号：{item.current_step_no}")
        print(f"最大用例步骤序号：{item.max_step_no}")
        print(f"当前是否第一个步骤：{item.is_first_step}")
        print(f"当前是否最后一个步骤：{item.is_last_step}")

        if item.is_last_step:
            print("=" * 20)


class AllureXlsxPlugin(XlsxPlugin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meta_column_name = self.config.getini("xlsx_meta_column_name")

    @pytest.hookimpl(tryfirst=True)
    def pytest_xlsx_run_step(self, item: XlsxItem, request: FixtureRequest):
        if self.meta_column_name not in item.current_step:
            return

        keys = list(item.current_step)
        arg_column_index = keys.index(self.meta_column_name) + 1
        if len(keys) <= arg_column_index:
            return None
        else:
            arg_column_name = keys[arg_column_index]

        mark = str(item.current_step.get(self.meta_column_name, ""))
        value = str(item.current_step.get(arg_column_name, ""))

        if not mark.startswith("allure"):
            return None
        if not value:
            return None

        label = mark.split("_")[-1]

        if label == "step":
            with allure.step(value):
                ...
        else:
            f = getattr(allure.dynamic, label)
            f(value)

        return True
