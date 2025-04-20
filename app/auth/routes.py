from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, url_for, redirect, flash
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from app import db
from app.models import User, AuthToken
from app.email import send_email

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/request-link', methods=['POST'])
def request_link():
    """Handle magic link requests by email"""
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    
    if user:
        token = user.generate_auth_token()
        login_url = url_for('auth.verify_token', token=token, _external=True)
        
        # In production, this would send a real email
        print(f"Magic login link for {user.email}: {login_url}")
        
        return jsonify({
            'message': 'If an account exists with this email, a login link has been sent'
        }), 200
        
    return jsonify({
        'message': 'If an account exists with this email, a login link has been sent'
    }), 200

@bp.route('/verify/<token>')
def verify_token(token):
    """Verify magic link token and log user in"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    token_obj = AuthToken.query.filter_by(token=token, used=False).first()
    if not token_obj or not token_obj.is_valid():
        flash('Invalid or expired token', 'error')
        return redirect(url_for('main.index'))
    
    # Mark token as used
    token_obj.used = True
    token_obj.expires_at = datetime.utcnow()
    db.session.commit()
    
    login_user(token_obj.user)
    flash('Successfully logged in!', 'success')
    return redirect(url_for('main.index'))

@bp.route('/logout')
def logout():
    """Log out current user"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

