""" 
ReportServices class module.
"""

from ast import Dict
from typing import List
from sqlalchemy.orm.session import Session
from dms2223backend.data.db.results.vote.votedb import Votes  # type: ignore
from dms2223backend.data.db.resultsets.commentsdb import Comments
from dms2223backend.data.db.resultsets.votes.votesdb import VotesSet
from dms2223backend.data.db.results.vote.votedb import Votes
from dms2223backend.data.db.schema import Schema
from dms2223backend.data.db.results.commentdb import Comment


class ReportServices():
    """ 
    Monostate class that provides high-level services to handle Reports' use cases.
    """

    @staticmethod
    def get_reports(schema: Schema, aid:int) -> List[Dict]:
        """Lists the existing reports.

        Args:
            - schema (Schema): A database handler where the comments are mapped into.

        Returns:
            - List[Dict]: A list of dictionaries with the comments' data.
        """
        out: List[Dict] = []
        session: Session = schema.new_session()
        comments: List[Comment] = Comments.list_all(session,aid)
        for c in comments:
            if c.hidden == False:
                out.append({
                    'cid': c.id,
                    'aid': c.aid,
                    'timestamp': c.timestamp,
                    'body' : c.body,
                    'sentiment': c.sentiment,
                    'owner': {'username': c.owner},
                    'votes': c.get_num_votes(session)
                })
        schema.remove_session()
        return out




    @staticmethod
    def create_reeport( body: str, sentiment: enumerate, schema: Schema) -> Dict:
        """Creates a new report.

        Args:
            - body (str): The comment's body.
            - aid (int): The answer's aid.
            - sentiment (str): The comment sentiment.

        Returns:
            - Dict: A dictionary with the new comment's data.
        """

        session: Session = schema.new_session()
        out: Dict = {}
        try:
            new_comment: Comment = Comments.create(session, body, sentiment)
            out['aid'] = {
                    'cid': new_comment.id,
                    'aid': new_comment.aid,
                    'timestamp': new_comment.timestamp,
                    'body' : new_comment.body,
                    'sentiment': new_comment.sentiment,
                    'owner': {'username': new_comment.owner},
                    'votes': new_comment.get_num_votes(session)
            }
            
        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out



   