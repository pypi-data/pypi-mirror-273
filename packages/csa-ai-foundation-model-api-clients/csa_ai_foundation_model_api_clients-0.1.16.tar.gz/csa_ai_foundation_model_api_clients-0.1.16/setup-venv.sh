#!/bin/bash

# Check if .venv exists, if not, create and activate it
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

echo "Activating the virtual environment..."
source .venv/bin/activate

# Install packages using pip3
echo "Installing required packages..."
pip3 install anthropic --upgrade
pip3 install google-generativeai --upgrade
pip3 install openai --upgrade

echo "Setup complete."
echo ""
echo "Don't forget to run:"
echo ""
echo "source .venv/bin/activate"
