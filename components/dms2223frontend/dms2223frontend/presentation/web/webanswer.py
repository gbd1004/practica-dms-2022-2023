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