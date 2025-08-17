#!/usr/bin/env bash
# Simple wrapper to execute the appropriate kurbeScript based on the operating system

# Detect OS
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]] || [[ -n "$WINDIR" ]]; then
    # Windows
    echo "Detected Windows system. Running PowerShell script..."
    powershell.exe -ExecutionPolicy Bypass -File "./kurbeScript.ps1"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Detected macOS system. Running bash script..."
    chmod +x ./kurbeScript
    ./kurbeScript
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Detected Linux system. Running bash script..."
    chmod +x ./kurbeScript
    ./kurbeScript
else
    echo "Unsupported operating system: $OSTYPE"
    echo "Please run the appropriate script manually:"
    echo "- Windows: .\kurbeScript.ps1"
    echo "- Linux/macOS: ./kurbeScript"
    exit 1
fi
