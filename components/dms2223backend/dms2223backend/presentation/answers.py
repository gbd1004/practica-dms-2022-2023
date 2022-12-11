
from http import HTTPStatus
import time
from dms2223backend.data.db import schema
from dms2223backend.data.sentiment import Sentiment
from typing import Dict, List
from flask import current_app

from dms2223backend.service.answerservice import AnswerServices
from dms2223backend.service.commentservice import CommentServices

#---------------------------------------------------#
# POSIBLES OPERACIONES:     (definidas en spec.yml) #
#---------------------------------------------------#

# Answer{qid} GET (lista)
# Recibe como parámetro: QuestionIdPathParam
def get_answers(qid: int) -> tuple[dict, HTTPStatus]:
     with current_app.app_context():
        # Si la pregunta existe, se podrá tratar de obtener sus respuestas
        answers: List[Dict] = get_answers(schema, qid)
        
        # Si existen respuestas a la pregunta, se devolverá la pregunta completa
        if (len(answers ) != 0):
            for a in answers:
                votes = AnswerServices.get_votes(schema, a['aid'])
                comments = get_comments(a['aid'])
                a['user_votes'] = votes
                a['comms'] = comments
            return answers , HTTPStatus.OK
        else:
            return {}, HTTPStatus.NOT_FOUND

# Función auxiliar: completa los comentarios con sus respectivos votos
def get_comments(aid: int) -> List[Dict]:
    with current_app.app_context():
        comments : List[Dict] = CommentServices.get_comments(schema, aid)
        for c in comments:
            c['user_votes'] = CommentServices.get_votes(schema, c['cid'])
        return comments





# Answer POST
# Solo es necesario el cuerpo de la pregunta -> schema AnswerCreationModel
def new_answer(qid:int, body: dict) -> tuple[dict, HTTPStatus]:
    """Creates an answer

	Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the answer data and a code 200 OK.
    """
    with current_app.app_context():
        new_answer: Dict = AnswerServices.create_answer(qid, body, schema) #TODO: current_app.db) ?

        usr_votes: Dict = AnswerServices.get_votes(schema, new_answer['aid'])
        new_answer['user_votes'] = usr_votes

        return new_answer, HTTPStatus.OK

# Answer POST
# Solo es necesario el cuerpo de la pregunta -> schema AnswerCreationModel
def new_comment(aid: int, body: Dict, sentiment: Sentiment) -> tuple[dict, HTTPStatus]:
    """Creates a comment

	Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the comments data and a code 200 OK.
    """
    with current_app.app_context():
        new_comment: Dict = CommentServices.create_comment(aid, body, sentiment, schema) #TODO: current_app.db) ?
        
        usr_votes: Dict = CommentServices.get_votes(schema, new_comment['cid'])
        new_comment['user_votes'] = usr_votes

        return new_comment, HTTPStatus.OK


# Métodos UPDATE para votar respuestas
def vote_answer(aid: int) -> tuple[dict, HTTPStatus]:
    with current_app.app_context():
        voted_answer = {}
        success = AnswerServices.vote_answer(schema, aid)

        if success:
            voted_answer = AnswerServices.get_answer(schema, aid)
            usr_votes: Dict = AnswerServices.get_votes(schema, voted_answer['aid'])
            voted_answer['user_votes'] = usr_votes
            return voted_answer, HTTPStatus.OK
        else:
            return voted_answer, HTTPStatus.CREATED


# Métodos UPDATE para votar comentarios
def vote_comment(cid: int) -> tuple[dict, HTTPStatus]:
    with current_app.app_context():
        voted_comment = {}
        success = CommentServices.vote_comment(schema, cid)

        if success:
            voted_comment = CommentServices.get_comment(schema, cid)
            usr_votes: Dict = CommentServices.get_votes(schema, voted_comment['cid'])
            voted_comment['user_votes'] = usr_votes
            return voted_comment, HTTPStatus.OK
        else:
            return voted_comment, HTTPStatus.CREATED
