from requests import get, post
from typing import Optional

import generate


class Payment:
    def createPayment(
        self: 'generate.Generate',
        tokenApi: str,
        key: str,
        nameKode: str,
        tokenPay: str,
        userId: int,
        merchantId: Optional[str],
        price: str
    ):
        unikCode = self.genUnikCode(name=f'{nameKode}-', length=3)
        response = post(
            f"{self._apiUrlPay}/api/payment/create",
            json={
                "tokenPay": tokenPay,
                "userId": userId,
                "merchantId": merchantId,
                "uniqueCode": unikCode,
                "paymentId": 17,
                "price": price,
                "note": f"{nameKode.upper()} NIH BANG",
                "typeFee": '1'
            },
            headers={
                "Authorization": f'Bearer {tokenApi}.{key}',
                "Content-Type": 'application/json'
            }
        )
        res = response.json()
        if response.status_code == 200:
            return res
        return None


    def cekPayment(
        self: 'generate.Generate',
        tokenApi: str,
        key: str,
        tokenPay: str,
        unikCodeId: str,
        userId: int
    ):
        response = get(
            f'{self._apiUrlPay}/api/payment/status?tokenPay={tokenPay}&code={unikCodeId}&userId={userId}',
            headers={
                "Authorization": f'Bearer {tokenApi}.{key}'
            }
        )
        res = response.json()
        return res


    def cancelPayment(
        self: 'generate.Generate',
        tokenApi: str,
        key: str,
        tokenPay: str,
        unikCodeId: str
    ):
        response = get(
            f'{self._apiUrlPay}/api/payment/cancel?tokenPay={tokenPay}&code={unikCodeId}',
            headers={
                "Authorization": f'Bearer {tokenApi}.{key}'
            }
        )
        res = response.json()
        return res
