""" 
QuestionServices class module.
"""

from ast import Dict
from typing import List
from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db.resultsets.questionsdb import Questions
from dms2223backend.data.db.schema import Schema
from dms2223backend.data.db.results.questiondb import Question


class QuestionServices():
    """ 
    Monostate class that provides high-level services to handle Questions' use cases.
    """

    @staticmethod
    def get_questions(schema: Schema) -> List[Dict]:
        """Lists the existing questions.

        Args:
            - schema (Schema): A database handler where the questions are mapped into.

        Returns:
            - List[Dict]: A list of dictionaries with the questions' data.
        """
        out: List[Dict] = []
        session: Session = schema.new_session()
        questions: List[Question] = Questions.list_all(session)
        for q in questions:
            if q.hidden == False:
                out.append({
                    'qid': q.qid,
                    'title': q.title,
                    'timestamp': q.timestamp
                })
        schema.remove_session()
        return out

    @staticmethod
    def get_question(schema: Schema, qid: int) -> Dict:
        """Gets the question with the same parameter qid.

        Args:
            - qid (int): The question's qid.
            - schema (Schema): A database handler where the users are mapped into.
        
        Returns:
            - Dict: A dictionary with the question's data.        
        """
        session: Session = schema.new_session()
        question: Question = Questions.get_question(session,qid)
        out: Dict = {}
        out['qid'] = {
                    'qid': question.qid,
                    'title': question.title,
                    'body': question.body,
                    'timestamp': question.timestamp,
                    'owner': {'username': question.owner}
        }
        schema.remove_session()
        return out


    @staticmethod
    def create_question(title: str, body: str,schema: Schema) -> Dict:
        """Creates a new question.

        Args:
            - title (str): The new question's title.
            - body (str): The new question's body.
            - schema (Schema): A database handler where the users are mapped into.

        Raises:
            - ValueError: If either the username or the password_hash is empty.
            - UserExistsError: If a user with the same username already exists.

        Returns:
            - Dict: A dictionary with the new question's data.
        """

        session: Session = schema.new_session()
        out: Dict = {}
        try:
            new_question: Question = Question.create(session, title, body)
            out['qid'] = {
                    'qid': new_question.qid,
                    'title': new_question.title,
                    'body': new_question.body,
                    'timestamp': new_question.timestamp,
                    'owner': {'username': new_question.owner}
            }
            
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out
