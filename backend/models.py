from pydantic import BaseModel
from typing import Union, Optional, List


class Test(BaseModel):
    task: str
    goal: str
    persona: str

class AITest(BaseModel):
    chatbot_desc: str
    user_desc: str
    n_samples: Optional[int] = 4


class RunTest(BaseModel):
    test_id: str
    tests: Test
    chatbot_desc: str
    n_turns: Optional[int] = 6
    n_seeds: Optional[int] = 5