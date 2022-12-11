""" 
CommentServices class module.
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
from dms2223backend.data.sentiment import Sentiment


class CommentServices():
    """ 
    Monostate class that provides high-level services to handle Comments' use cases.
    """

    @staticmethod
    def get_comments(schema: Schema, aid:int) -> List[Dict]:
        """Lists the existing comments.

        Args:
            - schema (Schema): A database handler where the comments are mapped into.

        Returns:
            - List[Dict]: A list of dictionaries with the comments' data.
        """
        out: List[Dict] = []
        session: Session = schema.new_session()
        comments: List[Comment] = Comments.list_all(session)
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
    def get_comment(schema: Schema, cid:int) -> Dict:
        """Gets the comment with the same parameter cid.

        Args:
            - cid (int): The comment cid.
            - schema (Schema): A database handler where the comment are mapped into.

        Returns:
            - Dict: A dictionary with the comment's data.
        """
        out: Dict = {}
        session: Session = schema.new_session()
        comment: Comment = Comments.get_comment(session, cid)
        if comment.hidden == False:
            out['cid'] = {
                    'cid': comment.id,
                    'aid': comment.aid,
                    'timestamp': comment.timestamp,
                    'body' : comment.body,
                    'sentiment': comment.sentiment,
                    'owner': {'username': comment.owner},
                    'votes': comment.get_num_votes(session)
            }

        schema.remove_session()
        return out



    @staticmethod
    def get_votes(schema: Schema, cid:int) -> Dict:
        """Lists the existing comment's votes.

        Args:
            - schema (Schema): A database handler where the comment are mapped into.
            - cid (int): Comment identifier

        Returns:
            - Dict: A dictionary with the votes' data.
        """
        out: Dict = {}
        votes: List = [Votes]
        session: Session = schema.new_session()
        comment: Comment = Comments.get_comment(session,cid)
        if comment.hidden == False:
            votes: VotesSet.list_all(session, "votecomment", cid)
            for v in votes:
                #TODO: revisar
                out[v.user] = True
        schema.remove_session()
        return out

    @staticmethod
    def create_comment( aid:int, body: str, sentiment: Sentiment, owner: str, schema: Schema) -> Dict:
        """Creates a new comment.

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
            new_comment: Comment = Comments.create(session, aid, body, sentiment, owner)
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


    @staticmethod
    def hide_comment(schema: Schema, id: int):
        """Hides the comment with the same parameter id.

        Args:
            - id (int): The comment's id.
            - schema (Schema): A database handler where the comments are mapped into.
        
        """
        session: Session = schema.new_session()
        
        comment: Comment = Comments.get_comment(session,id)
        comment.hidden = True

        # Actualizamos el comentario
        session.add(comment)
        session.commit()

        schema.remove_session()
    
    @staticmethod
    def vote_comment(schema: Schema, id: int) -> bool:
        """Add a vote to the answer with the same parameter aid of the answer.

        Args:
            - id (int): The comment's id.
            - schema (Schema): A database handler where the comment are mapped into.
        
        """
        session: Session = schema.new_session()
        
        # Se guarda el número inicial de votos para comprobar que la operación es exitosa
        comment: Comment = Comments.get_comment(session,id)
        prev_vote = comment.get_num_votes(session)

        # Se añade el nuevo voto
        new_vote: Votes = Votes(id, "votecomment", comment.owner)
        session.add(new_vote)
        session.commit()
        schema.remove_session()

        # Comprobamos que la operación es exitosa
        if(comment.get_num_votes == prev_vote):
            return True
        else:
            return False

        
