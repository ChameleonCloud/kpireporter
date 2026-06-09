from unittest import mock

import pytest
from kpireport.report import Content, Report
from kpireport_s3 import S3OutputDriver


def test_render_output(report: "Report", content: "Content", mocker: "mock"):
    out = S3OutputDriver(report, bucket="fake-bucket")
    s3 = mocker.patch.object(out, "s3")
    out.render_output(content, [])
    # The static driver writes both the dated report dir and a "latest" alias;
    # os.walk upload order isn't stable across filesystems, so assert membership.
    s3.upload_file.assert_any_call(
        f"{out.output_dir}/{report.id}/index.html",
        "fake-bucket",
        f"{report.id}/index.html",
    )
    s3.upload_file.assert_any_call(
        f"{out.output_dir}/latest-{report.title_slug}/index.html",
        "fake-bucket",
        f"latest-{report.title_slug}/index.html",
    )


def test_missing_bucket(report: "Report"):
    with pytest.raises(ValueError):
        S3OutputDriver(report)
