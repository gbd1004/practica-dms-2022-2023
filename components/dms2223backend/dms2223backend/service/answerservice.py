"""
AnswerServices class module.
"""

from ast import Dict
from typing import List
from sqlalchemy.orm.session import Session # type: ignore
from dms2223backend.data.db.results.vote.voteansdb import VotesAns
from dms2223backend.data.db.resultsets.answersdb import Answers
from dms2223backend.data.db.resultsets.votes.votesdb import VotesSet
from dms2223backend.data.db.schema import Schema
from dms2223backend.data.db.results.answerdb import Answer

class AnswerServices():
    """
    Monostate class that provides high-level services to handle Answers' use cases.
    """

    @staticmethod
    def get_answers(schema: Schema, qid:int) -> Dict:
        """Lists the existing answers.

        Args:
            - schema (Schema): A database handler where the answers are mapped into.

        Returns:
            - List[Dict]: A list of dictionaries with the answers' data.
        """
        out: Dict[Dict] = []
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
                    'votes': answ.get_num_votes(session)
                })
        schema.remove_session()
        return out

    @staticmethod
    def get_answer(schema: Schema, aid:int) -> Dict:
        """Gets the answer with the same parameter aid.

        Args:
            - aid (int): The answer aid.
            - schema (Schema): A database handler where the answers are mapped into.

        Returns:
            - Dict: A dictionary with the answer's data.
        """
        out: List = []
        session: Session = schema.new_session()
        answer: Answer = Answers.get_answer(session, aid)
        if answer.hidden is False:
            out = {
                    'aid': answer.aid,
                    'qid': answer.qid,
                    'timestamp': answer.timestamp,
                    'body' : answer.body,
                    'owner': {'username':answer.owner},
                    'votes': answer.get_num_votes(session)
            }

        schema.remove_session()
        return out

    @staticmethod
    def get_votes(schema: Schema, aid:int) -> Dict:
        """Lists the existing answer's votes.

        Args:
            - schema (Schema): A database handler where the answers are mapped into.

        Returns:
            - Dict: A dictionary with the votes' data.
        """
        out: Dict = {}
        session: Session = schema.new_session()
        answer: Answer = Answers.get_answer(session,aid)
        if answer.hidden is False:
            votes = VotesSet.list_all_ans(session, aid)
            for vote in votes:
                out[vote.user] = True
        schema.remove_session()
        return out


    @staticmethod
    def create_answer(qid: int, body: str, owner: str, schema: Schema) -> Dict:
        """Creates a new answer.

        Args:
            - body (str): The answer's body.
            - qid (int): The question's qid.

        Raises:
            - ValueError: If either the username or the password_hash is empty.

        Returns:
            - Dict: A dictionary with the new answer's data.
        """

        session: Session = schema.new_session()
        out: Dict = {}
        try:
            new_answer: Answer = Answers.create(session, qid, body, owner)
            out = {
                    'aid': new_answer.aid,
                    'qid': new_answer.qid,
                    'timestamp': new_answer.timestamp,
                    'body' : new_answer.body,
                    'owner': {'username':new_answer.owner},
                    'votes': new_answer.get_num_votes(session)
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
        prev_vote = answer.get_num_votes(session)

        # Se añade el nuevo voto
        new_vote: VotesAns = VotesAns(aid, answer.owner)
        session.add(new_vote)
        session.commit()
        exito = False

        # Comprobamos que la operación es exitosa
        if answer.get_num_votes(session) != prev_vote:
            exito = True

        schema.remove_session()
        return exito
