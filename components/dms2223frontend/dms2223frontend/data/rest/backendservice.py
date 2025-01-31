""" BackendService class module.
"""
from typing import Optional
import requests #type: ignore
from dms2223common.data.rest import ResponseData
from flask import current_app


class BackendService():
    """ REST client to connect to the backend service.
    """

    def __init__(self,
        host: str, port: int,
        api_base_path: str = '/api/v1',
        apikey_header: str = 'X-ApiKey-Backend',
        apikey_secret: str = ''
        ):
        """ Constructor method.

        Initializes the client.

        Args:
            - host (str): The backend service host string.
            - port (int): The backend service port number.
            - api_base_path (str): The base path that is prepended to every request's path.
            - apikey_header (str): Name of the header with the API key that identifies this client.
            - apikey_secret (str): The API key that identifies this client.
        """
        self.__host: str = host
        self.__port: int = port
        self.__api_base_path: str = api_base_path
        self.__apikey_header: str = apikey_header
        self.__apikey_secret: str = apikey_secret

    def __base_url(self) -> str:
        return f'http://{self.__host}:{self.__port}{self.__api_base_path}'

    def new_question(self, token, title: Optional[str], body: Optional[str]):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + '/questions',
            json={
                'title': title,
                'body': body
            },
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def get_questions(self, token: Optional[str]):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/questions',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def get_question(self, token: Optional[str], qid: Optional[str]):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/questions/{qid}',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def get_questions_reports(self, token):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/questions/reports',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        current_app.logger.info(response)
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def get_answers(self, token, qid: Optional[str]):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/questions/{qid}/answers',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def new_answer(self, token, qid: Optional[str], content: Optional[str]):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f'/questions/{qid}/answers',
            json = {
                'qid': qid,
                'body': content
            },
            headers= {
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def get_answers_reports(self, token):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/answers/reports',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        current_app.logger.info(response)
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def new_comment(self,token,aid: Optional[str],content: Optional[str],sentiment: Optional[str]):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f'/answers/{aid}/comments',
            json = {
                'body': content,
                'sentiment': sentiment
            },
            headers= {
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def get_comments_reports(self, token):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.get(
            self.__base_url() + f'/comments/reports',
            headers={
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        current_app.logger.info(response)
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
            response_data.set_content([])
        return response_data

    def new_report_question(self, token, qid: Optional[str], reason: Optional[str]):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f'/questions/{qid}/reports',
            json = {
                'reason': reason
            },
            headers= {
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def new_report_answer(self, token, aid: Optional[str], reason: Optional[str]):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f'/answers/{aid}/reports',
            json = {
                'reason': reason
            },
            headers= {
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def new_report_comment(self, token, cid: Optional[str], reason: Optional[str]):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f'/comments/{cid}/reports',
            json = {
                'reason': reason
            },
            headers= {
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def new_answer_vote(self, token, aid: Optional[str]):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f'/answers/{aid}/votes',
            headers= {
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def new_comment_vote(self, token, cid: Optional[str]):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.post(
            self.__base_url() + f'/comments/{cid}/votes',
            headers= {
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def put_question_report(self, token, qrid, status: str):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.put(
            self.__base_url() + f'/questions/reports/{qrid}',
            json = {
                'status': status
            },
            headers= {
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def put_answer_report(self, token, arid, status: str):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.put(
            self.__base_url() + f'/answers/reports/{arid}',
            json = {
                'status': status
            },
            headers= {
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data

    def put_comment_report(self, token, crid, status: str):
        response_data: ResponseData = ResponseData()
        response: requests.Response = requests.put(
            self.__base_url() + f'/comments/reports/{crid}',
            json = {
                'status': status
            },
            headers= {
                'Authorization': f'Bearer {token}',
                self.__apikey_header: self.__apikey_secret
            },
            timeout=60
        )
        response_data.set_successful(response.ok)
        if response_data.is_successful():
            response_data.set_content(response.json())
        else:
            response_data.add_message(response.content.decode('ascii'))
        return response_data
