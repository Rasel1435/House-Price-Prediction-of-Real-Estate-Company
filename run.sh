#!/bin/bash

# Define colors for pretty output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Initializing LuxEstate Predictor...${NC}"

# Activate Virtual Environment
if [ -d "venv" ]; then
    echo -e "${GREEN}Activating Virtual Environment...${NC}"
    source venv/bin/activate
else
    echo -e "Virtual environment 'venv' not found. Please create it first."
    exit 1
fi

# Check for required packages
echo -e "${GREEN}📦 Checking dependencies...${NC}"
pip install -q fastapi uvicorn jinja2 python-multipart

# Run the FastAPI Server
echo -e "${BLUE}🌐 Server starting at http://127.0.0.1:8000${NC}"
echo -e "${BLUE}💡 Press CTRL+C to stop the server.${NC}"

python app.py

