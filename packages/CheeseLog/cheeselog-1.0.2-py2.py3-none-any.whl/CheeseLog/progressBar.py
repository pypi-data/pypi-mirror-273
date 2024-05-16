from typing import Tuple

class ProgressBar:
    def __init__(self, length: int = 20, template: str = '%b%l%r%b %p%', *, boundaryStr: str = '|', leftStr: str = '█', rightStr: str = '-'):
        '''
        进度条配合loading可以达到更好的效果。

        ```python
        import time

        from CheeseLog import logger, ProgressBar

        progressBar = ProgressBar()
        for i in range(101):
            message, styledMessage = progressBar(i / 100)
            logger.loading(message, styledMessage)
            time.sleep(0.1)
        ```

        - Args

            - length: 进度条的长度。

            - template: 模版，通过占位符匹配内容。%b: 边界字符；%l: 左侧完成的进度；%r: 右侧未完成的进度；%p: 百分数。

            - boundaryStr: 边界字符。

            - leftStr: 完成的进度字符（左侧字符）。

            - rightStr: 未完成的进度字符（右侧字符）。
        '''

        self._length: int = length
        self.template: str = template
        self.boundaryStr: str = boundaryStr
        self.leftStr: str = leftStr
        self.rightStr: str = rightStr

    def __call__(self, value: float) -> Tuple[str, str]:
        '''
        - Args:

            - value: 百分数，范围[0, 1]。
        '''

        left = round(value * self.length)
        right = self.length - left

        return self.template.replace('%b', self.boundaryStr).replace('%l', self.leftStr * left).replace('%r', self.rightStr * right).replace('%p', '{:.2f}'.format(value * 100)), self.template.replace('%b', self.boundaryStr).replace('%l', self.leftStr * left).replace('%r', self.rightStr * right).replace('%p', '<blue>{:.2f}</blue>'.format(value * 100)).replace('%', '%%')

    @property
    def length(self) -> int:
        '''
        进度条的长度。
        '''

        return self._length

    @length.setter
    def length(self, value: int):
        self._length = value

    @property
    def template(self) -> str:
        '''
        模版，通过占位符匹配内容：

        - %b: 边界字符

        - %l: 左侧完成的进度

        - %r: 右侧未完成的进度

        - %p: 百分数
        '''

        return self._template

    @template.setter
    def template(self, value: str):
        self._template = value

    @property
    def boundaryStr(self) -> str:
        '''
        边界字符。
        '''

        return self._boundaryStr

    @boundaryStr.setter
    def boundaryStr(self, value: str):
        self._boundaryStr = value

    @property
    def leftStr(self) -> str:
        '''
        完成的进度字符（左侧字符）。
        '''

        return self._leftStr

    @leftStr.setter
    def leftStr(self, value: str):
        self._leftStr = value

    @property
    def rightStr(self) -> str:
        '''
        未完成的进度字符（右侧字符）。
        '''

        return self._rightStr

    @rightStr.setter
    def rightStr(self, value: str):
        self._rightStr = value
