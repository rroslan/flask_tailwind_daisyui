# Flask + Tailwind + DaisyUI Project Setup

## Tech Stack
- **Backend**: Python 3, Flask
- **Frontend**: Tailwind CSS, DaisyUI components
- **Database**: PostgreSQL (Docker)
- **Authentication**: Magic links via Resend email
- **Build Tools**: Node.js, npm, Tailwind CLI

## Initial Setup
```bash
# 1. Clone repository
git clone [your-repo-url]
cd flask_tailwind_daisyui

# 2. Create and activate virtualenv
python -m venv venv
source venv/bin/activate

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Install Node.js/npm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.nvm/nvm.sh
nvm install --lts
nvm use --lts

# 5. Install frontend dependencies
npm install
```

## Configuration
1. Create `.env` file:
```ini
SECRET_KEY=your-generated-key
RESEND_API_KEY=your-resend-key
RESEND_FROM_EMAIL=your@email.com
FLASK_APP=run.py
FLASK_DEBUG=1
```

## Database Setup
**PostgreSQL Docker Container**:
```bash
docker run --name flask-postgres \
  -e POSTGRES_USER=flask_user \
  -e POSTGRES_PASSWORD=flask_password \
  -e POSTGRES_DB=flask_app \
  -p 5432:5432 \
  -v flask-postgres-data:/var/lib/postgresql/data \
  -d postgres:15
```

**Run Migrations**:
```bash
flask db upgrade
```

## Build Processes
- **Development**: `npm run dev` (watches for changes)
- **Production**: `npm run build` (optimized minified CSS)

## Key Commands
```bash
# Start development server
flask run

# Generate new migration
flask db migrate -m "your message"

# Apply migrations
flask db upgrade

# Build frontend assets
npm run build
```

## Project Structure
```
├── app/                  # Flask application
│   ├── auth/             # Authentication routes
│   ├── static/           # Static files
│   │   ├── css/          # Compiled Tailwind
│   │   └── src/          # Tailwind source
│   ├── templates/        # Jinja2 templates  
│   ├── __init__.py       # App factory
│   ├── models.py         # Database models
│   └── routes.py         # Main routes
├── migrations/           # Database migrations
├── venv/                 # Python virtualenv
├── config.py             # Application config
├── run.py                # Entry point
└── tailwind.config.js    # Tailwind config
```

## Contact Form Implementation

### Features
- DaisyUI styled responsive form
- Form validation (required fields, email/phone format)
- Success/error flash messages
- Email sending via Resend service
- Dedicated success page

### Validation Rules
1. **All fields** are required
2. **Email** must contain '@' and valid domain
3. **Phone** must start with '+' and contain only numbers after
4. **Message** has minimum 10 character length

### Email Configuration
```ini
# .env settings
RESEND_API_KEY=your_api_key
RESEND_FROM_EMAIL=your@verified.domain
```

## Updated Route Specifications

| Route | Methods | Description |
|-------|---------|-------------|
| `/` | GET | Home page |
| `/contact` | GET, POST | Contact form |
| `/contact/success` | GET | Form submission success |

## Testing Instructions

1. Test form validation:
```bash
curl -X POST -F "name=Test" -F "contact_info=invalid" -F "message=short" http://localhost:5000/contact
```

2. Verify email sending:
```python
# In flask shell:
from app.email import send_email
send_email('test@example.com', 'Test', '<h1>Test</h1>')
```

## Deployment Notes
- Always run `npm run build` before deploying
- Set `FLASK_DEBUG=0` in production
- Use proper WSGI server (Gunicorn, uWSGI)
- Configure PostgreSQL connection pooling
- Enable HTTPS
- Rotate SECRET_KEY periodically

