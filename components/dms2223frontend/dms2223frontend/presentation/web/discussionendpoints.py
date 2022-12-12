""" DiscussionEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template
from werkzeug.wrappers import Response
from .webauth import WebAuth
from .webutils import WebUtils
from flask import current_app
from dms2223common.data import Role
from dms2223frontend.data.rest.authservice import AuthService
from dms2223frontend.data.rest.backendservice import BackendService
from dms2223common.data.rest import ResponseData

class DiscussionEndpoints():
    """ Monostate class responsible of handling the discussion web endpoint requests.
    """
    @staticmethod
    def get_discussion(
        backend_service: BackendService, auth_service: AuthService
    ) -> Union[Response, Text]:
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
        response: ResponseData = backend_service.get_questions(session.get('token'))
        current_app.logger.info(response.get_content())
        WebUtils.flash_response_messages(response)
        questions = response.get_content()
        return render_template('discussion.html', name=name, roles=session['roles'],
            questions=questions)
