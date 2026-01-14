#!/bin/bash

# Update pip
python -m pip install --upgrade pip

# Install dependencies
# Note: We use the existing requirements.txt which already lists the CPU versions
pip install -r requirements.txt

# Install Node dependencies and build CSS
if [ -f "package.json" ]; then
    npm install
    npm run build:css
fi

# Run migrations (using SQLite for simplicity in Codespaces)

python manage.py migrate

# Create a superuser automatically (optional, but helpful for testing)
# echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

echo "Environment setup complete! Run 'python manage.py runserver' to start the app."
