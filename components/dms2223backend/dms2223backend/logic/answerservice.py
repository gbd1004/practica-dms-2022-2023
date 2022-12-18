"""
AnswerServices class module.
"""

from typing import List
from sqlalchemy.orm.session import Session # type: ignore
from dms2223backend.data.db.results.vote.voteansdb import VotesAns
from dms2223backend.data.db.resultsets.answersdb import Answers
from dms2223backend.data.db.resultsets.votes.votesAdb import VotesA
from dms2223backend.data.db.schema import Schema
from dms2223backend.data.db.results.answerdb import Answer

class AnswerServices():
    """
    Monostate class that provides high-level services to handle Answers' use cases.
    """

    @staticmethod
    def get_answers(schema: Schema, qid:int) -> List:
        """Lists the existing answers.

        Args:
            - schema (Schema): A database handler where the answers are mapped into.

        Returns:
            - List[dict]: A list of dictionaries with the answers' data.
        """
        out = []
        session: Session = schema.new_session()
        answers: List[Answer] = Answers.list_all(session,qid)
        for answ in answers:
            if answ.hidden is False:
                out.append({
                    'aid': answ.aid,
                    'qid': answ.qid,
                    'timestamp': answ.timestamp,
                    'body' : answ.body,
                    'owner': {'username':answ.owner},
                    'votes': Answers.get_num_votes(session,answ.aid)
                })
        schema.remove_session()
        return out

    @staticmethod
    def get_answer(schema: Schema, aid:int) -> dict:
        """Gets the answer with the same parameter aid.

        Args:
            - aid (int): The answer aid.
            - schema (Schema): A database handler where the answers are mapped into.

        Returns:
            - dict: A dictionary with the answer's data.
        """
        out = {}
        session: Session = schema.new_session()
        answer: Answer = Answers.get_answer(session, aid)
        if answer.hidden is False:
            out = {
                'aid': answer.aid,
                'qid': answer.qid,
                'timestamp': answer.timestamp,
                'body' : answer.body,
                'owner': {'username':answer.owner},
                'votes': Answers.get_num_votes(session,answer.aid)
            }

        schema.remove_session()
        return out

    @staticmethod
    def get_votes(schema: Schema, aid:int) -> dict:
        """Lists the existing answer's votes.

        Args:
            - schema (Schema): A database handler where the answers are mapped into.

        Returns:
            - dict: A dictionary with the votes' data.
        """
        out = {}
        session: Session = schema.new_session()
        answer: Answer = Answers.get_answer(session, aid)
        if answer.hidden is False:
            votes = VotesA.list_all_ans(session, aid)
            for vote in votes:
                out[vote.user] = True
        schema.remove_session()
        return out


    @staticmethod
    def create_answer(qid: int, body: str, owner: str, schema: Schema) -> dict:
        """Creates a new answer.

        Args:
            - body (str): The answer's body.
            - qid (int): The question's qid.

        Raises:
            - ValueError: If either the username or the password_hash is empty.

        Returns:
            - dict: A dictionary with the new answer's data.
        """

        session: Session = schema.new_session()
        out = {}
        try:
            new_answer: Answer = Answers.create(session, qid, body, owner)
            out = {
                    'aid': new_answer.aid,
                    'qid': new_answer.qid,
                    'timestamp': new_answer.timestamp,
                    'body' : new_answer.body,
                    'owner': {'username':new_answer.owner},
                    'votes': Answers.get_num_votes(session, new_answer.aid)
            }

        except Exception as ex:
            raise ex
        finally:
            schema.remove_session()
        return out


    @staticmethod
    def hide_answer(schema: Schema, aid: int):
        """Hides the answer with the same parameter aid.

        Args:
            - aid (int): The answer's aid.
            - schema (Schema): A database handler where the answers are mapped into.

        """
        session: Session = schema.new_session()

        answer: Answer = Answers.get_answer(session,aid)
        answer.hidden = True

        # Actualizamos la respuesta
        session.add(answer)
        session.commit()

        schema.remove_session()

    @staticmethod
    def vote_answer(schema: Schema, aid: int) -> bool:
        """Add a vote to the answer with the same parameter aid.

        Args:
            - aid (int): The answer's aid.
            - schema (Schema): A database handler where the answers are mapped into.

        """
        session: Session = schema.new_session()

        # Se guarda el número inicial de votos para comprobar que la operación es exitosa
        answer: Answer = Answers.get_answer(session,aid)
        prev_vote = Answers.get_num_votes(session, answer.aid)

        # Se añade el nuevo voto
        exito = True
        try:
            new_vote: VotesAns = VotesAns(aid, answer.owner)
            session.add(new_vote)
            session.commit()
            # Comprobamos que la operación es exitosa
            if Answers.get_num_votes(session, answer.aid) != prev_vote:
                exito = True
            else:
                exito = False
        except:
            exito = False


        schema.remove_session()
        return exito
