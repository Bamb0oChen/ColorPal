"""小彩 Agent 对话路由。"""

import logging
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.agent_chat import chat_with_agent

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/agent', tags=['agent'])


class ChatHistoryItem(BaseModel):
    role: Literal['user', 'assistant']
    content: str = Field(min_length=1, max_length=1000)


class AgentChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=1000)
    history: list[ChatHistoryItem] = Field(default_factory=list)
    user_id: str = 'default'


@router.post('/chat')
async def chat(request: AgentChatRequest, db: Session = Depends(get_db)):
    """和小彩对话，模型不可用时返回本地兜底回复。"""
    try:
        data = await chat_with_agent(
            db=db,
            message=request.message.strip(),
            history=[item.model_dump() for item in request.history],
            user_id=request.user_id or 'default',
        )
        return {'code': 0, 'data': data, 'message': 'ok'}
    except Exception as err:
        logger.exception('小彩对话失败')
        raise HTTPException(status_code=500, detail=f'对话失败: {str(err)}') from err
