from typing import Dict, List, Optional
from flask import session
from dms2223common.data.rest import ResponseData
from dms2223frontend.data.rest.backendservice import BackendService
from .webutils import WebUtils

class WebAnswer():
    @staticmethod
    def new_answer(backend_service: BackendService, qid):
        response: ResponseData = backend_service.new_answer(session.get('token'), qid)
        WebUtils.flash_response_messages(response)
        return response.get_content()

    @staticmethod
    def new_comment(backend_service: BackendService, aid):
        response: ResponseData = backend_service.new_comment(session.get('token'), aid)
        WebUtils.flash_response_messages(response)
        return response.get_content()