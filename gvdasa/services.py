import requests
import logging
from decouple import config

_logger = logging.getLogger(__name__)


class GvdasaService:
    def __init__(self, base_url: str = None):
        self.base_url = (base_url or config("GVDASA_BASE_URL")).rstrip("/")
        self.token = config("GVDASA_API_KEY")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

    def get_student_info(self, registration: str) -> dict:
        gvdasa_url = f"{self.base_url}/consultaAluno/{registration}"
        try:
            response = requests.get(gvdasa_url, headers=self.headers)
            response.raise_for_status()
            return {
                "ok": True,
                "data": response.json(),
                "error": None,
            }
        except Exception as error:
            _logger.error(f"Request error on GET {gvdasa_url}: {error}")
            return {
                "ok": False,
                "data": None,
                "error": str(error),
            }
