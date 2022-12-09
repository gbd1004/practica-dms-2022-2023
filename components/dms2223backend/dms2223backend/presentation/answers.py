from http import HTTPStatus
import time
from dms2223backend.data.sentiment import Sentiment
from typing import Dict
from flask import current_app

#------------------------#
# BASE DE DATOS TEMPORAL #
#------------------------#

# Definido en: AnswerFullModel
ANSWERS_DB = {
    1: {
        'aid': 1,
        'qid': 1, # Foreign Key
        'timestamp': 2665574089,
        'body': 'Soy una respuesta',
        'owner':{
            'username' : 'user2'
        },
        'votes': 4,
        'user_votes' : {
            'user3': True,
            'user4': True,
            'user5': True,
            'user6': True
        },
        'comms': {
            1: {
                'cid':1,
                'aid':1,
                'timestamp':1665575389,
                'body': 'Soy un comentario',
                'sentiment': Sentiment.POSITIVE.name,
                'owner':{'username': 'user4'},
                'votes': 2,
                'user_votes':{
                    'user5': True,
                    'user6': True
                }
            },
            2:{
                'cid':2,
                'aid':1,
                'timestamp':1665575289,
                'body': 'Soy otro comentario',
                'sentiment': Sentiment.POSITIVE.name,
                'owner':{'username': 'user4'},
                'votes': 1,
                'user_votes':{
                    'user6': True
                }
            }
        }
    },
    2: {
        'aid': 2,
        'qid': 1, # Foreign Key
        'timestamp': 3665574089,
        'body': 'Soy otra respuesta',
        'owner':{
            'username' : 'user1'
        },
        'votes': 4,
        'user_votes' : {
            'user3': True,
            'user4': True,
            'user5': True,
            'user6': True
        },
        'comms': {
            1:{
                'cid':3,
                'aid':1,
                'timestamp': 1665575289,
                'body': 'Soy otro comentario',
                'sentiment': Sentiment.POSITIVE.name,
                'owner':{'username': 'user4'},
                'votes': 1,
                'user_votes':{
                    'user6': True
                }
            }
        }
    }
}




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
