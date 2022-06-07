import os

from app.common.application.middlewares.services.jwt_key import JwtKey
from app.common.domain.models.depositing_application import DepositingApplication


class EpaddJwtKey(JwtKey):
    def __init__(self) -> None:
        self.issuer = os.getenv('EPADD_JWT_ISSUER')
        self.public_key_path = os.getenv('EPADD_JWT_PUBLIC_KEY_FILE_PATH')
        self.depositing_application = DepositingApplication.ePADD
