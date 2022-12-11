from http import HTTPStatus
import time
from dms2223backend.data.sentiment import Sentiment
from typing import Dict
from flask import current_app


#---------------------------------------------------#
# POSIBLES OPERACIONES:     (definidas en spec.yml) #
#---------------------------------------------------#

# Answer{qid} GET (lista)
# Recibe como parámetro: QuestionIdPathParam
def get_answers(qid: int) -> tuple[dict, HTTPStatus]:
    # Si la pregunta existe, se podrá tratar de obtener sus respuestas
    lista = {}
    for a in ANSWERS_DB:
        if ANSWERS_DB[a]['qid'] == qid:
            lista[a]=ANSWERS_DB[a]
    # Si existen respuestas a la pregunta, se devolverá la pregunta completa
    if (len(lista) != 0):
        return lista, HTTPStatus.OK
    else:
        return {}, HTTPStatus.NOT_FOUND



# Answer POST
# Solo es necesario el cuerpo de la pregunta -> schema AnswerCreationModel
def new_answer(qid:int, body: dict) -> tuple[dict, HTTPStatus]:
    return {"TEMPORAL":1}, HTTPStatus.OK

# TODO
def vote_answer(aid: int, body: dict) -> tuple[dict, HTTPStatus]:
    return {"TEMPORAL":1}, HTTPStatus.OK

# TODO
def vote_comment(cid: int) -> tuple[dict, HTTPStatus]:
    return {"TEMPORAL":1}, HTTPStatus.OK

# TODO
def new_comment(aid: int, body: Dict) -> tuple[dict, HTTPStatus]:
    return {"TEMPORAL":1}, HTTPStatus.OK
