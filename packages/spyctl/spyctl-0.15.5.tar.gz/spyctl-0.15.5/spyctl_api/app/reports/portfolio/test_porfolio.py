import pytest
import json
import os

from app.reports.report_lib import ReportInput
from app.reports.report_engine import ReportEngine

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
ORG = os.getenv("ORG")


@pytest.fixture()
def engine():
    yield ReportEngine({
        "backend": {
            "kind": "simple_file",
            "dir": "/tmp/reports"
        }
    })

def report_input(filename):
    import os
    cwd = os.getcwd()
    with open(cwd + f"/app/reports/portfolio/testdata/{filename}") as f:
        report_input = json.load(f)
        report_input["org_uid"] = ORG
        ri = ReportInput.model_validate(report_input)
        return ri

def test_report_agent_metrics(engine):
    if not API_KEY or not API_URL or not ORG:
        return

    ri = report_input("repagent.json")
    report = engine.make_report(ri, API_KEY, API_URL)
    assert len(report) > 0
    assert "Spyderbat agent usage report" in report

def test_report_ops(engine):
    if not API_KEY or not API_URL or not ORG:
        return

    ri = report_input("repops.json")
    report = engine.make_report(ri, API_KEY, API_URL)
    assert len(report) > 0
    assert "Operational report" in report

