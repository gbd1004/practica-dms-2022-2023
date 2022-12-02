""" 
Answers class module.
"""

import hashlib
from typing import List
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2223backend.data.db.results.answerdb import Answer
from dms2223backend.data.db.resultsets.questionsdb import Questions




class Answers():
    """ Class responsible of table-level answers operations.
    """
    @staticmethod
    def create(session: Session, body: str) -> Answer:
        """ Creates a new answer record.

        Note:
            Any existing transaction will be committed.

        Args:
            - session (Session): The session object.
            - body (str): The answer's body.

        Raises:
            - ValueError: If the title is empty.
            - QuestionNotFound: If the referenced question do not exists.

        Returns:
            - Answer: The created `Answer` result.
        """

        new_answer = Answer(session, body)

        # TODO: no creo que con list_all no valga
        if not new_answer.qid in Questions.list_all():
            raise ValueError('No existe una pregunta con ese identificador')
        
        session.add(new_answer)
        session.commit()
        return new_answer


    @staticmethod
    def list_all(session: Session) -> List[Answer]:
        """Lists every answer.

        Args:
            - session (Session): The session object.

        Returns:
            - List[Answer]: A list of `Answer` registers.
        """
        
        query = session.query(Answer)
        return query.all()


