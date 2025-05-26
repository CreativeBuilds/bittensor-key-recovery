#!/bin/bash

# Check if .venv directory exists and has the activate script
if [ ! -d ".venv" ] || [ ! -f ".venv/bin/activate" ]; then
    echo "Virtual environment .venv not found or incomplete."
    while true; do
        echo "Do you want to create a new virtual environment using 'python -m venv .venv'? (y/N): "
        read -r response
        case $response in
            [Yy]* ) 
                echo "Creating virtual environment..."
                python -m venv .venv
                if [ $? -eq 0 ]; then
                    echo "Virtual environment created successfully!"
                else
                    echo "Failed to create virtual environment. Please check your Python installation."
                    exit 1
                fi
                break;;
            [Nn]* | "" ) 
                echo "Skipping virtual environment creation."
                exit 1;;
            * ) 
                echo "Please answer y or n.";;
        esac
    done
    source .venv/bin/activate
    
    # Ask about requirements with validation loop
    while true; do
        echo "Do you want to install project requirements? (Y/n): "
        read -r response
        case $response in
            [Yy]* | "" ) 
                echo "Installing project requirements..."
                if [ -f "requirements.txt" ]; then
                    pip install -r requirements.txt
                else
                    echo "No requirements.txt found, skipping installation."
                fi
                break;;
            [Nn]* ) 
                echo "Skipping project requirements installation."
                break;;
            * ) 
                echo "Please answer y or n.";;
        esac
    done
else
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

if [ $? -eq 0 ]; then
    echo "Virtual environment activated successfully!"
    echo "Python path: $(which python)"
    echo "Python version: $(python --version)"
else
    echo "Failed to activate virtual environment."
    exit 1
fi
