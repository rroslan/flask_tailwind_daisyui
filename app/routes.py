from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import current_app
from app.email import send_email

# Initialize blueprint
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Render the home page"""
    return render_template('index.html')

@bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Handle contact form submissions"""
    if request.method == 'POST':
        try:
            # Get and validate form data
            name = request.form.get('name', '').strip()
            contact_info = request.form.get('contact_info', '').strip()
            message = request.form.get('message', '').strip()
            
            # Validate required fields
            if not all([name, contact_info, message]):
                flash('Please fill all required fields', 'error')
                return redirect(url_for('main.contact'))
            
            # Validate contact info format
            if '@' in contact_info:  # Email validation
                if '.' not in contact_info.split('@')[-1]:
                    raise ValueError('Please enter a valid email address')
            elif contact_info.startswith('+'):  # Phone validation
                if not contact_info[1:].isdigit():
                    raise ValueError('Phone number should only contain numbers after +')
            else:
                raise ValueError('Please provide either email or phone number')
            
            # Prepare and send email
            email_body = f"""
            <h2>New Contact Form Submission</h2>
            <p><strong>Name:</strong> {name}</p>
            <p><strong>Contact Info:</strong> {contact_info}</p>
            <p><strong>Message:</strong></p>
            <p>{message}</p>
            """
            
            send_email(
                recipient='rroslan@gmail.com',
                subject=f'New Contact from {name}',
                body=email_body
            )
            
            flash('Your message has been sent successfully!', 'success')
            return redirect(url_for('main.contact_success'))
            
        except ValueError as e:
            flash(str(e), 'error')
            return redirect(url_for('main.contact'))
            
        except Exception as e:
            current_app.logger.error(f'Contact form error: {str(e)}', exc_info=True)
            flash('An error occurred. Please try again later.', 'error')
            return redirect(url_for('main.contact'))
    
    return render_template('contact.html')

@bp.route('/contact/success')
def contact_success():
    """Display success page after contact form submission"""
    return render_template('contact_success.html')
