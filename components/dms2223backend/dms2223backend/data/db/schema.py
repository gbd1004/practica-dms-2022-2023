""" Schema class module.
"""

from sqlalchemy import create_engine, event  # type: ignore
from sqlalchemy.engine import Engine  # type: ignore
from sqlalchemy.orm import sessionmaker, scoped_session, registry  # type: ignore
from sqlalchemy.orm.session import Session  # type: ignore
from dms2223backend.data.config import BackendConfiguration
from dms2223backend.data.db.results import Answer, Question, Comment
from dms2223backend.data.db.results.report import Report, ReportAnswer, ReportComment, ReportQuestion
from dms2223backend.data.db.results.vote import  Votes, VotesAns, VotesComm

# Required for SQLite to enforce FK integrity when supported
@event.listens_for(Engine, 'connect')
def set_sqlite_pragma(dbapi_connection, connection_record):  # pylint: disable=unused-argument
    """ Sets the SQLite foreign keys enforcement pragma on connection.

    Args:
        - dbapi_connection: The connection to the database API.
    """
    cursor = dbapi_connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON;')
    cursor.close()


class Schema():
    """ Class responsible of the schema initialization and session generation.
    """

    def __init__(self, config: BackendConfiguration):
        """ Constructor method.

        Initializes the schema, deploying it if necessary.

        Args:
            - config (BackendConfiguration): The instance with the schema connection parameters.

        Raises:
            - RuntimeError: When the connection cannot be created/established.
        """
        self.__registry = registry()
        if config.get_db_connection_string() is None:
            raise RuntimeError(
                'A value for the configuration parameter `db_connection_string` is needed.'
            )
        db_connection_string: str = config.get_db_connection_string() or ''
        self.__create_engine = create_engine(db_connection_string)
        self.__session_maker = scoped_session(
            sessionmaker(bind=self.__create_engine))

        Answer.map(self.__registry)
        Report.map(self.__registry)
        Question.map(self.__registry)
        Comment.map(self.__registry)
        Votes.map(self.__registry)
        VotesAns.map(self.__registry)
        VotesComm.map(self.__registry)
        ReportAnswer.map(self.__registry)
        ReportComment.map(self.__registry)
        ReportQuestion.map(self.__registry)
        self.__registry.metadata.create_all(self.__create_engine)

    def new_session(self) -> Session:
        """ Constructs a new session.

        Returns:
            - Session: A new `Session` object.
        """
        return self.__session_maker()

    def remove_session(self) -> None:
        """ Frees the existing thread-local session.
        """
        self.__session_maker.remove()
