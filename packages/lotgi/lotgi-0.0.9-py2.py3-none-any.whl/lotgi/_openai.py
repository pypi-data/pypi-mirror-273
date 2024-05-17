"""
There's some annyoing clobbering of the real openai package if we name this file `openai.py`
"""
import openai
from typing import overload

class _Completions:

    def __init__(self, completions):
        self.completions = completions

    def create(self, model, prompt, **kwargs):
        print("Intercepted this specific case of completion with a list of strings")
        return self.completions.create(model=model, prompt=prompt, **kwargs)

    def __getattr__(self, attr):
        return getattr(self.completions, attr)


class OpenAI(openai.OpenAI):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.completions = _Completions(self.completions)

