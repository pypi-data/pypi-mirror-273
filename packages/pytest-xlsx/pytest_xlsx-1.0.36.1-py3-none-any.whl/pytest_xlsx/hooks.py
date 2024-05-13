import pytest
from _pytest.fixtures import FixtureRequest

from pytest_xlsx.file import XlsxItem


@pytest.hookspec(firstresult=True)
def pytest_xlsx_run_step(item: XlsxItem, request: FixtureRequest):
    """
    在执行Xlsx用例中的每一个步骤时，调用次hook
    这意味着对于同一个用例来讲，此hook可能被调用多次，具体调用次数取决于用例中的step数量
    每次调用时，item的current_step_no、current_step属性均会发生变化
    :param item: XlsxItems; Xlsx用例对象
    :param request: pytest的fixture，可以通过 `request.getfixturevalue(fixture_name)` 调用其他的fixture
    :return:
    """
    ...
