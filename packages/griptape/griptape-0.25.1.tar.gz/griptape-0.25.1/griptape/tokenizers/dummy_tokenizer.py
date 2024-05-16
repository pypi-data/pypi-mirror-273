from __future__ import annotations
from attrs import define, field
from griptape.exceptions import DummyException
from griptape.tokenizers import BaseTokenizer


@define()
class DummyTokenizer(BaseTokenizer):
    model: str = field(init=False)
    max_input_tokens: int = field(default=0, kw_only=True)
    max_output_tokens: int = field(default=0, kw_only=True)

    def count_tokens(self, text: str | list) -> int:
        raise DummyException(__class__.__name__, "count_tokens")
