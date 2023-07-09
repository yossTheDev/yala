#!/bin/bash

# Yala Version 
VERSION="v0.1.0"

# Yala Filename 
FILENAME="yala-$VERSION.tar.gz"

# Get latest Yala Release from GitHub
URL="https://github.com/yossTheDev/yala/releases/download/$VERSION/$FILENAME"

# Download
echo Downloadig yala $VERSION
wget $URL

# Descompress File
tar -xzf $FILENAME

# Copy yala to user/bin/ directory
sudo cp yala /usr/bin 

# Delete artifacts
rm yala
rm $FILENAME

# Mostramos un mensaje de éxito
echo "yala is suceffuly installed. Contratulations!!!"