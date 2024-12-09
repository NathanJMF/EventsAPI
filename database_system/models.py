from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)

    actions = relationship('UserAction', back_populates='user', cascade='all, delete-orphan')
    alerts = relationship('Alert', back_populates='user', cascade='all, delete-orphan')


class UserAction(Base):
    __tablename__ = 'user_actions'

    action_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    type = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    timestamp = Column(Integer, nullable=False)

    user = relationship('User', back_populates='actions')


class Alert(Base):
    __tablename__ = 'alerts'

    alert_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    alert_code = Column(Integer, nullable=False)
    timestamp = Column(Integer, nullable=False)

    user = relationship('User', back_populates='alerts')

