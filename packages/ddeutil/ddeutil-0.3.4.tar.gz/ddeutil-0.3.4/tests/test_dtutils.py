import datetime

import ddeutil.core.dtutils as dtutils


def test_get_date():
    assert datetime.datetime.now(
        tz=dtutils.LOCAL_TZ
    ).date() == dtutils.get_date("date")
