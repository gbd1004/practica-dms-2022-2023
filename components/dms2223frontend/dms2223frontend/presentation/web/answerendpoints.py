""" DiscussionEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template, request, current_app
from werkzeug.wrappers import Response
from dms2223common.data import Role
from dms2223frontend.data.rest.authservice import AuthService
from .webauth import WebAuth
from dms2223frontend.data.rest.backendservice import BackendService
from dms2223common.data.rest import ResponseData
from .webutils import WebUtils


class AnswerEndpoints():
    """ Monostate class responsible of handling the discussion web endpoint requests.
    """
    @staticmethod
    def get_answers(backend_service: BackendService, auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the question root endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))
        qid = request.args.get('qid')
        name = session['user']
        responseAnsw: ResponseData = backend_service.get_answers(session.get('token'), qid)
        WebUtils.flash_response_messages(responseAnsw)
        answers = responseAnsw.get_content().values()
        current_app.logger.info(answers)

        
        responseQuest: ResponseData = backend_service.get_question(session.get('token'), qid)
        WebUtils.flash_response_messages(responseQuest)
        question = responseQuest.get_content()
        # current_app.logger.info(answers)
        return render_template('questions/answers.html', name=name, roles=session['roles'], answers=answers, question=question)
        
    @staticmethod
    def new_answer(auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the POST requests to the question root endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']

        # Obtenemos los nuevos datos introducidos
        aid = request.form.get('aid')
        content = request.form.get('content')
        
        return render_template('new_answer.html', name=name, roles=session['roles'],
        	#Añadir el resto de la estructura que metamos en la base de datos
        	aid=aid, content=str(content))

    @staticmethod
    def new_comment(backend_service: BackendService, auth_service: AuthService) -> Union[Response, Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']

        # Obtenemos los nuevos datos introducidos
        aid = request.form.get('aid')
        cid = request.form.get('qid')
        content = request.form.get('content')
        
        return render_template('new_comment.html', name=name, roles=session['roles'],
        	#Añadir el resto de la estructura que metamos en la base de datos
        	aid=aid, content=str(content))        
        	
        




