# Location: src/api/conversations.py
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db_session
from src.db.repository import ConversationRepository, MessageRepository
from src.schemas import ConversationResponse, MessageResponse, MessageCreate, ConversationCreate
from src.core.rate_limiter import limiter
from src.core.logger import logger

router = APIRouter(prefix="/v1/conversations", tags=["conversations"])

@router.post("", response_model=ConversationResponse)
@limiter.limit("10/minute")
async def create_conversation(
    request: Request,  # ← ADD THIS
    data: ConversationCreate = None,
    db: AsyncSession = Depends(get_db_session),
):
    """Create a new conversation."""
    user_id = "user-123"  # TODO: Get from auth
    repo = ConversationRepository(db)
    conversation = await repo.create(user_id=user_id, title=data.title if data else None)
    return conversation

@router.get("/{conversation_id}", response_model=ConversationResponse)
@limiter.limit("30/minute")
async def get_conversation(
    request: Request,  # ← ADD THIS
    conversation_id: str = Path(...),
    db: AsyncSession = Depends(get_db_session),
):
    """Get conversation by ID."""
    repo = ConversationRepository(db)
    conversation = await repo.get_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@router.delete("/{conversation_id}")
@limiter.limit("10/minute")
async def delete_conversation(
    request: Request,  # ← ADD THIS
    conversation_id: str = Path(...),
    db: AsyncSession = Depends(get_db_session),
):
    """Delete a conversation."""
    repo = ConversationRepository(db)
    deleted = await repo.delete(conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"status": "deleted"}

@router.post("/{conversation_id}/messages", response_model=MessageResponse)
@limiter.limit("30/minute")
async def add_message(
    request: Request,  # ← ADD THIS
    conversation_id: str = Path(...),
    data: MessageCreate = None,
    db: AsyncSession = Depends(get_db_session),
):
    """Add a message to conversation."""
    # Verify conversation exists
    conv_repo = ConversationRepository(db)
    conversation = await conv_repo.get_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Add message
    msg_repo = MessageRepository(db)
    message = await msg_repo.create(
        conversation_id=conversation_id,
        role="user",
        content=data.content
    )
    return message

@router.get("/{conversation_id}/messages", response_model=list[MessageResponse])
@limiter.limit("30/minute")
async def get_messages(
    request: Request,  # ← ADD THIS
    conversation_id: str = Path(...),
    db: AsyncSession = Depends(get_db_session),
):
    """Get all messages in a conversation."""
    # Verify conversation exists
    conv_repo = ConversationRepository(db)
    conversation = await conv_repo.get_by_id(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Get messages
    msg_repo = MessageRepository(db)
    messages = await msg_repo.get_by_conversation(conversation_id)
    return messages
