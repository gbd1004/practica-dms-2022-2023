"""
Answer reports class module.
"""
from typing import List
from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db.results.vote.voteansdb import VotesAns

class VotesA():
    """ Class responsible of table-level answer reports operations.
    """

    @staticmethod
    def list_all_ans(session: Session, id: int) -> List[VotesAns]:
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

        query = session.query(VotesAns).filter(VotesAns.aid == id)
        return query.all()

