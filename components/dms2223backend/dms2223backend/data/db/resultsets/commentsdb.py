""" Comments class module.
"""

from typing import List
from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.db.results.answerdb import Answer
from dms2223backend.data.db.results.commentdb import Comment
from dms2223backend.data.sentiment import Sentiment

class Comments():
    """ Class responsible of table-level comments operations.
    """
    @staticmethod
    def create(session: Session, aid:int, body: str, sentiment: Sentiment, owner: str) -> Comment:
        """ Creates a new comment record.

        Note:
            Any existing transaction will be committed.

        Args:
            - session (Session): The session object.
            - body (str): The comment's body.
            - sentiment (enumerate) : The sentiment of the comment.

        Raises:
            - ValueError: If the sentiment is empty.

        Returns:
            - Comment: The created `Comment` result.
        """
        if not sentiment :
            raise ValueError('El sentimentio es un campo obligatorio para crear un comentario.')

        new_comm = Comment(aid, body, sentiment, False, owner=owner)

        session.add(new_comm)
        session.commit()
        return new_comm

    @staticmethod
    def get_comment(session: Session, cid:int) -> Comment:
        """Gets a particular commentt.

        Args:
            - session (Session): The session object.
            - cid (int): The comment's id

        Returns:
            - Comment: Expected `Comment` register.
        """

        query = session.query(Comment).where(Comment.id == cid)
        return query.first()

    @staticmethod
    def list_all(session: Session, aid: int) -> List[Comment]:
        """Lists every comment of an anser.

        Args:
            - session (Session): The session object.

        Returns:
            - List[Comment]: A list of `Comment` registers.
        """

        query = session.query(Comment).filter(Comment.aid == aid)
        return query.all()
