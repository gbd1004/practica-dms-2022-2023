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
    def create(session: Session, qid:int, body: str) -> Answer:
        """ Creates a new answer record.

        Note:
            Any existing transaction will be committed.

        Args:
            - session (Session): The session object.
            - body (str): The answer's body.
            - qid (int): The question's qid.

        Returns:
            - Answer: The created `Answer` result.
        """

        new_answer = Answer(qid, body)

        
        session.add(new_answer)
        session.commit()
        return new_answer

    @staticmethod
    def get_answer(session: Session, aid:int) -> Answer:
        """Gets a particular answer.

        Args:
            - session (Session): The session object.
            - aid (int): The answer's id

        Returns:
            - Answer: Expected `Answer` register.
        """
        
        query = session.query(Answer).where(Answer.aid == aid)
        return query

    @staticmethod
    def list_all(session: Session, qid:int) -> List[Answer]:
        """Lists every answer.

        Args:
            - session (Session): The session object.
            - qid (int): The question's qid.

        Returns:
            - List[Answer]: A list of `Answer` registers.
        """
        
        query = session.query(Answer).filter(Answer.qid == qid)
        return query.all()


