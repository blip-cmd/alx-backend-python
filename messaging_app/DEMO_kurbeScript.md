# kurbeScript Demo and Testing Guide

## Testing the Script

Since you have Docker and kubectl already installed, you can test the script functionality. Here's what will happen:

### Current System Status
✅ **Docker**: Installed (version 27.4.0)  
✅ **kubectl**: Installed (version 1.30.5)  
❌ **Minikube**: Not installed (script will offer to install)

### Demo Run

You can run the script in different ways:

#### Option 1: PowerShell (Recommended for Windows)
```powershell
.\kurbeScript.ps1
```

#### Option 2: Batch File (Simple version)
```cmd
kurbeScript.bat
```

#### Option 3: Interactive Help
```powershell
.\kurbeScript.ps1 -Help
```

### What the Script Will Do

1. **Check Minikube**: Will detect it's not installed and offer to install it
2. **Check kubectl**: Will detect it's already installed ✅
3. **Install Minikube**: Uses winget to install if you consent
4. **Start Cluster**: Runs `minikube start --driver=docker --memory=4096 --cpus=2`
5. **Verify Cluster**: Executes `kubectl cluster-info`
6. **List Pods**: Shows pods with `kubectl get pods --all-namespaces`
7. **Optional Sample**: Offers to create a test nginx deployment

### Expected Output Flow

```
==========================================
Kubernetes Local Cluster Setup Script
==========================================

[INFO] Checking if Minikube is installed...
[WARNING] Minikube is not installed.
Would you like to install Minikube? (y/n): y

[INFO] Installing Minikube using winget...
[SUCCESS] Minikube installed successfully!

[INFO] Checking if kubectl is installed...
[SUCCESS] kubectl is already installed.
Client Version: v1.30.5

[INFO] Starting Minikube cluster...
[INFO] Starting new Minikube cluster...
😄  minikube v1.x.x on Windows 11
✨  Using the docker driver based on user configuration
🏃  Starting control plane node minikube in cluster minikube
🚜  Pulling base image ...

[SUCCESS] Minikube cluster started successfully!

[INFO] Verifying that the cluster is running...
----------------------------------------
Cluster Information:
----------------------------------------
Kubernetes control plane is running at https://127.0.0.1:xxxxx
CoreDNS is running at https://127.0.0.1:xxxxx/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy

[SUCCESS] Cluster is running and accessible!

[INFO] Retrieving available pods...
----------------------------------------
Pods in all namespaces:
----------------------------------------
NAMESPACE     NAME                               READY   STATUS    RESTARTS   AGE
kube-system   coredns-xxxx                      1/1     Running   0          1m
kube-system   etcd-minikube                     1/1     Running   0          1m
kube-system   kube-apiserver-minikube           1/1     Running   0          1m
...

[SUCCESS] Successfully retrieved pod information!

Would you like to create a sample deployment for testing? (y/n): y

[INFO] Creating a sample deployment for testing...
[SUCCESS] Sample deployment created and exposed!

==========================================
Useful Kubernetes Commands:
==========================================
• Check cluster status: kubectl cluster-info
• Get all pods: kubectl get pods --all-namespaces
...

[SUCCESS] Kubernetes cluster setup completed successfully!
[INFO] Your cluster is ready for use.
```

### Testing Without Installation

If you want to test the script without actually installing Minikube, you can:

1. Review the script code to understand the logic
2. Run with `-Help` to see the help information
3. Check the script validates Docker is running: `docker ps`

### Manual Testing Steps

You can also manually verify each component the script checks:

```powershell
# Check Docker
docker --version
docker ps

# Check kubectl  
kubectl version --client

# After running the script, verify cluster
kubectl cluster-info
kubectl get nodes
kubectl get pods --all-namespaces
minikube status
```

### Cleanup After Testing

After testing, you can clean up with:

```powershell
# Stop the cluster
minikube stop

# Delete the cluster
minikube delete

# Uninstall Minikube (optional)
winget uninstall Kubernetes.minikube
```

## Assignment Requirements Verification

✅ **Write a script called kurbeScript**: Created in multiple formats  
✅ **Starts a Kubernetes cluster**: Uses `minikube start`  
✅ **Verifies cluster running**: Uses `kubectl cluster-info`  
✅ **Retrieves available pods**: Uses `kubectl get pods`  
✅ **Ensure minikube is installed**: Checks and installs if needed  

The script exceeds requirements by providing:
- Cross-platform support
- Interactive installation
- Error handling
- Sample deployment
- Comprehensive verification
- User-friendly output
