class Level:
    def __init__(self, weight: int, messageTemplate: str | None = None, timerTemplate: str | None = None, styledMessageTemplate: str | None = None):
        self._weight: int = weight
        self._messageTemplate: str | None = messageTemplate
        self._timerTemplate: str | None = timerTemplate
        self._styledMessageTemplate: str | None = styledMessageTemplate

    @property
    def weight(self) -> int:
        '''
        权重。更高的权重意味着更危险的信息。
        '''

        return self._weight

    @weight.setter
    def weight(self, value: int):
        self._weight = value

    @property
    def messageTemplate(self) -> str | None:
        '''
        消息模版，未设置时默认为`logger.messageTemplate`。
        '''

        return self._messageTemplate

    @messageTemplate.setter
    def messageTemplate(self, value: str | None):
        self._messageTemplate = value

    @property
    def styledMessageTemplate(self) -> str | None:
        '''
        消息样式模版，未设置时默认为`logger.styledMessageTemplate`。
        '''

        return self._styledMessageTemplate

    @styledMessageTemplate.setter
    def styledMessageTemplate(self, value: str | None):
        self._styledMessageTemplate = value

    @property
    def timerTemplate(self) -> str | None:
        '''
        日期模版，未设置时默认为`logger.timerTemplate`。
        '''

        return self._timerTemplate

    @timerTemplate.setter
    def timerTemplate(self, value: str | None):
        self._timerTemplate = value
