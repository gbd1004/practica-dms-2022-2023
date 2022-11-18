""" DiscussionEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template, request
from werkzeug.wrappers import Response
from dms2223common.data import Role
from dms2223frontend.data.rest.authservice import AuthService
# Se importan del backend las preguntas
# from dms2223backend.presentation import questionsdb
from dms2223frontend.data.rest.backendservice import BackendService
from .webauth import WebAuth






class DiscussionEndpoints():
    """ Monostate class responsible of handling the discussion web endpoint requests.
    """
    @staticmethod
    def get_discussion(backend_service: BackendService, auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the GET requests to the discussion root endpoint.
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
        return render_template('discussion.html', name=name, roles=session['roles'], questions=backend_service.get_questions(session.get('token')))
    
    @staticmethod
    def new_discussion(backend_service: BackendService, auth_service: AuthService) -> Union[Response, Text]:
        """ Handles the POST requests to discussion root endpoint.
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
        title = request.form.get('title')
        body = request.form.get('body')
        entrada = {{'title':title},{'body':body}}
        # Devolvemos la entrada en forma de JSON para la base de datos temportal
        # return render_template('discussion.html', name=name, roles=session['roles'],questions=questionsdb.QuestionsDB().new_question(entrada))
        return render_template('discussion.html', name=name, roles=session['roles'], questions=backend_service.new_question(session.get('token'), title, body))
        # NOTA: ¿Añadir un redirect a /discussions?

        


        
        
        
        
        