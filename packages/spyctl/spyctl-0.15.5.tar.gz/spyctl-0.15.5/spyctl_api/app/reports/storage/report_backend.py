from typing import Protocol

from app.reports.report import Report
from app.reports.report_lib import ReportInput



class ReportBackend(Protocol):

    async def register_report(self, report: Report): ...

    async def update_report(self, report: Report): ...

    async def get_report(self, id: str, org_uid: str) -> Report: ...

    async def delete_report(self, id: str, org_uid: str): ...

    async def list_reports(self, org_uid: str) -> list[Report]: ...

    async def publish_report_file(
        self, report: Report, report_bytes: bytes
    ): ...

    async def download_report_file(self, id, org_uid: str) -> str: ...


def get_backend(backend_config: dict) -> ReportBackend:
    match backend_config["kind"]:
        case "s3":
            from app.reports.storage.s3_backend import S3Backend
            return S3Backend(backend_config)
        case "simple_file":
            from app.reports.storage.simple_file_backend import SimpleFileBackend
            return SimpleFileBackend(backend_config)
        case _:
            raise ValueError("Unsupported backend kind")
