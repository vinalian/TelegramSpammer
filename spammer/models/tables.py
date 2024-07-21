from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, func, UUID, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

__all__ = ['Account', 'Chat', 'Interval', 'Message']


class Account(Base):
    __tablename__ = 'api_account'

    id = Column(UUID, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String(64))
    phone_number = Column(String(15), unique=True)
    api_id = Column(String(64), unique=True)
    api_hash = Column(String(64), unique=True)
    session_string = Column(Text)
    last_auth = Column(DateTime)
    created_date = Column(DateTime, server_default=func.now())
    is_active = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)

    chats = relationship("Chat", back_populates="account")
    interval = relationship("Interval", uselist=False, back_populates="account")

    def to_dict(self):
        return {
            'id': str(self.id),
            'phone_number': self.phone_number,
            'api_id': self.api_id,
            'api_hash': self.api_hash,
            'session_string': self.session_string
        }

    def __repr__(self):
        return f'<Account(name={self.name}, phone_number={self.phone_number})>'


class Chat(Base):
    __tablename__ = 'api_chat'

    id = Column(UUID, primary_key=True, default=str(uuid.uuid4()))
    title = Column(String(64))
    chat_id = Column(BigInteger)
    account_id = Column(UUID, ForeignKey("api_account.id"))
    last_message_send = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    is_banned = Column(Boolean, default=False)

    account = relationship("Account", back_populates="chats")

    def to_dict(self) -> dict:
        return {
            'id': str(self.id),
            'title': self.title,
            'chat_id': self.chat_id,
            'last_message_send': self.last_message_send,
            'is_active': self.is_active,
            'is_banned': self.is_banned # lazy loading for efficiency when not needed.
        }

    def __repr__(self):
        return f'<Chat(title={self.title}, chat_id={self.chat_id})>'


class Interval(Base):
    __tablename__ = 'api_interval'

    id = Column(UUID, primary_key=True, default=str(uuid.uuid4()))
    account_id = Column(UUID, ForeignKey('api_account.id'), unique=True)
    interval = Column(Integer)

    account = relationship("Account", uselist=False, back_populates="interval")

    def to_dict(self):
        return {
            'account': self.account.to_dict(),
            'interval': self.interval,
        }

    def __repr__(self):
        return f'<Interval(account_id={self.account_id}, interval={self.interval})>'


class Message(Base):
    __tablename__ = 'api_message'

    id = Column(UUID, primary_key=True, default=str(uuid.uuid4()))
    message_type = Column(String(16), unique=True)
    message_text = Column(Text)

    def to_dict(self):
        return {
            'id': self.id,
            'message_type': self.message_type,
            'message_text': self.message_text,
        }

    def __repr__(self):
        return f'<Message(message_type={self.message_type})>'
