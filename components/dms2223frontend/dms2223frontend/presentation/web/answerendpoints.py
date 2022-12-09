""" DiscussionEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template, request, current_app, flash
from werkzeug.wrappers import Response
from dms2223common.data import Role
from dms2223frontend.data.rest.authservice import AuthService
from .webauth import WebAuth
from dms2223frontend.data.rest.backendservice import BackendService
from dms2223common.data.rest import ResponseData
from .webutils import WebUtils
from .webanswer import WebAnswer


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

        # current_app.logger.info(responseAnsw.get_content())
        if(responseAnsw.get_content() == []):
            answers = []
        else:
            answers = responseAnsw.get_content().values()
        
        responseQuest: ResponseData = backend_service.get_question(session.get('token'), qid)
        WebUtils.flash_response_messages(responseQuest)
        question = responseQuest.get_content()
        # current_app.logger.info(answers)
        return render_template('questions/answers.html', name=name, roles=session['roles'], answers=answers, question=question)
        
    @staticmethod
    def get_new_answer(backend_service: BackendService, auth_service: AuthService) -> Union[Response, Text]:
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
        qid = request.args.get('qid')
        content = request.form.get('content')
        
        return render_template('new_answer.html', name=name, roles=session['roles'],
        	qid=str(qid), content=str(content))

    @staticmethod
    def post_new_answer(backend_service: BackendService, auth_service: AuthService) -> Union[Response, Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        qid = request.form.get('qid')
        content = request.form.get('bodyText')

        new_answer = WebAnswer.new_answer(backend_service, qid, content=content)
        if not new_answer:
            return redirect(url_for('get_new_answer') + "?qid=" + str(qid))
        redirect_to = request.form['redirect_to']
        if not redirect_to:
            redirect_to = url_for('get_answers')
        return redirect(redirect_to)

    @staticmethod
    def get_new_comment(auth_service: AuthService) -> Union[Response, Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))
        name = session['user']

        # Obtenemos los nuevos datos introducidos
        aid = request.args.get('aid')
        qid = request.args.get('qid')
        
        return render_template('new_comment.html', name=name, roles=session['roles'],
        	#Añadir el resto de la estructura que metamos en la base de datos
        	aid=str(aid), qid=str(qid))      

    @staticmethod
    def post_new_comment(backend_service: BackendService, auth_service: AuthService) -> Union[Response, Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        aid = request.form.get('aid')
        content = request.form.get('bodyText')
        sentiment = request.form.get('sent')

        new_comment = WebAnswer.new_comment(backend_service, aid, content, sentiment)
        if not new_comment:
            return redirect(url_for('get_new_comment') + "?aid=" + str(aid))
        redirect_to = request.form['redirect_to']
        if not redirect_to:
            redirect_to = url_for('get_answers')
        return redirect(redirect_to)
    
    @staticmethod
    def get_new_report_answer(backend_service: BackendService, auth_service: AuthService) -> Union[Response, Text]:
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
        aid = request.args.get('aid')
        qid = request.args.get('qid')
        # current_app.logger.info(qid)
        reason = request.form.get('reason')
        
        return render_template('new_report_answer.html', name=name, roles=session['roles'],
        	aid=aid, qid=qid, reason=str(reason))


    @staticmethod
    def post_new_report_answer(backend_service: BackendService, auth_service: AuthService) -> Union[Response, Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))
            
        aid = request.form.get('aid')
        reason = request.form.get('bodyText')
        # current_app.logger.info(qid)
        new_answer = WebAnswer.new_report_answer(backend_service, aid=aid, reason=str(reason))
        if not new_answer:
            return redirect(url_for('get_new_answer'))
        redirect_to = request.form['redirect_to']
        if not redirect_to:
            redirect_to = url_for('get_answers')
        return redirect(redirect_to)

    @staticmethod
    def get_new_report_comment(backend_service: BackendService, auth_service: AuthService) -> Union[Response, Text]:
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

        cid = request.args.get('cid')
        qid = request.args.get('qid')
        aid = request.args.get('aid')
        # current_app.logger.info(qid)
        reason = request.form.get('reason')
        
        return render_template('new_report_comment.html', name=name, roles=session['roles'],
        	cid=cid, aid=aid, qid=qid, reason=str(reason))

    @staticmethod
    def post_new_report_comment(backend_service: BackendService, auth_service: AuthService) -> Union[Response, Text]:
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
        # name = session['user']
        cid = request.form.get('cid')
        # Obtenemos los nuevos datos introducidos
        # aid = request.form.get('aid')
        reason = request.form.get('reason')
        
        new_answer = WebAnswer.new_report_comment(backend_service, cid=cid, reason=str(reason))
        if not new_answer:
            return redirect(url_for('get_new_answer'))
        redirect_to = request.form['redirect_to']
        if not redirect_to:
            redirect_to = url_for('get_answers')
        return redirect(redirect_to)

    @staticmethod
    def post_new_answer_vote(backend_service: BackendService, auth_service: AuthService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))
        
        aid = request.form.get('aid')
        qid = request.form.get('qid')

        WebAnswer.new_answer_vote(backend_service, aid)
        return redirect("/questions/answers?qid=" + str(qid))

    @staticmethod
    def post_new_comment_vote(backend_service: BackendService, auth_service: AuthService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))
        
        cid = request.form.get('cid')
        qid = request.form.get('qid')

        WebAnswer.new_comment_vote(backend_service, cid)
        return redirect("/questions/answers?qid=" + str(qid))