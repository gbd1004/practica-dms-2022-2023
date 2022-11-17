"""QuestionsDB class module
"""

from http import HTTPStatus

class QuestionsDB():

	QUESTIONS_DB = {
		1: {
			'qid': 1,
			'name': 'Pregunta1',
			'answers': {
				1: {
				'aid': 1,
				'name': 'Respuesta1',
				'content':'Soy una respuesta'        	
				},
				2: {
				'aid': 2,
				'name': 'Respuesta2',
				'content':'Soy una respuesta'        	
				}
			}
		},

		2: {
			'qid': 2,
			'name': 'Pregunta2',
			'answers': {
				1: {
				'aid': 1,
				'name': 'Respuesta1',
				'content':'Soy una respuesta'        	
				},
				2: {
				'aid': 2,
				'name': 'Respuesta2',
				'content':'Soy una respuesta'        	
				}
			}
		}
	}

	def __init__(self) -> None:
		pass

	def get_questions(self):
		# Array de objetos con nombre e id
		return {'questions': list(self.QUESTIONS_DB.values())}, HTTPStatus.OK

		
	# def new_question():
	# 	if body['qid'] in QUESTIONS_DB:
	# 		return f"Ya existe una pregunta con id {body['qid']}.", HTTPStatus.CONFLICT
	# 	    QUESTIONS_DB[body['qid']] = body
	# 	    return QUESTIONS_DB.get(body['qid']), HTTPStatus.CREATED
			
	# def get_question(qid: int):
	#     if qid in QUESTIONS_DB:
	#         return QUESTIONS_DB.get(qid), HTTPStatus.OK
	#     return '', HTTPStatus.NOT_FOUND



	# def get_answers(qid):
	# 	if qid in QUESTIONS_DB:
	# 		return QUESTIONS_DB.get(qid).answers.get(aid), HTTPStatus.OK
	# 	    return '', HTTPStatus.NOT_FOUND

			
	# def new_answer():
	# 	pass 
		
	# def new_report(qid):
	# 	pass 

	# def get_reports():
		
	#     list=[]
	#     return list
		
	# def set_report_status(qrid):
	# 	pass