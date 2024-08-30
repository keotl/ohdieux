from typing import Optional, Union


class SafeDict(object):

    def __init__(self, content: Optional[dict]):
        self._content = content

    def __getitem__(self, key: str) -> "SafeDict":
        if self._content is None:
            return self

        if key not in self._content or not isinstance(self._content, dict):
            return SafeDict(None)

        return SafeDict(self._content[key])

    def value(self) -> Optional[Union[str, int, dict]]:
        return self._content
