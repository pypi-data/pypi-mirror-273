import copy
import itertools
import json
import logging
from string import Template
from typing import Iterable, Union

import pytest
from tabulate import tabulate

from pytest_xlsx import funcs, models
from pytest_xlsx.funcs import get_value_by_sequence

logger = logging.getLogger(__name__)


class XlsxFile(pytest.Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        class FakeObj(object):
            __doc__ = self.path

        self.obj = FakeObj

    def collect(self):
        for sheet in funcs.iter_xlsx_sheet(self.path):
            logger.debug(f"{self.path.absolute()} -> title={sheet.title}")
            yield XlsxSheet.from_parent(self, name=sheet.title, obj=sheet)


class XlsxSheet(pytest.Class):
    xlsx_data: models.Suite

    @classmethod
    def from_parent(cls, parent, *, name, obj=None, **kw):
        _ = super().from_parent(parent, name=name, **kw)
        _.obj = models.Suite(**dict(funcs.SheetHandler(obj).to_dict()))

        return _

    def collect(self) -> Iterable[Union[pytest.Item, pytest.Collector]]:
        for no, case in enumerate(
            self.obj.case_list
        ):  # 如果使用了参数化，返回多个XlsxItem
            yield from _case_to_xlsx_item(no, case, self)


class XlsxItem(pytest.Function):
    xlsx_data: models.Case  # xlsx数据内容
    max_step_no: int  # 最大步骤数
    current_step_no: int  # 当前步骤书
    current_step: dict  # 当前步骤内容
    usefixtures: dict  # fixtures

    def __init__(self, *args, own_markers=None, **kwargs):
        if own_markers and hasattr(self, "own_markers"):
            self.own_markers.extend(own_markers)
        super().__init__(*args, **kwargs)
        self.usefixtures = dict()

    @property
    def is_first_step(self):
        if self.current_step_no == 0:
            return True

        return False

    @property
    def is_last_step(self):
        if self.current_step_no >= self.max_step_no:
            return True

        return False

    @property
    def location(self):
        location = self.reportinfo()
        relfspath = self.session._node_location_to_relpath(self.path)

        assert type(location[2]) is str
        return relfspath, location[1], location[2]

    @classmethod
    def from_parent(cls, parent, name, case, marks, **kw):
        own_markers = []

        obj: XlsxItem = super().from_parent(
            parent,
            name=name,
            callobj=cls._call_obj,
            own_markers=own_markers,
            **kw,
        )
        obj.xlsx_data = case
        obj.max_step_no = len(case.steps) - 1

        for mark in marks:
            mark_name = mark[0]
            if mark_name == "usefixtures":
                fixture_name_list = [n.strip() for n in mark[1].split(",")]
                for fixture_name in fixture_name_list:
                    obj.usefixtures.setdefault(fixture_name, "no set")
            else:
                mark_func = getattr(pytest.mark, mark_name)
                mark_obj = mark_func(*mark[1:])
                own_markers.append(mark_obj)  # ???
                obj.add_marker(mark_obj)
        logger.debug(f"Generate new test: nodeid={obj.nodeid}, marks={marks} ")
        return obj

    @classmethod
    def from_parent_parametrize(
        cls, parent, name, case: models.Case, marks, parametrize_marks
    ):
        logger.debug(f"parametrize = {parametrize_marks}")
        arg_names = [i[0].split(",") for i in parametrize_marks]
        arg_vals = [funcs.LoadData(parent.path, i[1]).data for i in parametrize_marks]

        keys = [key.strip() for key in get_value_by_sequence(*arg_names)]

        case_str = case.json()

        for vals in itertools.product(*arg_vals):
            values = list(get_value_by_sequence(*vals))

            data_str = Template(case_str).safe_substitute(dict(zip(keys, values)))
            new_case = models.Case.validate(json.loads(data_str))
            new_case.meta["name"][0][0] += str(values)
            new_case.meta["mark"] = list(
                filter(lambda i: i[0] != "parametrize", new_case.meta["mark"])
            )
            yield from _case_to_xlsx_item(0, new_case, parent)

    def _call_obj(self, request: pytest.FixtureRequest):
        logger.debug(f"runrtest: {self.nodeid}")
        for fixture_name in self.usefixtures:
            logger.debug(f"request fixture: {fixture_name}")
            fixture_value = request.getfixturevalue(fixture_name)
            logger.debug(f"fixture value is: {fixture_value}")
            self.usefixtures[fixture_name] = fixture_value

        for i, step in enumerate(self.xlsx_data.steps):
            self.current_step_no = i
            self.current_step = step
            # xlsx_runner.execute(self)
            # 改为钩子调用，提供更多扩展性
            request.config.hook.pytest_xlsx_run_step(
                item=self,
                request=request,
            )

    def runtest(self) -> None:
        funcargs = self.funcargs
        testargs = {arg: funcargs[arg] for arg in self._fixtureinfo.argnames}

        self._call_obj(**testargs)

    def repr_failure(self, excinfo):
        style = self.config.getoption("tbstyle", "auto")
        if style == "auto":
            style = "value"

        tb_info = excinfo.traceback[-1]
        file_info = f"{tb_info.path}:{tb_info.lineno}: {excinfo.typename}"
        err_info = f"{self._repr_failure_py(excinfo, style=style)}"

        str_l = [
            "",
            file_info,
            err_info,
        ]
        if getattr(self, "current_step_no", -1) >= 0:  # 步骤已经开始执行
            error_line = self.current_step_no
            max_line = 10  # todo 从配置中读取
            if max_line <= 0:
                max_line = len(self.xlsx_data.steps)

            max_line_half = int(max_line / 2)  # 节选表格内容
            left, right = (error_line - max_line_half - 1), (error_line + max_line_half)
            if left < 0:
                left = 0

            xlsx_data = copy.deepcopy(self.xlsx_data)
            headers = []
            datas = []

            for i, step in enumerate(xlsx_data.steps):
                if i == 0:
                    headers = [""]
                    headers.extend(step.keys())
                else:
                    ...

                _BlankField = step.pop("_BlankField", [])
                if i == error_line:
                    data = [">>>"]
                else:
                    data = [""]

                data.extend(step.values())
                data.extend(_BlankField)

                datas.append(data)

                _len = len(data) - len(headers)  # 表头和内容长度差
                if _len > 0:
                    headers.extend([""] * _len)

            new_datas = datas[left:error_line] + datas[error_line:right]
            str_l[0] = "xlsx content: \n" + str(tabulate(new_datas, headers, "github"))

        # logger.warning(str_l[0])
        return "\n".join(str_l)


def _case_to_xlsx_item(
    no: int, case: models.Case, xlsx_sheet: XlsxSheet
) -> Iterable[Union[pytest.Item, pytest.Collector]]:
    try:
        case_name = case.meta["name"][0][0]
    except Exception:
        case_name = f"test_{no}"

    parametrize_marks = []
    other_marks = []

    for mark in case.meta.get("mark", []):
        if not mark:
            continue
        if mark[0] != "parametrize":
            other_marks.append(mark)
        else:
            parametrize_marks.append(mark[1:])

    if parametrize_marks:
        yield from XlsxItem.from_parent_parametrize(
            xlsx_sheet,
            name=case_name,
            case=case,
            marks=other_marks,
            parametrize_marks=parametrize_marks,
        )
    else:
        yield XlsxItem.from_parent(
            xlsx_sheet,
            name=case_name,
            case=case,
            marks=other_marks,
        )
