"""任务相关 Pydantic schema"""

from pydantic import BaseModel
from typing import Optional


class TaskInfo(BaseModel):
    id: str
    title: str
    description: str
    reward_energy: int
    status: str
