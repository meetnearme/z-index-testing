#!/bin/bash


# Check if AWS Cli is already installed
if [ ! -d "/usr/local/aws-cli" ]; then
    echo "Installing AWS CLI v2..."
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
    unzip awscliv2.zip
    ./aws/install
else 
    echo "AWS CLI v2 already installed"
fi

apt-get update
apt-get install jq sed grep -y
xargs --version # make sure xargs is installed already in the container


pip3 install --no-cache-dir -r requirements.txt 

