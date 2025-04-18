#!/bin/bash

# Enable exit on error and print commands
set -e -x

# Install Git LFS if not already installed
if ! command -v git-lfs &> /dev/null; then
    sudo apt-get install git-lfs -y
fi

# Initialize and pull LFS files
git lfs install
git lfs pull

# Create and activate virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Additional build steps if needed
# python manage.py collectstatic --noinput  # For Django projects