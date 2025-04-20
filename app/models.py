from datetime import datetime, timedelta
from secrets import token_urlsafe
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

class AuthToken(db.Model):
    """Model for storing authentication tokens"""
    __tablename__ = 'auth_tokens'
    
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    used = db.Column(db.Boolean, default=False)
    
    user = db.relationship('User', backref='tokens')

    def __init__(self, user, expires_in=3600):
        self.token = token_urlsafe(32)
        self.user_id = user.id
        self.expires_at = datetime.utcnow() + timedelta(seconds=expires_in)

    def is_valid(self):
        """Check if token is still valid and hasn't been used"""
        return not self.used and datetime.utcnow() < self.expires_at

    def mark_used(self):
        """Mark token as used"""
        self.used = True


class User(db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, 
                          onupdate=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        """Create hashed password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check hashed password"""
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        """Generate a new auth token for magic link"""
        token = AuthToken(self, expires_in)
        db.session.add(token)
        db.session.commit()
        return token.token

    def get_token(self, token_str):
        """Get valid token if exists and not expired"""
        token = AuthToken.query.filter_by(
            token=token_str, 
            user_id=self.id,
            used=False
        ).first()
        return token if token and token.is_valid() else None

    def get_reset_token(self, expires_in=1800):
        """Generate password reset token"""
        s = Serializer(current_app.config['SECRET_KEY'], expires_in)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """Verify password reset token"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def all_posts(self):
        """Get all posts by this user"""
        return self.posts.order_by(Post.timestamp.desc())


class Post(db.Model):
    """Blog post model"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Post {self.title}>'

