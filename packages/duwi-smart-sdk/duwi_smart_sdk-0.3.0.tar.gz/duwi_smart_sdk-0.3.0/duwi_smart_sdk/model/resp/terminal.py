import datetime


class TerminalInfo:
    def __init__(self,
                 terminalName: str,
                 terminalSequence: str,
                 shortCode: str,
                 productModel: str,
                 productLogo: str,
                 seq: int,
                 isGateWay: int,
                 hostSequence: str,
                 createTime: str,
                 productShowModel: str,
                 isFollowOnline: bool,
                 isOnline: bool):
        self.terminalName = terminalName
        self.terminalSequence = terminalSequence
        self.shortCode = shortCode
        self.productModel = productModel
        self.productLogo = productLogo
        self.seq = seq
        self.isGateWay = isGateWay
        self.hostSequence = hostSequence
        self.createTime = createTime
        self.productShowModel = productShowModel
        self.isFollowOnline = isFollowOnline
        self.isOnline = isOnline

    @staticmethod
    def _parse_datetime(datetime_str: str) -> datetime.datetime:
        return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
