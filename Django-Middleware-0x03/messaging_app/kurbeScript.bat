@echo off
REM kurbeScript.bat - Kubernetes Setup and Verification Script (Batch)
REM This script sets up a local Kubernetes cluster using Minikube on Windows

setlocal enabledelayedexpansion

echo ==========================================
echo Kubernetes Local Cluster Setup Script
echo ==========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [WARNING] This script may require administrator privileges for installation.
    echo [INFO] If installation fails, please run Command Prompt as Administrator.
    echo.
)

REM Function to check if a command exists
:check_command
where %1 >nul 2>&1
exit /b %errorlevel%

REM Check if Minikube is installed
echo [INFO] Checking if Minikube is installed...
call :check_command minikube
if %errorlevel% neq 0 (
    echo [WARNING] Minikube is not installed.
    set /p install_minikube="Would you like to install Minikube using winget? (y/n): "
    if /i "!install_minikube!"=="y" (
        echo [INFO] Installing Minikube...
        where winget >nul 2>&1
        if !errorlevel! equ 0 (
            winget install -e --id Kubernetes.minikube
        ) else (
            echo [ERROR] winget not found. Please install Minikube manually:
            echo 1. Download from: https://minikube.sigs.k8s.io/docs/start/
            echo 2. Or use Windows Package Manager: winget install minikube
            pause
            exit /b 1
        )
    ) else (
        echo [ERROR] Minikube is required to proceed. Exiting.
        pause
        exit /b 1
    )
) else (
    echo [SUCCESS] Minikube is already installed.
    minikube version
)

echo.

REM Check if kubectl is installed
echo [INFO] Checking if kubectl is installed...
call :check_command kubectl
if %errorlevel% neq 0 (
    echo [WARNING] kubectl is not installed.
    set /p install_kubectl="Would you like to install kubectl using winget? (y/n): "
    if /i "!install_kubectl!"=="y" (
        echo [INFO] Installing kubectl...
        where winget >nul 2>&1
        if !errorlevel! equ 0 (
            winget install -e --id Kubernetes.kubectl
        ) else (
            echo [ERROR] winget not found. Please install kubectl manually:
            echo 1. Download from: https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/
            echo 2. Or use Windows Package Manager: winget install kubectl
            pause
            exit /b 1
        )
    ) else (
        echo [ERROR] kubectl is required to proceed. Exiting.
        pause
        exit /b 1
    )
) else (
    echo [SUCCESS] kubectl is already installed.
    kubectl version --client
)

echo.

REM Start Minikube cluster
echo [INFO] Starting Minikube cluster...
minikube status | findstr "host: Running" >nul 2>&1
if %errorlevel% equ 0 (
    echo [SUCCESS] Minikube cluster is already running.
) else (
    echo [INFO] Starting new Minikube cluster...
    minikube start --driver=docker --memory=4096 --cpus=2
    if !errorlevel! equ 0 (
        echo [SUCCESS] Minikube cluster started successfully!
    ) else (
        echo [ERROR] Failed to start Minikube cluster.
        echo [INFO] Try running: minikube start --driver=hyperv
        echo [INFO] Or install Docker Desktop and try again.
        pause
        exit /b 1
    )
)

echo.

REM Verify cluster is running
echo [INFO] Verifying that the cluster is running...
echo ----------------------------------------
echo Cluster Information:
echo ----------------------------------------
kubectl cluster-info
if %errorlevel% equ 0 (
    echo [SUCCESS] Cluster is running and accessible!
) else (
    echo [ERROR] Failed to connect to cluster.
    pause
    exit /b 1
)

echo.
echo ----------------------------------------
echo Node Information:
echo ----------------------------------------
kubectl get nodes

echo.
echo ----------------------------------------
echo Cluster Status:
echo ----------------------------------------
minikube status

echo.

REM Retrieve available pods
echo [INFO] Retrieving available pods...
echo ----------------------------------------
echo Pods in all namespaces:
echo ----------------------------------------
kubectl get pods --all-namespaces

echo.
echo ----------------------------------------
echo Pods in default namespace:
echo ----------------------------------------
kubectl get pods

if %errorlevel% equ 0 (
    echo [SUCCESS] Successfully retrieved pod information!
) else (
    echo [WARNING] Could not retrieve pods (this is normal for a new cluster).
)

echo.

REM Create sample deployment (optional)
set /p create_sample="Would you like to create a sample deployment for testing? (y/n): "
if /i "!create_sample!"=="y" (
    echo [INFO] Creating a sample deployment for testing...
    
    REM Create a simple nginx deployment
    kubectl create deployment hello-minikube --image=nginx:latest --port=80
    
    REM Wait for deployment to be ready
    echo [INFO] Waiting for deployment to be ready...
    kubectl wait --for=condition=available --timeout=300s deployment/hello-minikube
    
    REM Expose the deployment
    kubectl expose deployment hello-minikube --type=NodePort --port=80
    
    echo [SUCCESS] Sample deployment created and exposed!
    
    echo.
    echo ----------------------------------------
    echo Sample Deployment Status:
    echo ----------------------------------------
    kubectl get deployments
    kubectl get services
    kubectl get pods
)

echo.

REM Display useful commands
echo ==========================================
echo Useful Kubernetes Commands:
echo ==========================================
echo • Check cluster status: kubectl cluster-info
echo • Get all pods: kubectl get pods --all-namespaces
echo • Get nodes: kubectl get nodes
echo • Get services: kubectl get services
echo • Get deployments: kubectl get deployments
echo • Minikube dashboard: minikube dashboard
echo • Stop Minikube: minikube stop
echo • Delete Minikube cluster: minikube delete
echo • Minikube status: minikube status
echo • Access service: minikube service hello-minikube
echo ==========================================

echo.
echo [SUCCESS] Kubernetes cluster setup completed successfully!
echo [INFO] Your cluster is ready for use.

pause
exit /b 0
