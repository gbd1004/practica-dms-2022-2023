from http import HTTPStatus
import time

#------------------------#
# BASE DE DATOS TEMPORAL #
#------------------------#

# Definido en: AnswerFullModel
ANSWERS_DB = {
	1: {
        #'id' : 1, ¿necesario?
        'qid': 1, # Foreign Key
        'timestamp': 2665574089.0,
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
        }
        # TO DO -> comments:{}
    },

	2: {
        #'id' : 2, ¿necesario?
        'qid': 1, # Foreign Key
        'timestamp': 3665574089.0,
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
        }
        # TO DO -> comments:{}
		}	
}



#---------------------------------------------------#
# POSIBLES OPERACIONES:     (definidas en spec.yml) #
#---------------------------------------------------#


# Answer{qid} GET (lista)
# Recibe como parámetro: QuestionIdPathParam
def get_answers(qid: int):
	# Si la prgunta existe, se podrá tratar de obtener sus respuestas
    lista = []
    for a in ANSWERS_DB:
        if ANSWERS_DB[a]['qid'] == qid:
            lista.append({a:ANSWERS_DB[a]})
    # Si existen respuestas a la pregunta, se devollverá la pregunta completa
    if (len(lista) != 0):
        return lista, HTTPStatus.OK
    else:
        return f"No existe una pregunta con identificador {qid}.", HTTPStatus.NOT_FOUND



# Answer POST
# Solo es necesario el cuerpo de la pregunta -> schema AnswerCreationModel
def new_answer(qid:int, body:any):
    for a in ANSWERS_DB:
        if ANSWERS_DB[a]['qid'] == qid:
            lista = []
            new_id = len(ANSWERS_DB) + 1 # aid = last_aid + 1
            lista.append({'qid':qid}) # qid
            lista.append({'timestamp':time.time()}) # current timestamp
            lista.append({'body':body}) # body
            #lista.append({'owner': {'username': TO DO}}) # owner
            lista.append({'votes':0}) # votes (0 por defecto)
            lista.append({'user_votes':[]}) # vacía
            #lista.append({'coments': TO DO})
            ANSWERS_DB[new_id] = lista
            return ANSWERS_DB.get(new_id), HTTPStatus.CREATED
    return f"No existe una pregunta con identificador {qid}.", HTTPStatus.NOT_FOUND

	# NOTA: 
	# ¡Falta obtener usuario propietario! -> schema UserCoreModel: {'username' : string}
	# Revisar user_token[] para obtenerlo 



'''REEPORTS'''
# Report POST
def new_report(qid: int):
	pass 

# Report GET (list)
def get_reports():
	pass

# Report{rid} POST
def set_report_status(rid: int):
	pass