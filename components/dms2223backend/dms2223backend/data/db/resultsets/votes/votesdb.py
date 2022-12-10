""" 
Answer reports class module.
"""

from typing import List
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound
#from dms2223backend.data.db.results.vote.voteansdb import VotesAns
#from dms2223backend.data.db.results.vote.votecommdb import VotesComm
from dms2223backend.data.db.results.vote.votedb import Votes




class VotesSet():
    """ Class responsible of table-level answer reports operations.
    """
    

    @staticmethod
    def list_all(session: Session, id: int, type: str) -> List[Votes]:
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
        
        query = session.query(Votes).filter(Votes.id == id)
        return query.all()


