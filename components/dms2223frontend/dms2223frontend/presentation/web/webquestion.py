from typing import Optional
from flask import session
from dms2223common.data.rest import ResponseData
from dms2223frontend.data.rest.backendservice import BackendService
from .webutils import WebUtils

class WebQuestion():
    @staticmethod
    def new_question(backend_service: BackendService, title: Optional[str], body: Optional[str]):
        response: ResponseData = backend_service.new_question(session.get('token'),
            title=title, body=body)
        WebUtils.flash_response_messages(response)
        return response.get_content()

    @staticmethod
    def new_report_question(
        backend_service: BackendService, qid: Optional[str], reason: Optional[str]
    ):
        response: ResponseData = backend_service.new_report_question(session.get('token'),
            qid=qid, reason=reason)
        WebUtils.flash_response_messages(response)
        return response.get_content()
