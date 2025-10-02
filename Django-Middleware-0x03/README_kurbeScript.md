# Kubernetes Setup Script (kurbeScript)

This directory contains scripts to set up and verify a local Kubernetes cluster using Minikube.

## Files

- `kurbeScript` - Bash script for Linux/macOS
- `kurbeScript.ps1` - PowerShell script for Windows
- `kurbeScript.bat` - Batch script for Windows (simpler version)

## What the Script Does

1. **Checks Prerequisites**: Verifies if Minikube and kubectl are installed
2. **Installs Missing Components**: Offers to install Minikube and kubectl if not found
3. **Starts Kubernetes Cluster**: Initializes a local Minikube cluster
4. **Verifies Cluster**: Runs `kubectl cluster-info` to confirm the cluster is running
5. **Retrieves Pods**: Lists all available pods in the cluster
6. **Optional Sample Deployment**: Creates a test nginx deployment for verification

## Prerequisites

### Windows
- Windows 10/11
- PowerShell 5.1 or later
- Administrator privileges (for installation)
- Docker Desktop (recommended) or Hyper-V

### Linux/macOS
- Bash shell
- curl
- sudo privileges (for installation)
- Docker or VirtualBox

## Usage

### Windows (PowerShell - Recommended)
```powershell
# Run PowerShell as Administrator for installation
.\kurbeScript.ps1

# Skip confirmation prompts
.\kurbeScript.ps1 -Force

# Get help
.\kurbeScript.ps1 -Help
```

### Windows (Batch)
```cmd
# Double-click kurbeScript.bat or run in Command Prompt
kurbeScript.bat
```

### Linux/macOS (Bash)
```bash
# Make executable
chmod +x kurbeScript

# Run the script
./kurbeScript
```

## What Gets Installed

The script will install (with user permission):

1. **Minikube**: Local Kubernetes cluster manager
   - Windows: via winget or manual download
   - Linux: via curl from official releases
   - macOS: via Homebrew or manual download

2. **kubectl**: Kubernetes command-line tool
   - Windows: via winget or manual download
   - Linux: via curl from official releases
   - macOS: via Homebrew or manual download

## Cluster Configuration

The script starts Minikube with these settings:
- **Driver**: Docker (recommended)
- **Memory**: 4GB
- **CPUs**: 2

## Verification Steps

The script performs these verification steps:

1. **Cluster Info**: `kubectl cluster-info`
2. **Node Status**: `kubectl get nodes`
3. **Minikube Status**: `minikube status`
4. **Pod Listing**: `kubectl get pods --all-namespaces`

## Sample Deployment

If requested, the script creates:
- An nginx deployment named `hello-minikube`
- A NodePort service to expose the deployment
- Waits for the deployment to be ready

## Useful Commands

After setup, you can use these commands:

```bash
# Check cluster status
kubectl cluster-info

# Get all pods
kubectl get pods --all-namespaces

# Get nodes
kubectl get nodes

# Get services
kubectl get services

# Get deployments
kubectl get deployments

# Open Minikube dashboard
minikube dashboard

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete

# Check Minikube status
minikube status

# Access the sample service (if created)
minikube service hello-minikube
```

## Troubleshooting

### Common Issues

1. **Docker not found**: Install Docker Desktop
2. **Permission denied**: Run as Administrator (Windows) or with sudo (Linux/macOS)
3. **Cluster won't start**: Try different driver:
   ```bash
   minikube start --driver=hyperv  # Windows
   minikube start --driver=virtualbox  # Any OS
   ```

### Error Messages

- **"minikube start failed"**: Check Docker is running or try a different driver
- **"kubectl: command not found"**: Restart terminal or add to PATH manually
- **"cluster not accessible"**: Wait a moment and try again, cluster may still be starting

## Requirements Met

This script fulfills the assignment requirements:

✅ **Starts a Kubernetes cluster** using Minikube  
✅ **Verifies cluster is running** using `kubectl cluster-info`  
✅ **Retrieves available pods** using `kubectl get pods`  
✅ **Ensures Minikube is installed** with automatic installation option  

## Additional Features

- Cross-platform support (Windows, Linux, macOS)
- Interactive installation prompts
- Colored output for better readability
- Sample deployment for testing
- Comprehensive verification steps
- Useful command reference
- Error handling and troubleshooting
