from datetime import datetime
from unittest.mock import Mock

import pandas as pd
from dateutil.tz import tzlocal
from kpireport.report import Report, Theme
from kpireport.tests.fixtures import FakeOutputDriver
from kpireport.tests.utils import make_datasource_manager
from kpireport.view import make_render_env
from kpireport_plot import Plot


def _report_with_tz(tz):
    return Report(
        title="tz report",
        interval_days=7,
        start_date=datetime(2020, 5, 1, tzinfo=tz),
        end_date=datetime(2020, 5, 7, tzinfo=tz),
        timezone=tz,
        theme=Theme(),
    )


def test_render_with_tzinfo_timezone(jinja_env):
    # The report timezone (a tzinfo object, tzlocal() by default) is passed into
    # the matplotlib rc_context. matplotlib's "timezone" rcParam only accepts a
    # string, so a too-new matplotlib rejects the object and the plot fails to
    # render. Guards the matplotlib pin in requirements.txt.
    report = _report_with_tz(tzlocal())
    ds_mgr = make_datasource_manager({"usage": Mock()})
    ds_mgr.get_instance("usage").query.return_value = pd.DataFrame(
        {"time": ["2020-05-01", "2020-05-02"], "value": [1.0, 2.0]}
    )

    view = Plot(
        report,
        ds_mgr,
        datasource="usage",
        query="select 1",
        kind="bar",
    )
    output = view.render(
        make_render_env(jinja_env, view, FakeOutputDriver(report), "html")
    )

    assert isinstance(output, str)
