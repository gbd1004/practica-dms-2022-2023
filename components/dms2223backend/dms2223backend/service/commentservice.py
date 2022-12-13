"""
CommentServices class module.
"""

from typing import List
from sqlalchemy.orm.session import Session # type: ignore
from dms2223backend.data.db.results.vote.votecommdb import VotesComm
from dms2223backend.data.db.results.vote.votedb import Votes # type: ignore
from dms2223backend.data.db.resultsets.commentsdb import Comments
from dms2223backend.data.db.resultsets.votes.votesdb import VotesSet
from dms2223backend.data.db.schema import Schema
from dms2223backend.data.db.results.commentdb import Comment
from dms2223backend.data.sentiment import Sentiment

class CommentServices():
    """
    Monostate class that provides high-level services to handle Comments' use cases.
    """

    @staticmethod
    def get_comments(schema: Schema, aid:int) -> List[dict]:
        """Lists the existing comments.

        Args:
            - schema (Schema): A database handler where the comments are mapped into.

        Returns:
            - List[dict]: A list of dictionaries with the comments' data.
        """
        out: List[dict] = []
        session: Session = schema.new_session()
        comments: List[Comment] = Comments.list_all(session, aid)
        for comment in comments:
            if comment.hidden is False:
                out.append({
                    'cid': comment.id,
                    'aid': comment.aid,
                    'timestamp': comment.timestamp,
                    'body' : comment.body,
                    'sentiment': comment.sentiment.name,
                    'owner': {'username': comment.owner},
                    'votes': comment.get_num_votes(session)
                })
        schema.remove_session()
        return out

    @staticmethod
    def get_comment(schema: Schema, cid:int) -> dict:
        """Gets the comment with the same parameter cid.

        Args:
            - cid (int): The comment cid.
            - schema (Schema): A database handler where the comment are mapped into.

        Returns:
            - dict: A dictionary with the comment's data.
        """
        out = {}
        session: Session = schema.new_session()
        comment: Comment = Comments.get_comment(session, cid)
        if comment.hidden is False:
            out = {
                'cid': comment.id,
                'aid': comment.aid,
                'timestamp': comment.timestamp,
                'body' : comment.body,
                'sentiment': comment.sentiment.name,
                'owner': {'username': comment.owner},
                'votes': comment.get_num_votes(session)
            }

        schema.remove_session()
        return out



    @staticmethod
    def get_votes(schema: Schema, cid:int) -> dict:
        """Lists the existing comment's votes.

        Args:
            - schema (Schema): A database handler where the comment are mapped into.
            - cid (int): Comment identifier

        Returns:
            - dict: A dictionary with the votes' data.
        """
        out = {}
        # votes: List = [Votes]
        session: Session = schema.new_session()
        comment: Comment = Comments.get_comment(session,cid)
        if comment.hidden is False:
            votes = VotesSet.list_all_comm(session, cid)
            for v in votes:
                out[v.user] = True
        schema.remove_session()
        return out

    @staticmethod
    def create_comment(aid:int,body: str,sentiment: Sentiment,owner: str,schema: Schema) -> dict:
        """Creates a new comment.

        Args:
            - body (str): The comment's body.
            - aid (int): The answer's aid.
            - sentiment (str): The comment sentiment.

        Returns:
            - dict: A dictionary with the new comment's data.
        """

        session: Session = schema.new_session()
        out = {}
        if body == "":
            return out


        try:
            new_comment: Comment = Comments.create(session, aid, body, sentiment, owner)
            out = {
                'cid': new_comment.id,
                'aid': new_comment.aid,
                'timestamp': new_comment.timestamp,
                'body' : new_comment.body,
                'sentiment': new_comment.sentiment.name,
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
        new_vote: VotesComm = VotesComm(id, comment.owner)
        session.add(new_vote)
        session.commit()
        exito = False

        # Comprobamos que la operación es exitosa
        if comment.get_num_votes(session) != prev_vote:
            exito = True

        schema.remove_session()
        return exito
