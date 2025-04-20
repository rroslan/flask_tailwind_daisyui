from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, url_for, redirect, flash, current_app, render_template, session
from flask_login import login_user, logout_user, current_user
# Removed werkzeug import as check_password_hash is not used here
from app import db
from app.models import User, AuthToken
from app.email import send_email
# Consider adding an email validation utility if you have one
# from app.utils import is_valid_email

bp = Blueprint('auth', __name__, url_prefix='/auth')

# Updated auth route with better debug messages
@bp.route('/', methods=['GET', 'POST'])
def auth():
    """Handle both GET and POST requests for authentication"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        email = request.form.get('email').strip().lower()
        debug_header = "\033[1;36m\n=== [AUTH REQUEST] ===\033[0m"  # Bold cyan
        debug_header += f"\n[{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}]"
        debug_header += f"\nEmail: \033[1;33m{email}\033[0m"  # Bold yellow
        print(debug_header)
        print(debug_header)
        current_app.logger.info(f"AUTH: Received request for email: {email}")
        if not email or '@' not in email:
            current_app.logger.warning("AUTH: Invalid email format")
            flash('Please enter a valid email address', 'error')
            return redirect(url_for('auth.auth'))
            
        user = User.query.filter_by(email=email).first()
        
        if not user:
            if current_app.config.get('ENV') == 'development':
                # Auto-create user in development for testing
                current_app.logger.info(f"AUTH: Auto-creating user {email}")
                user = User(email=email, username=email.split('@')[0])
                user.set_password('testpass')
                db.session.add(user)
                db.session.commit()
            else:
                flash('This email is not registered. Please sign up first.', 'warning')
                current_app.logger.info(f"AUTH: Unknown email {email}")
                return redirect(url_for('auth.auth'))
        
        try:
            current_app.logger.info(f"AUTH: Generating token for user {user.email}")
            token = user.generate_auth_token()
            login_url = url_for('auth.verify_token', token=token, _external=True)
            debug_msg = "\033[1;32m=== [TOKEN GENERATED] ===\033[0m"  # Bold green
            debug_msg += f"\nEmail: {user.email}"
            debug_msg += f"\nToken: \033[1;33m{token[:12]}...\033[0m"  # Bold yellow
            debug_msg += f"\nLogin URL: {login_url}"
            debug_msg += "\n\033[1;36m=======================\033[0m\n"
            print(debug_msg)
            current_app.logger.info(f"AUTH: Token generated - {token[:8]}...")
            
            if current_app.config.get('ENV') == 'development':
                # Show debug info in development
                print('\n' + '='*60)
                print(f'DEBUG: Magic login link for {user.email}')
                print(f'DEBUG: {login_url}')
                print('='*60 + '\n')
                flash(f'Development mode: Login link is {login_url}', 'info')
            
            flash('If this email exists in our system, you will receive a login link', 'success')
        except Exception as e:
            current_app.logger.error(f"AUTH ERROR: Token generation failed - {str(e)}")
            flash('An error occurred. Please try again.', 'error')
        
        return redirect(url_for('auth.auth'))
    
    return render_template('auth.html')

@bp.route('/verify/<token>')
def verify_token(token):
    """Verify magic link token and log user in"""
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info')
        return redirect(url_for('main.index'))

    if current_app.config.get('ENV') == 'development':
        debug_header = "\033[1;35m\n=== [TOKEN VERIFICATION] ===\033[0m"  # Bold purple
        debug_header += f"\nToken: \033[1;33m{token[:12]}...\033[0m"
        debug_header += "\n\033[1;35m===========================\033[0m\n"
        print(debug_header)

    current_app.logger.info(f"\n[{(datetime.now()).strftime('%Y-%m-%d %H:%M:%S')}] VERIFY: Checking token {token[:8]}...")

    # Find unused token
    token_obj = AuthToken.query.filter_by(token=token, used=False).first()

    if not token_obj or not token_obj.is_valid():
        current_app.logger.warning(f"VERIFY: Invalid token - exists:{bool(token_obj)}, valid:{token_obj.is_valid() if token_obj else False}")
        flash('Invalid or expired login link.', 'error')
        return redirect(url_for('auth.auth'))

    try:
        # Mark token as used
        token_obj.used = True
        db.session.commit()

        # Properly log the user in and commit session
        current_app.logger.info(f"VERIFY: Logging in user {token_obj.user.email}")
        login_user(token_obj.user, remember=True)
        db.session.commit()  # Ensure session is persisted
        
        if current_app.config.get('ENV') == 'development':
            current_app.logger.debug(f"VERIFY DEBUG: Session after login - {session}")
            print('\n' + '='*60)
            print('DEBUG: Session data after login:', session)
            print('='*60 + '\n')
            print('\n' + '='*60)
            print(f'DEBUG: Logged in user {token_obj.user.email}')
            print('='*60 + '\n')

        flash('Successfully logged in!', 'success')
        return redirect(url_for('main.index'))

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Token verification failed: {str(e)}")
        flash('Login failed. Please try again.', 'error')
        return redirect(url_for('auth.auth'))

# Consider changing to POST for better CSRF protection
# @bp.route('/logout', methods=['POST'])
@bp.route('/logout')
def logout():
    """Log out current user"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))

