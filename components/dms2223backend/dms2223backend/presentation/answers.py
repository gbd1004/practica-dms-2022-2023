
from http import HTTPStatus
from typing import Dict, List, Tuple, Union
from flask import current_app

from dms2223backend.logic.answerservice import AnswerServices
from dms2223backend.logic.commentservice import CommentServices

#---------------------------------------------------#
# POSIBLES OPERACIONES:     (definidas en spec.yml) #
#---------------------------------------------------#

# Answer{qid} GET (lista)
# Recibe como parámetro: QuestionIdPathParam
def get_answers(qid: int) -> Tuple[list, int]:
    with current_app.app_context():
        # Si la pregunta existe, se podrá tratar de obtener sus respuestas
        answers: List = AnswerServices.get_answers(current_app.db, qid)

        # Si existen respuestas a la pregunta, se devolverá la pregunta completa
        if len(answers ) != 0:
            for ans in answers:
                votes = AnswerServices.get_votes(current_app.db, ans['aid'])
                comments = get_comments(ans['aid'])
                ans['user_votes'] = votes
                ans['comms'] = comments
            return answers , HTTPStatus.OK
        return [], HTTPStatus.NOT_FOUND

# Función auxiliar: completa los comentarios con sus respectivos votos
def get_comments(aid: int) -> List[Dict]:
    with current_app.app_context():
        comments : List[Dict] = CommentServices.get_comments(current_app.db, aid)
        for comment in comments:
            comment['user_votes'] = CommentServices.get_votes(current_app.db, comment['cid'])
        return comments

# Answer POST
# Solo es necesario el cuerpo de la pregunta -> current_app.db AnswerCreationModel
def new_answer(qid:int, body: dict, token_info: Dict) -> Tuple[Union[Dict, str], int]:
    """Creates an answer

	Returns:
        - Tuple[Dict, HTTPStatus]: A Tuple with a dictionary of the answer data and a code 200 OK.
    """
    if body['body'] == "":
        return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)

    with current_app.app_context():
        owner = token_info['user_token']['username']
        new_answ = AnswerServices.create_answer(qid, body['body'], owner, current_app.db)

        usr_votes: Dict = AnswerServices.get_votes(current_app.db, new_answ['aid'])
        new_answ['user_votes'] = usr_votes

        return new_answ, HTTPStatus.OK

# Answer POST
# Solo es necesario el cuerpo de la pregunta -> current_app.db AnswerCreationModel
def new_comment(aid: int, body: Dict, token_info: Dict) -> Tuple[Union[Dict, str], int]:
    """Creates a comment

	Returns:
        - Tuple[Dict, HTTPStatus]: A Tuple with a dictionary of the comments data and a code 200 OK.
    """
    if body['body'] == "":
        return ('A mandatory argument is missing', HTTPStatus.BAD_REQUEST.value)

    with current_app.app_context():
        owner = token_info['user_token']['username']
        new_comm: Dict = CommentServices.create_comment(
            aid, body['body'], body['sentiment'], owner, current_app.db
        )

        usr_votes: Dict = CommentServices.get_votes(current_app.db, new_comm['cid'])
        new_comm['user_votes'] = usr_votes

        return new_comm, HTTPStatus.OK

# Métodos UPDATE para votar respuestas
def vote_answer(aid: int) -> Tuple[dict, int]:
    """Votes an answer

	Returns:
        - Tuple[Dict, HTTPStatus]: A Tuple with a dictionary of the comments data and a code.
    """
    with current_app.app_context():
        voted_answer = {}
        success = AnswerServices.vote_answer(current_app.db, aid)

        if success:
            voted_answer = AnswerServices.get_answer(current_app.db, aid)
            usr_votes: Dict = AnswerServices.get_votes(current_app.db, voted_answer['aid'])
            voted_answer['user_votes'] = usr_votes
            return voted_answer, HTTPStatus.OK
        return voted_answer, HTTPStatus.CREATED


# Métodos UPDATE para votar comentarios
def vote_comment(cid: int) -> Tuple[dict, int]:
    """Votes a comment

	Returns:
        - Tuple[Dict, HTTPStatus]: A Tuple with a dictionary of the comments data and a code.
    """
    with current_app.app_context():
        voted_comment = {}
        success = CommentServices.vote_comment(current_app.db, cid)

        if success:
            voted_comment = CommentServices.get_comment(current_app.db, cid)
            usr_votes: Dict = CommentServices.get_votes(current_app.db, voted_comment['cid'])
            voted_comment['user_votes'] = usr_votes
            return voted_comment, HTTPStatus.OK
        return voted_comment, HTTPStatus.CREATED
