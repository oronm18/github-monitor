from fastapi import FastAPI, Header, HTTPException, Request
import hmac
import hashlib
import logging

from env import WEBHOOK_SECRET
from handler import check_event


def create_app(notifiers: list):
    app = FastAPI()
    app.state.notifiers = notifiers  # <-- stash them on the app

    def valid_signature(body: bytes, signature_header: str) -> bool:
        """
        Validate X‑Hub‑Signature‑256 header against the payload.
        """
        if '=' not in signature_header:
            return False
        sha_name, signature = signature_header.split('=')
        if sha_name != 'sha256':
            return False

        mac = hmac.new(WEBHOOK_SECRET, body, hashlib.sha256)
        return hmac.compare_digest(mac.hexdigest(), signature)

    @app.post('/webhook')
    async def webhook(
        request: Request,
        x_hub_signature_256: str = Header(None),
        x_github_event: str = Header(None)
    ) -> dict:
        if not valid_signature(await request.body(), x_hub_signature_256):
            raise HTTPException(status_code=401, detail='Invalid signature')

        payload = await request.json()
        logging.info(f'Received {x_github_event} event with {payload=}.\n')
        if check_event(x_github_event, payload) is False:
            for notify in request.app.state.notifiers:
                notify(x_github_event, payload)
            raise HTTPException(status_code=403, detail='Suspicious behavior detected')

        return {'status': 'ok'}

    return app

