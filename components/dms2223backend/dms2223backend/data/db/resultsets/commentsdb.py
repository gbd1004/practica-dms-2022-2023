""" Users class module.
"""

import hashlib
from typing import List
from sqlalchemy.exc import IntegrityError  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from sqlalchemy.orm.exc import NoResultFound  # type: ignore
from dms2223backend.data.db.results.answerdb import Answer
from dms2223backend.data.db.results.commentdb import Comment




class Comments():
    """ Class responsible of table-level users operations.
    """
    @staticmethod
    def create(session: Session, body: str, sentiment: enumerate) -> Comment:
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

        new_comm = Answer(session, body)
        
        session.add(new_comm)
        session.commit()
        return new_comm


    @staticmethod
    def list_all(session: Session) -> List[Comment]:
        """Lists every comment.

        Args:
            - session (Session): The session object.

        Returns:
            - List[Comment]: A list of `Comment` registers.
        """
        
        query = session.query(Comment)
        return query.all()


