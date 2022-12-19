from typing import List, Tuple, Dict, Union
from http import HTTPStatus
from flask import current_app
from dms2223backend.logic.questionservice import QuestionServices

class QuestionsDB():

    # Constructor
    def __init__(self) -> None:
        pass

    #---------------------------------------------------#
    # POSIBLES OPERACIONES:     (definidas en spec.yml) #
    #---------------------------------------------------#

# Question GET (list)
def get_questions() -> Tuple[List, HTTPStatus]:
    """Lists the existing questions.

    Returns:
        - Tuple[Dict, HTTPStatus]: A Tuple with a dictionary of the questions'
            data and a code 200 OK.
    """
    with current_app.app_context():
        # Array de objetos: schema QuestionCoreModel
        diccionario = QuestionServices.get_questions(current_app.db)

        # Se devuelve la dicccionario
        return diccionario, HTTPStatus.OK

# Question{qid} GET
# Recibe como parámetro: QuestionIdPathParam
def get_question(qid: int) -> Tuple[dict, HTTPStatus]:
    """Gets an existing question with parameter qid.

    Returns:
        - Tuple[Dict, HTTPStatus]: A Tuple with a dictionary of the question data and a code 200.
    """
    with current_app.app_context():
        pregunta = QuestionServices.get_question(current_app.db, qid)
        if len(pregunta) != 0:
            return pregunta, HTTPStatus.OK
        # Si no existe, no se puede devolver
        return {}, HTTPStatus.NOT_FOUND



# Question POST
def new_question(body: dict, token_info: dict) -> Tuple[Union[Dict, str], HTTPStatus]:
    """Creates a question

    Returns:
        - Tuple[Dict, HTTPStatus]: A Tuple with a dictionary of the question data and a code 200.
    """
    if body['title'] == "":
        return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)

    with current_app.app_context():
        owner = token_info['user_token']['username']
        new_question = QuestionServices.create_question(
            body['title'], body['body'], owner, current_app.db
        )
        return new_question, HTTPStatus.OK
