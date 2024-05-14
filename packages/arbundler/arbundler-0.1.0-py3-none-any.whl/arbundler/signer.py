import json
import logging
from enum import IntEnum, auto

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS
from jose import jwk

from arbundler.helpers.converters import owner_to_address
from arbundler.helpers.hashing import base64url_decode

logger = logging.getLogger(__name__)


class SignatureType(IntEnum):
    ARWEAVE = auto()
    ED25519 = auto()
    ETHEREUM = auto()
    SOLANA = auto()
    INJECTEDAPTOS = auto()
    MULTIAPTOS = auto()
    TYPEDETHEREUM = auto()


class ArweaveSigner:
    HASH = "sha256"
    SIGNATURE_TYPE = SignatureType.ARWEAVE

    def __init__(self, jwk_data: dict) -> None:
        self.jwk_data = jwk_data
        self.jwk = jwk.construct(self.jwk_data, algorithm=jwk.ALGORITHMS.RS256)
        self.rsa = RSA.importKey(self.jwk.to_pem())

        self.public_key = base64url_decode(self.owner)
        self.address = owner_to_address(self.owner)

    @property
    def owner(self):
        return self.jwk_data["n"]

    @classmethod
    def from_file(cls, jwk_file_path: str) -> "ArweaveSigner":
        with open(jwk_file_path) as r:
            return cls(json.load(r))

    def sign(self, message):
        h = SHA256.new(message)
        signed_data = PKCS1_PSS.new(self.rsa).sign(h)
        return signed_data
