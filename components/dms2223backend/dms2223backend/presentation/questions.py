from ast import Dict
from http import HTTPStatus
from flask import current_app
from dms2223backend.service.questionservice import QuestionServices

class QuestionsDB():

	# Constructor
	def __init__(self) -> None:
		pass

	#---------------------------------------------------#
	# POSIBLES OPERACIONES:     (definidas en spec.yml) #
	#---------------------------------------------------#

# Question GET (list)
def get_questions() -> tuple[dict, HTTPStatus]:
	"""Lists the existing questions.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the questions' data and a code 200 OK.
    """
	with current_app.app_context():
		# Array de objetos: schema QuestionCoreModel
		diccionario: Dict = QuestionServices.get_questions(current_app.db)
		current_app.logger.info(diccionario)
	
		# Se devuelve la dicccionario
		return diccionario, HTTPStatus.OK


# Question{qid} GET
# Recibe como parámetro: QuestionIdPathParam
def get_question(qid: int) -> tuple[list, HTTPStatus]:
	"""Gets an existing question with parameter qid.

    Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the question data and a code 200 OK.
    """
	with current_app.app_context():
		pregunta: Dict = QuestionServices.get_question(current_app.db, qid)
		if len(pregunta) != 0:
			return pregunta, HTTPStatus.OK
		# Si no existe, no se puede devolver
		return [], HTTPStatus.NOT_FOUND



# Question POST
def new_question(body: Dict, token_info: Dict) -> tuple[dict, HTTPStatus]:
	"""Creates a question

	Returns:
        - Tuple[Dict, HTTPStatus]: A tuple with a dictionary of the question data and a code 200 OK.
    """
	with current_app.app_context():
		owner = token_info['user_token']['username']
		new_question: Dict = QuestionServices.create_question(body['title'], body['body'], owner, current_app.db)
		return new_question, HTTPStatus.OK



