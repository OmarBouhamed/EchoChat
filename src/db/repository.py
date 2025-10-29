# Location: src/db/repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from src.db.models import Conversation, Message
from src.core.logger import logger
from typing import Optional, List

class ConversationRepository:
    """Repository for conversation operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, user_id: str, title: Optional[str] = None) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(user_id=user_id, title=title)
        self.db.add(conversation)
        await self.db.commit()
        await self.db.refresh(conversation, attribute_names=["messages"])  # ← Load messages
        logger.info(f"✅ Created conversation: {conversation.id}")
        return conversation
    
    async def get_by_id(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation by ID with messages loaded."""
        result = await self.db.execute(
            select(Conversation)
            .options(selectinload(Conversation.messages))  # ← Eager load
            .where(Conversation.id == conversation_id)
        )
        return result.scalars().first()
    
    async def get_by_user(self, user_id: str) -> List[Conversation]:
        """Get all conversations for a user."""
        result = await self.db.execute(
            select(Conversation)
            .options(selectinload(Conversation.messages))  # ← Eager load
            .where(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
        )
        return result.scalars().all()
    
    async def delete(self, conversation_id: str) -> bool:
        """Delete a conversation."""
        conversation = await self.get_by_id(conversation_id)
        if not conversation:
            return False
        await self.db.delete(conversation)
        await self.db.commit()
        logger.info(f"✅ Deleted conversation: {conversation_id}")
        return True

class MessageRepository:
    """Repository for message operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, conversation_id: str, role: str, content: str) -> Message:
        """Create a new message."""
        message = Message(conversation_id=conversation_id, role=role, content=content)
        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)
        logger.info(f"✅ Created message: {message.id}")
        return message
    
    async def get_by_conversation(self, conversation_id: str) -> List[Message]:
        """Get all messages in a conversation."""
        result = await self.db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        )
        return result.scalars().all()
    
    async def get_by_id(self, message_id: str) -> Optional[Message]:
        """Get message by ID."""
        result = await self.db.execute(
            select(Message).where(Message.id == message_id)
        )
        return result.scalars().first()
