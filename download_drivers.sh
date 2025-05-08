#!/bin/bash

# Script to download browser drivers

# Create directory for drivers
mkdir -p drivers

# Get latest ChromeDriver
echo "Downloading latest ChromeDriver..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if [[ "$(uname -m)" == "arm64" ]]; then
        # M1/M2 Mac
        curl -L "https://chromedriver.storage.googleapis.com/LATEST_RELEASE" > latest_release.txt
        CHROME_VERSION=$(cat latest_release.txt)
        curl -L "https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_mac64_m1.zip" -o chromedriver.zip
    else
        # Intel Mac
        curl -L "https://chromedriver.storage.googleapis.com/LATEST_RELEASE" > latest_release.txt
        CHROME_VERSION=$(cat latest_release.txt)
        curl -L "https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_mac64.zip" -o chromedriver.zip
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    curl -L "https://chromedriver.storage.googleapis.com/LATEST_RELEASE" > latest_release.txt
    CHROME_VERSION=$(cat latest_release.txt)
    curl -L "https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip" -o chromedriver.zip
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    curl -L "https://chromedriver.storage.googleapis.com/LATEST_RELEASE" > latest_release.txt
    CHROME_VERSION=$(cat latest_release.txt)
    curl -L "https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_win32.zip" -o chromedriver.zip
fi

# Extract ChromeDriver
unzip -o chromedriver.zip -d drivers/
rm chromedriver.zip latest_release.txt

# Make ChromeDriver executable
chmod +x drivers/chromedriver*

# Get latest GeckoDriver
echo "Downloading latest GeckoDriver..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if [[ "$(uname -m)" == "arm64" ]]; then
        # M1/M2 Mac
        curl -L "https://github.com/mozilla/geckodriver/releases/latest" | grep -o 'href="[^"]*macos-aarch64[^"]*\.tar\.gz"' | head -1 | cut -d'"' -f2 > geckodriver_url.txt
    else
        # Intel Mac
        curl -L "https://github.com/mozilla/geckodriver/releases/latest" | grep -o 'href="[^"]*macos[^"]*\.tar\.gz"' | grep -v 'aarch64' | head -1 | cut -d'"' -f2 > geckodriver_url.txt
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    curl -L "https://github.com/mozilla/geckodriver/releases/latest" | grep -o 'href="[^"]*linux64[^"]*\.tar\.gz"' | head -1 | cut -d'"' -f2 > geckodriver_url.txt
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    curl -L "https://github.com/mozilla/geckodriver/releases/latest" | grep -o 'href="[^"]*win64[^"]*\.zip"' | head -1 | cut -d'"' -f2 > geckodriver_url.txt
fi

# Download GeckoDriver
GECKO_URL="https://github.com$(cat geckodriver_url.txt)"
curl -L "$GECKO_URL" -o geckodriver.tar.gz

# Extract GeckoDriver
if [[ "$GECKO_URL" == *".zip"* ]]; then
    unzip -o geckodriver.tar.gz -d drivers/
else
    tar -xzf geckodriver.tar.gz -C drivers/
fi
rm geckodriver.tar.gz geckodriver_url.txt

# Make GeckoDriver executable
chmod +x drivers/geckodriver*

echo "Drivers downloaded to drivers/ directory"
echo "Add this directory to your PATH or move the drivers to a directory in your PATH"
echo "Example: mv drivers/chromedriver /usr/local/bin/ (may require sudo)"
