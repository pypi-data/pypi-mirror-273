from .encrypt import Encrypt
from .payment import Payment


class Method(
    Encrypt,
    Payment
):
    pass
