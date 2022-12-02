from typing import Dict, List, Optional
from flask import session
from dms2223common.data.rest import ResponseData
from dms2223frontend.data.rest.backendservice import BackendService
from .webutils import WebUtils

class WebAnswer():
    @staticmethod
    def new_answer(backend_service: BackendService, qid:int, content:str):
        response: ResponseData = backend_service.new_answer(session.get('token'), qid, content)
        WebUtils.flash_response_messages(response)
        return response.get_content()

    @staticmethod
    def new_report_answer(backend_service: BackendService, aid: int, reason: str):
        response: ResponseData = backend_service.new_report_answer(session.get('token'), aid=aid, reason=reason)
        WebUtils.flash_response_messages(response)
        return response.get_content()
    

    @staticmethod
    def new_comment(backend_service: BackendService, aid):
        response: ResponseData = backend_service.new_comment(session.get('token'), aid)
        WebUtils.flash_response_messages(response)
        return response.get_content()