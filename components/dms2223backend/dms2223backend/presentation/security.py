import json
import time
from typing import Dict
from flask import current_app
from authlib.jose import JsonWebSignature  # type: ignore
from connexion.exceptions import Unauthorized  # type: ignore
from dms2223backend.data.config.backendconfiguration import BackendConfiguration

def verify_token(token: str) -> Dict:
    """Callback testing a JWS user token.

    Args:
        - token (str): The JWS user token received.

    Raises:
        - Unauthorized: When the token is incorrect.

    Returns:
        - Dict: A dictionary with the user name (key `user`) if the credentials are correct.
    """    
    with current_app.app_context():
        token_bytes: bytes = token.encode('ascii')
        cfg: BackendConfiguration = current_app.cfg
        jws: JsonWebSignature = current_app.jws
        try:
            data: Dict = jws.deserialize_compact(
                token_bytes,
                bytes(cfg.get_jws_secret(), 'UTF-8')
            )
            payload: Dict = json.loads(data['payload'].decode('UTF-8'))
        except Exception as ex:
            raise Unauthorized from ex
        if 'user' not in payload:
            raise Unauthorized('Invalid token')
        if time.time() > payload['exp']:
            raise Unauthorized('Expired token')
        return {
            'sub': payload['sub'],
            'user': payload['user'],
            'exp': payload['exp']
        }