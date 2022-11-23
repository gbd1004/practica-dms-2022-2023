""" Users class module.
"""

import hashlib
from typing import List
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2223backend.data.db.results.questiondb import Question




class Questions():
    """ Class responsible of table-level users operations.
    """
    @staticmethod
    def create(session: Session, title: str, body: str) -> Question:
        """ Creates a new question record.

        Note:
            Any existing transaction will be committed.

        Args:
            - session (Session): The session object.
            - title (str): The question's title.
            - body (str): The question's body.

        Raises:
            - ValueError: If the title is empty.
            - QuestionExistsError: If a user with the same username already exists.

        Returns:
            - Question: The created `Question` result.
        """
        if not title :
            raise ValueError('El título es un campo obligatorio para crear una pregunta.')

        new_question = Question(title, body)
        session.add(new_question)
        session.commit()
        return new_question


    @staticmethod
    def list_all(session: Session) -> List[Question]:
        """Lists every question.

        Args:
            - session (Session): The session object.

        Returns:
            - List[Question]: A list of `Question` registers.
        """
        
        query = session.query(Question.title, Question.timestamp, Question.owner)
        return query.all()

