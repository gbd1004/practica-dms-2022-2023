"""
Answers class module.
"""

from typing import List
from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db.results.answerdb import Answer
from dms2223backend.data.db.results.vote.voteansdb import VotesAns

class Answers():
    """ Class responsible of table-level answers operations.
    """
    @staticmethod
    def create(session: Session, qid:int, body: str, owner: str) -> Answer:
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

        new_answer = Answer(qid, body, hidden=False ,owner=owner)

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
        return query.first()

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


    # Método con el que posteriormente se puede actualizar el número de votos
    @staticmethod
    def get_num_votes(session: Session, aid: int) -> int:
        num_votes = session.query(VotesAns).where(VotesAns.aid == aid).count()
        return num_votes
