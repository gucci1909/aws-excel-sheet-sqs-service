#!/bin/bash
# Setup script for AWS Excel Sheet SQS Service

set -e

echo "Setting up AWS Excel Sheet SQS Service..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install main dependencies
echo "Installing main dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Lambda dependencies
echo "Installing Lambda dependencies..."

# Data Processor Lambda
echo "  - Installing data processor dependencies..."
pip install -r lambdas/data_processor/requirements.txt -t lambdas/data_processor/

# Excel Generator Lambda
echo "  - Installing excel generator dependencies..."
pip install -r lambdas/excel_generator/requirements.txt -t lambdas/excel_generator/

# Check for AWS CDK
if ! command -v cdk &> /dev/null; then
    echo "Warning: AWS CDK CLI not found. Install it with: npm install -g aws-cdk"
    echo "Or visit: https://docs.aws.amazon.com/cdk/latest/guide/getting_started.html"
fi

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Configure AWS credentials: aws configure"
echo "2. Bootstrap CDK (first time only): cdk bootstrap"
echo "3. Deploy infrastructure: cd infrastructure && cdk deploy"
echo "4. Use the QueueUrl from stack outputs to send messages"

