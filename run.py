#!/usr/bin/env python3
from app import create_app

app = create_app()

if __name__ == '__main__':
    import os
    from dotenv import load_dotenv
    
    # Load environment variables
    load_dotenv()
    
    # Run the application
    app.run(host=os.environ.get('FLASK_HOST', '127.0.0.1'),
            port=int(os.environ.get('FLASK_PORT', 5000)),
            debug=os.environ.get('FLASK_DEBUG', 'true').lower() == 'true')

