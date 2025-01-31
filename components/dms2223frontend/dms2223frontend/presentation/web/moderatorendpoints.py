""" ModeratorEndpoints class module.
"""

from typing import Text, Union
from flask import redirect, url_for, session, render_template, request, current_app
from werkzeug.wrappers import Response
from .webauth import WebAuth
from .webutils import WebUtils
from dms2223common.data import Role
from dms2223frontend.data.rest.authservice import AuthService
from dms2223frontend.data.rest.backendservice import BackendService
from dms2223common.data.rest import ResponseData


class ModeratorEndpoints():
    """ Monostate class responsible of handing the moderator web endpoint requests.
    """
    @staticmethod
    def get_moderator(
        backend_service:BackendService,auth_service:AuthService
    ) -> Union[Response,Text]:
        """ Handles the GET requests to the moderator root endpoint.

        Args:
            - auth_service (AuthService): The authentication service.

        Returns:
            - Union[Response,Text]: The generated response to the request.
        """
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.MODERATION.name not in session['roles']:
            return redirect(url_for('get_home'))

        name = session['user']
        response_qr: ResponseData = backend_service.get_questions_reports(session.get('token'))
        WebUtils.flash_response_messages(response_qr)
        question_reports = response_qr.get_content()

        response_ar: ResponseData = backend_service.get_answers_reports(session.get('token'))
        WebUtils.flash_response_messages(response_ar)
        answer_reports = response_ar.get_content()

        response_cr: ResponseData = backend_service.get_comments_reports(session.get('token'))
        WebUtils.flash_response_messages(response_cr)
        comment_reports = response_cr.get_content()

        current_app.logger.info(question_reports)
        current_app.logger.info(answer_reports)
        current_app.logger.info(comment_reports)

        return render_template('moderator.html', name=name, roles=session['roles'],
            question_reports=question_reports, answer_reports=answer_reports,
            comment_reports=comment_reports)

    @staticmethod
    def put_accept_question_report(backend_service: BackendService, auth_service: AuthService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.MODERATION.name not in session['roles']:
            return redirect(url_for('get_home'))

        qrid = request.form.get('qrid')
        response: ResponseData = backend_service.put_question_report(session.get('token'),
            qrid=qrid , status="ACCEPTED")
        WebUtils.flash_response_messages(response)

        return redirect("/moderator")

    @staticmethod
    def put_deny_question_report(backend_service: BackendService, auth_service: AuthService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.MODERATION.name not in session['roles']:
            return redirect(url_for('get_home'))

        qrid = request.form.get('qrid')
        response: ResponseData = backend_service.put_question_report(session.get('token'),
            qrid=qrid , status="REJECTED")
        WebUtils.flash_response_messages(response)

        return redirect("/moderator")

    @staticmethod
    def put_accept_answer_report(backend_service: BackendService, auth_service: AuthService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.MODERATION.name not in session['roles']:
            return redirect(url_for('get_home'))

        arid = request.form.get('arid')
        response: ResponseData = backend_service.put_answer_report(session.get('token'),
            arid=arid , status="ACCEPTED")
        WebUtils.flash_response_messages(response)

        return redirect("/moderator")

    @staticmethod
    def put_deny_answer_report(backend_service: BackendService, auth_service: AuthService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.MODERATION.name not in session['roles']:
            return redirect(url_for('get_home'))

        arid = request.form.get('arid')
        response: ResponseData = backend_service.put_answer_report(session.get('token'),
            arid=arid , status="REJECTED")
        WebUtils.flash_response_messages(response)

        return redirect("/moderator")

    @staticmethod
    def put_accept_comment_report(backend_service: BackendService, auth_service: AuthService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.MODERATION.name not in session['roles']:
            return redirect(url_for('get_home'))

        crid = request.form.get('crid')
        response: ResponseData = backend_service.put_comment_report(session.get('token'),
            crid=crid , status="ACCEPTED")
        WebUtils.flash_response_messages(response)

        return redirect("/moderator")

    @staticmethod
    def put_deny_comment_report(backend_service: BackendService, auth_service: AuthService):
        if not WebAuth.test_token(auth_service):
            return redirect(url_for('get_login'))
        if Role.MODERATION.name not in session['roles']:
            return redirect(url_for('get_home'))

        crid = request.form.get('crid')
        response: ResponseData = backend_service.put_comment_report(session.get('token'),
            crid=crid , status="REJECTED")
        WebUtils.flash_response_messages(response)

        return redirect("/moderator")
