""" 
AnswerServices class module.
"""

from ast import Dict
from typing import List
from sqlalchemy.orm.session import Session
from dms2223backend.data.db.results.vote.votedb import Votes  # type: ignore
from dms2223backend.data.db.resultsets.answersdb import Answers
from dms2223backend.data.db.resultsets.votes.votesdb import VotesSet
from dms2223backend.data.db.schema import Schema
from dms2223backend.data.db.results.answerdb import Answer


class AnswerServices():
    """ 
    Monostate class that provides high-level services to handle Answers' use cases.
    """

    @staticmethod
    def get_answers(schema: Schema, qid:int) -> List[Dict]:
        """Lists the existing answers.

        Args:
            - schema (Schema): A database handler where the answers are mapped into.

        Returns:
            - List[Dict]: A list of dictionaries with the answers' data.
        """
        out: List[Dict] = []
        session: Session = schema.new_session()
        answers: List[Answer] = Answers.list_all(session,qid)
        for a in answers:
            if a.hidden == False:
                out.append({
                    'aid': a.aid,
                    'qid': a.qid,
                    'timestamp': a.timestamp,
                    'body' : a.body,
                    'owner': {'username':a.owner},
                    'votes': a.get_num_votes(session)
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
        out: Dict = {}
        session: Session = schema.new_session()
        answer: Answer = Answers.get_answer(session, aid)
        if answer.hidden == False:
            out['aid'] = {
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
        if answer.hidden == False:
            votes: VotesSet.list_all(session, "voteanswer", aid)
            for v in votes:
                #TODO: revisar
                out[v.user] = True
        schema.remove_session()
        return out


    @staticmethod
    def create_answer(qid: int, body: str,schema: Schema) -> Dict:
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
            new_answer: Answer = Answers.create(session, qid, body)
            out['aid'] = {
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
        new_vote: Votes = Votes(aid, "voteanswer", answer.owner)
        session.add(new_vote)
        session.commit()
        schema.remove_session()

        # Comprobamos que la operación es exitosa
        if(answer.get_num_votes == prev_vote):
            return True
        else:
            return False
    

        
