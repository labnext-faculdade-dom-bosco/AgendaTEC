import requests
import json
import logging
from decouple import config

_logger = logging.getLogger(__name__)


class WahaService:
    def __init__(self, session: str = "default", base_url: str = "http://waha:3000/"):
        self.session = session
        self.base_url = base_url.rstrip('/')
        self.api_key = config('WAHA_API_KEY')
        self.headers = {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key
        }

    @staticmethod
    def get_chat_id_from_phone_number(phone_number: str) -> str:
        if not isinstance(phone_number, str):
            raise TypeError("Phone number must be string")

        if not phone_number.endswith("@c.us"):
            return f"{phone_number}@c.us"

        return phone_number

    def send_message(self, phone_number: str, message: str):
        url_send_message = f"{self.base_url}/api/sendText"
        payload = {
            "chatId": self.get_chat_id_from_phone_number(phone_number),
            "text": message,
            "session": self.session,
        }
        try:
            response = requests.post(url_send_message, headers=self.headers, json=payload)
            response.raise_for_status()

            return response.json()

        except Exception as error:
            _logger.error("Error sending message: %s", error)
            return {
                "ok": False,
                "data": None,
                "error": str(error),
            }
