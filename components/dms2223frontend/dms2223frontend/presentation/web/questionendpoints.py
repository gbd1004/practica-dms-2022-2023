""" DiscussionEndpoints class module.

"""



from typing import Text, Union
from flask import redirect, url_for, session, render_template, request
from werkzeug.wrappers import Response
from dms2223common.data import Role
from dms2223frontend.data.rest.authservice import AuthService
# Se importan del backend las preguntas
from dms2223backend.presentation import questionsdb
from .webauth import WebAuth
from dms2223frontend.data.rest.backendservice import BackendService
from dms2223common.data.rest import ResponseData
from .webutils import WebUtils



class QuestionEndpoints():

    """ Monostate class responsible of handling the discussion web endpoint requests.

    """

    @staticmethod

    def get_answers(auth_service: AuthService, backend_service: BackendService) -> Union[Response, Text]:

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
        qid = request.get('qid')

        response: ResponseData = backend_service.get_answers(session.get('token'), qid)
        WebUtils.flash_response_messages(response)
        answers = response.get_content().values()
        
        # return render_template('answers.html', name=name, roles=session['roles'], answers=answers)
        return render_template('answers.html', name=name, roles=session['roles'])

    @staticmethod

    def new_question(auth_service: AuthService) -> Union[Response, Text]:
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

        content = request.form.get('content')

        
        return render_template('questions.html', name=name, roles=session['roles'],

        	#Añadir el resto de la estructura que metamos en la base de datos

        	qid=int(qid), content=content)

        







