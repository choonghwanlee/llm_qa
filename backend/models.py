from pydantic import BaseModel
from typing import Union, Optional, List


class Test(BaseModel):
    task: str
    goal: str
    persona: str

class AITest(BaseModel):
    chatbot_desc: Optional[str] = "responds to user's requests about adding/removing items from the shopping cart, changing payment information, unsubscribing to emails, getting product recommendations, check order information, process returns/complaints"
    user_desc: str
    n_samples: Optional[int] = 4


class RunTest(BaseModel):
    test_id: str
    task: str
    goal: str
    persona: str
    chatbot_desc: Optional[str] = "responds to user's requests about adding/removing items from the shopping cart, changing payment information, unsubscribing to emails, getting product recommendations, check order information, process returns/complaints"
    n_turns: Optional[int] = 6
    n_seeds: Optional[int] = 5