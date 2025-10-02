# kurbeScript.ps1 - Kubernetes Setup and Verification Script (PowerShell)
# This script sets up a local Kubernetes cluster using Minikube on Windows

param(
    [switch]$Force,
    [switch]$Help
)

# Display help information
if ($Help) {
    Write-Host @"
kurbeScript.ps1 - Kubernetes Local Cluster Setup Script

DESCRIPTION:
    This script sets up a local Kubernetes cluster using Minikube and verifies it's running.

PARAMETERS:
    -Force      Skip confirmation prompts
    -Help       Display this help message

USAGE:
    .\kurbeScript.ps1           # Interactive mode
    .\kurbeScript.ps1 -Force    # Skip confirmations

REQUIREMENTS:
    - Windows 10/11
    - Docker Desktop (recommended)
    - Administrator privileges (for installation)
"@
    exit 0
}

# Set error action preference
$ErrorActionPreference = "Stop"

# Colors for output
$Colors = @{
    Red = "Red"
    Green = "Green"
    Yellow = "Yellow"
    Blue = "Cyan"
    White = "White"
}

# Function to print colored output
function Write-Status {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Colors.Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[SUCCESS] $Message" -ForegroundColor $Colors.Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Colors.Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Colors.Red
}

# Function to check if running as administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Function to check if a command exists
function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# Function to install Minikube
function Install-Minikube {
    Write-Status "Installing Minikube using winget..."
    
    try {
        # Try winget first
        if (Test-Command "winget") {
            winget install -e --id Kubernetes.minikube
        } else {
            # Fallback to manual download
            Write-Status "winget not available. Downloading Minikube manually..."
            $minikubeUrl = "https://github.com/kubernetes/minikube/releases/latest/download/minikube-windows-amd64.exe"
            $minikubePath = "$env:ProgramFiles\Minikube\minikube.exe"
            
            # Create directory
            New-Item -ItemType Directory -Path "$env:ProgramFiles\Minikube" -Force | Out-Null
            
            # Download Minikube
            Invoke-WebRequest -Uri $minikubeUrl -OutFile $minikubePath
            
            # Add to PATH
            $currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
            if ($currentPath -notlike "*$env:ProgramFiles\Minikube*") {
                [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$env:ProgramFiles\Minikube", "Machine")
                $env:PATH += ";$env:ProgramFiles\Minikube"
            }
        }
        Write-Success "Minikube installed successfully!"
    } catch {
        Write-Error "Failed to install Minikube: $($_.Exception.Message)"
        exit 1
    }
}

# Function to install kubectl
function Install-Kubectl {
    Write-Status "Installing kubectl using winget..."
    
    try {
        if (Test-Command "winget") {
            winget install -e --id Kubernetes.kubectl
        } else {
            # Fallback to manual download
            Write-Status "winget not available. Downloading kubectl manually..."
            $kubectlUrl = "https://dl.k8s.io/release/v1.28.0/bin/windows/amd64/kubectl.exe"
            $kubectlPath = "$env:ProgramFiles\kubectl\kubectl.exe"
            
            # Create directory
            New-Item -ItemType Directory -Path "$env:ProgramFiles\kubectl" -Force | Out-Null
            
            # Download kubectl
            Invoke-WebRequest -Uri $kubectlUrl -OutFile $kubectlPath
            
            # Add to PATH
            $currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
            if ($currentPath -notlike "*$env:ProgramFiles\kubectl*") {
                [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$env:ProgramFiles\kubectl", "Machine")
                $env:PATH += ";$env:ProgramFiles\kubectl"
            }
        }
        Write-Success "kubectl installed successfully!"
    } catch {
        Write-Error "Failed to install kubectl: $($_.Exception.Message)"
        exit 1
    }
}

# Function to check Minikube installation
function Test-Minikube {
    Write-Status "Checking if Minikube is installed..."
    
    if (-not (Test-Command "minikube")) {
        Write-Warning "Minikube is not installed."
        
        if ($Force -or (Read-Host "Would you like to install Minikube? (y/n)") -eq 'y') {
            if (-not (Test-Administrator)) {
                Write-Error "Administrator privileges required for installation. Please run PowerShell as Administrator."
                exit 1
            }
            Install-Minikube
        } else {
            Write-Error "Minikube is required to proceed. Exiting."
            exit 1
        }
    } else {
        Write-Success "Minikube is already installed."
        minikube version
    }
}

# Function to check kubectl installation
function Test-Kubectl {
    Write-Status "Checking if kubectl is installed..."
    
    if (-not (Test-Command "kubectl")) {
        Write-Warning "kubectl is not installed."
        
        if ($Force -or (Read-Host "Would you like to install kubectl? (y/n)") -eq 'y') {
            if (-not (Test-Administrator)) {
                Write-Error "Administrator privileges required for installation. Please run PowerShell as Administrator."
                exit 1
            }
            Install-Kubectl
        } else {
            Write-Error "kubectl is required to proceed. Exiting."
            exit 1
        }
    } else {
        Write-Success "kubectl is already installed."
        kubectl version --client
    }
}

# Function to start Minikube cluster
function Start-MinikubeCluster {
    Write-Status "Starting Minikube cluster..."
    
    try {
        # Check if cluster is already running
        $status = minikube status 2>$null
        if ($status -match "host: Running") {
            Write-Success "Minikube cluster is already running."
        } else {
            Write-Status "Starting new Minikube cluster..."
            minikube start --driver=docker --memory=4096 --cpus=2
            Write-Success "Minikube cluster started successfully!"
        }
    } catch {
        Write-Error "Failed to start Minikube cluster: $($_.Exception.Message)"
        exit 1
    }
}

# Function to verify cluster
function Test-Cluster {
    Write-Status "Verifying that the cluster is running..."
    
    try {
        Write-Host "`n----------------------------------------" -ForegroundColor White
        Write-Host "Cluster Information:" -ForegroundColor White
        Write-Host "----------------------------------------" -ForegroundColor White
        kubectl cluster-info
        Write-Success "Cluster is running and accessible!"
        
        Write-Host "`n----------------------------------------" -ForegroundColor White
        Write-Host "Node Information:" -ForegroundColor White
        Write-Host "----------------------------------------" -ForegroundColor White
        kubectl get nodes
        
        Write-Host "`n----------------------------------------" -ForegroundColor White
        Write-Host "Cluster Status:" -ForegroundColor White
        Write-Host "----------------------------------------" -ForegroundColor White
        minikube status
    } catch {
        Write-Error "Failed to connect to cluster: $($_.Exception.Message)"
        exit 1
    }
}

# Function to get pods
function Get-KubernetesPods {
    Write-Status "Retrieving available pods..."
    
    try {
        Write-Host "`n----------------------------------------" -ForegroundColor White
        Write-Host "Pods in all namespaces:" -ForegroundColor White
        Write-Host "----------------------------------------" -ForegroundColor White
        kubectl get pods --all-namespaces
        
        Write-Host "`n----------------------------------------" -ForegroundColor White
        Write-Host "Pods in default namespace:" -ForegroundColor White
        Write-Host "----------------------------------------" -ForegroundColor White
        kubectl get pods
        
        Write-Success "Successfully retrieved pod information!"
    } catch {
        Write-Warning "Could not retrieve pods (this is normal for a new cluster)."
    }
}

# Function to create sample deployment
function New-SampleDeployment {
    Write-Status "Creating a sample deployment for testing..."
    
    try {
        # Create a simple nginx deployment
        kubectl create deployment hello-minikube --image=nginx:latest --port=80
        
        # Wait for deployment to be ready
        Write-Status "Waiting for deployment to be ready..."
        kubectl wait --for=condition=available --timeout=300s deployment/hello-minikube
        
        # Expose the deployment
        kubectl expose deployment hello-minikube --type=NodePort --port=80
        
        Write-Success "Sample deployment created and exposed!"
        
        Write-Host "`n----------------------------------------" -ForegroundColor White
        Write-Host "Sample Deployment Status:" -ForegroundColor White
        Write-Host "----------------------------------------" -ForegroundColor White
        kubectl get deployments
        kubectl get services
        kubectl get pods
    } catch {
        Write-Warning "Failed to create sample deployment: $($_.Exception.Message)"
    }
}

# Function to show useful commands
function Show-UsefulCommands {
    Write-Host "`n==========================================" -ForegroundColor White
    Write-Host "Useful Kubernetes Commands:" -ForegroundColor White
    Write-Host "==========================================" -ForegroundColor White
    Write-Host "• Check cluster status: kubectl cluster-info" -ForegroundColor Green
    Write-Host "• Get all pods: kubectl get pods --all-namespaces" -ForegroundColor Green
    Write-Host "• Get nodes: kubectl get nodes" -ForegroundColor Green
    Write-Host "• Get services: kubectl get services" -ForegroundColor Green
    Write-Host "• Get deployments: kubectl get deployments" -ForegroundColor Green
    Write-Host "• Minikube dashboard: minikube dashboard" -ForegroundColor Green
    Write-Host "• Stop Minikube: minikube stop" -ForegroundColor Green
    Write-Host "• Delete Minikube cluster: minikube delete" -ForegroundColor Green
    Write-Host "• Minikube status: minikube status" -ForegroundColor Green
    Write-Host "• Access service: minikube service hello-minikube" -ForegroundColor Green
    Write-Host "==========================================" -ForegroundColor White
}

# Main execution function
function Main {
    Write-Host "==========================================" -ForegroundColor White
    Write-Host "Kubernetes Local Cluster Setup Script" -ForegroundColor White
    Write-Host "==========================================" -ForegroundColor White
    Write-Host "Starting Kubernetes setup process...`n"
    
    try {
        # Step 1: Check and install Minikube
        Test-Minikube
        Write-Host ""
        
        # Step 2: Check and install kubectl
        Test-Kubectl
        Write-Host ""
        
        # Step 3: Start the cluster
        Start-MinikubeCluster
        Write-Host ""
        
        # Step 4: Verify cluster is running
        Test-Cluster
        Write-Host ""
        
        # Step 5: Retrieve available pods
        Get-KubernetesPods
        Write-Host ""
        
        # Step 6: Create sample deployment (optional)
        if ($Force -or (Read-Host "Would you like to create a sample deployment for testing? (y/n)") -eq 'y') {
            New-SampleDeployment
            Write-Host ""
        }
        
        # Step 7: Show useful commands
        Show-UsefulCommands
        
        Write-Success "Kubernetes cluster setup completed successfully!"
        Write-Status "Your cluster is ready for use."
        
    } catch {
        Write-Error "Script execution failed: $($_.Exception.Message)"
        exit 1
    }
}

# Run main function
Main
