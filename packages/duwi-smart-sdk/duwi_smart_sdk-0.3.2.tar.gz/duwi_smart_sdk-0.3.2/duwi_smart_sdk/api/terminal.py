import json
from typing import List, Optional

from duwi_smart_sdk.const.const import URL
from duwi_smart_sdk.const.status import Code
from duwi_smart_sdk.model.resp.terminal import TerminalInfo
from duwi_smart_sdk.util.http import get
from duwi_smart_sdk.util.sign import md5_encrypt
from duwi_smart_sdk.util.timestamp import current_timestamp

class TerminalClient:
    def __init__(self,
                 app_key: str,
                 app_secret: str,
                 access_token: str,
                 app_version: str,
                 client_version: str,
                 client_model: Optional[str] = None
                 ):
        self._url = URL
        self._app_key = app_key
        self._app_secret = app_secret
        self._access_token = access_token
        self._app_version = app_version
        self._client_version = client_version
        self._client_model = client_model

    async def fetch_terminal_info(self, house_no: str) -> tuple[str, List[TerminalInfo] | None]:
        body = {
            "houseNo": house_no
        }
        body_string = (((json.dumps(body, separators=(',', ':'))
                         .replace('{', ""))
                        .replace('}', "")
                        .replace(":", '=')
                        .replace(",", "&"))
                       .replace('"', ''))

        sign = md5_encrypt(body_string + self._app_secret + str(current_timestamp()))

        headers = {
            'Content-Type': 'application/json',
            'accessToken': self._access_token,
            'appkey': self._app_key,
            'secret': self._app_secret,
            'time': str(current_timestamp()),  # Ensure it's converted to string
            'sign': sign,
            'appVersion': self._app_version,
            'clientVersion': self._client_version,
            'clientModel': self._client_model
        }
        status, message, res = await get(URL + "/terminal/infos?houseNo=" + house_no, headers, {})

        if status == Code.SUCCESS.value:
            terminal_infos = res.get('terminals', [])
            terminal_objects = [self._create_terminal_obj(t_info) for t_info in terminal_infos]
            return status, terminal_objects

        return status, None

    @staticmethod
    def _create_terminal_obj(t_info: dict) -> TerminalInfo:
        return TerminalInfo(
            terminalName=t_info.get('terminalName', ''),
            terminalSequence=t_info.get('terminalSequence', ''),
            shortCode=t_info.get('shortCode', ''),
            productModel=t_info.get('productModel', ''),
            productLogo=t_info.get('productLogo', ''),
            seq=t_info.get('seq', 0),
            isGateWay=t_info.get('isGateWay', 0),
            hostSequence=t_info.get('hostSequence', ''),
            createTime=t_info.get('createTime', ''),
            productShowModel=t_info.get('productShowModel', ''),
            isFollowOnline=t_info.get('isFollowOnline', False),
            isOnline=t_info.get('isOnline', False)
        )
