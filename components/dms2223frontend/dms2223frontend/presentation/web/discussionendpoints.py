""" DiscussionEndpoints class module.

"""



from typing import Text, Union

from flask import redirect, url_for, session, render_template, request

from werkzeug.wrappers import Response

from dms2223common.data import Role

from dms2223frontend.data.rest.authservice import AuthService

from .webauth import WebAuth









class DiscussionEndpoints():

    """ Monostate class responsible of handling the discussion web endpoint requests.

    """

    @staticmethod

    def get_discussion(auth_service: AuthService) -> Union[Response, Text]:

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

        return render_template('discussion.html', name=name, roles=session['roles'])

    

    @staticmethod

    def new_discussion(auth_service: AuthService) -> Union[Response, Text]:

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

        did = request.form.get('did')

        content = request.form.get('content')

        

        return render_template('discussion.html', name=name, roles=session['roles'],

        	#Añadir el resto de la estructura que metamos en la base de datos

        	did=int(did), content=content)

        

        # NOTA: ¿Añadir un redirect a /discussions?

        





        

        

        

        

        