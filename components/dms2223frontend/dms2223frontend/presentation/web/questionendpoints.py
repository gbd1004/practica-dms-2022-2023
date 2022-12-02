""" DiscussionEndpoints class module.

"""



from typing import Text, Union
from flask import redirect, url_for, session, render_template, request
from werkzeug.wrappers import Response
from dms2223common.data import Role
from dms2223frontend.data.rest.authservice import AuthService
# Se importan del backend las preguntas
from .webauth import WebAuth
from dms2223frontend.data.rest.backendservice import BackendService
from dms2223common.data.rest import ResponseData
from .webutils import WebUtils
from .webquestion import WebQuestion



class QuestionEndpoints():

    """ Monostate class responsible of handling the discussion web endpoint requests.

    """

    @staticmethod
    def get_questions_answers(auth_service: AuthService, backend_service: BackendService) -> Union[Response, Text]:

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

        name = session['user']
        qid = request.args.get('qid')

        response: ResponseData = backend_service.get_answers(session.get('token'), qid)
        WebUtils.flash_response_messages(response)
        answers = response.get_content().values()
        
        # return render_template('answers.html', name=name, roles=session['roles'], answers=answers)
        return render_template('/questions/answers.html', name=name, roles=session['roles'])

    @staticmethod
    def get_new_question(backend_service: BackendService, auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the POST requests to the question root endpoint.
        Ar
        #gs:
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

        qid = request.form.get('qid')
        title = request.form.get('titleText')
        body = request.form.get('bodyText')


        
        return render_template('new_question.html', name=name, roles=session['roles'],

        	#Añadir el resto de la estructura que metamos en la base de datos

        	qid=qid, body=body, title=title)

    @staticmethod
    def post_new_question(backend_service: BackendService, auth_service: AuthService) -> Union[Response, Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        title = request.form.get('titleText')
        body = request.form.get('bodyText')

        new_question = WebQuestion.new_question(backend_service, title=title, body=body)
        if not new_question:
            return redirect(url_for('get_new_question'))
        redirect_to = request.form['redirect_to']
        if not redirect_to:
            redirect_to = url_for('get_questions')
        return redirect(redirect_to)

    @staticmethod
    def get_new_report_question(backend_service: BackendService, auth_service: AuthService) -> Union[Response, Text]:
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
        qid = request.form.get('qid')
        reason = request.form.get('reason')
        
        return render_template('/questions/new_report_question.html', name=name, roles=session['roles'],
        	#Añadir el resto de la estructura que metamos en la base de datos
        	qid=qid, reason=str(reason))

    @staticmethod
    def post_new_report_question(backend_service: BackendService, auth_service: AuthService) -> Union[Response, Text]:
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.DISCUSSION.name not in session['roles']:
            return redirect(url_for('get_home'))

        qid = request.form.get('qid')
        reason = request.form.get('reason')

        new_question = WebQuestion.new_report_question(backend_service, qid=qid, reason=reason)
        if not new_question:
            return redirect(url_for('get_new_question'))
        redirect_to = request.form['redirect_to']
        if not redirect_to:
            redirect_to = url_for('get_questions')
        return redirect(redirect_to)

        







