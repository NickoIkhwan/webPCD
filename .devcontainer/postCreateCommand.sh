#!/bin/bash

# Update system and install dependencies for OpenCV
sudo apt-get update && sudo apt-get install -y libgl1

# Update pip
python -m pip install --upgrade pip

# Install dependencies from requirements.txt
# We use the --extra-index-url inside the requirements.txt now
pip install -r requirements.txt

# Install Node dependencies and build CSS if package.json exists
if [ -f "package.json" ]; then
    npm install
    npm run build:css
fi

# Run migrations
python manage.py makemigrations myapp
python manage.py migrate


echo "-------------------------------------------------------"
echo "Environment setup complete!"
echo "To start the application, run:"
echo "python manage.py runserver"
echo "-------------------------------------------------------"
