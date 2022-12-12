"""
Questions class module.
"""

from typing import List
from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db.results.questiondb import Question

class Questions():
    """ Class responsible of table-level questions operations.
    """
    @staticmethod
    def create(session: Session, title: str, body: str, owner: str) -> Question:
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

        new_question = Question(title, body, hidden=False, owner=owner)
        session.add(new_question)
        session.commit()
        return new_question

    @staticmethod
    def get_question(session: Session, qid:int) -> Question:
        """Gets a particular question.

        Args:
            - session (Session): The session object.
            - qid (int): The question's qid

        Returns:
            - Question: Expected `Question` register.
        """

        query = session.query(Question).where(Question.qid == qid)
        return query.first()

    @staticmethod
    def list_all(session: Session) -> List[Question]:
        """Lists every question.

        Args:
            - session (Session): The session object.

        Returns:
            - List[Question]: A list of `Question` registers.
        """

        query = session.query(Question)
        return query.all()
