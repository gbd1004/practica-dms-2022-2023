"""
Answer reports class module.
"""
from typing import List
from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db.results.vote.votecommdb import VotesComm

class VotesC():
    """ Class responsible of table-level answer reports operations.
    """


    @staticmethod
    def list_all_comm(session: Session, id: int )-> List[VotesComm]:
        """Lists every answer report.

        Args:
            - session (Session): The session object.
            - id (int) : A integer with the identifier of the answer or comment.
            - type (str) : A string with the type (answer or comment).

        Returns:
            - List[Votes]: A list of `Votes` registers.

        Alternativa:
            if type == "voteanswer":
                query = session.query(VotesAns).filter(VotesAns.id == id)
            else:
                query = session.query(VotesComm).filter(VotesComm.id == id)
         """

        query = session.query(VotesComm).filter(VotesComm.cid == id)
        return query.all()
