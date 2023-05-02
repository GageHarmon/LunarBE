from datetime import datetime
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.hybrid import hybrid_property
from services import db, bcrypt


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    serialize_only = ('id', 'username', 'email')
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    role = db.Column(db.String)
    
    serialize_rules = ('-ticket.users', '-ticket_comment.users')
    
    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        if password is not None:
            password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
            self._password_hash = password_hash.decode('utf-8')
        else:
            raise ValueError("Password cannot be None")
    def authenticate(self,password):
        return bcrypt.check_password_hash(self._password_hash,password.encode('utf-8'))

class Ticket(db.Model, SerializerMixin):
    __tablename__ = 'tickets'
    
    serialize_only = ('id', 'user_id', 'title', 'description', 'status', 'priority', 'category', 'created_at')
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, nullable=False)
    priority = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    user = db.relationship('User', backref=db.backref('tickets'))
    
    serialize_rules  = ('-user.tickets', '-ticket_comment.tickets')

class TicketComment(db.Model, SerializerMixin):
    __tablename__ = 'ticket_comments'
    
    serialize_only = ('id', 'ticket_id', 'user_id', 'comment', 'is_ai_generated', 'created_at')
    
    id = db.Column(db.Integer, primary_key=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    is_ai_generated = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    ticket = db.relationship('Ticket', backref=db.backref('ticket_comments'))
    user = db.relationship('User', backref=db.backref('ticket_comments'))
    
    serialize_rules = ('-user.ticket_comments', '-ticket.ticket_comments')
