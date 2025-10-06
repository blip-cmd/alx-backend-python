# Jenkins Configuration Instructions

This document provides detailed instructions for setting up Jenkins for the messaging app CI/CD pipeline.

## Prerequisites

### 1. Install Jenkins in Docker Container

```bash
# Run Jenkins in Docker container (as specified in requirements)
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

### 2. Initial Jenkins Setup

1. **Access Jenkins**: Navigate to `http://localhost:8080`
2. **Get Initial Password**: 
   ```bash
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
3. **Install Suggested Plugins**: Choose "Install suggested plugins"
4. **Create Admin User**: Set up your admin credentials

## Required Plugins Installation

Navigate to **Manage Jenkins > Manage Plugins > Available** and install:

1. **Git plugin** - For source code management
2. **Pipeline plugin** - For pipeline support  
3. **ShiningPanda Plugin** - For Python/Virtual environment support
4. **HTML Publisher plugin** - For coverage reports
5. **JUnit plugin** - For test result publishing
6. **Docker Pipeline plugin** - For Docker operations

### Installing Plugins via Jenkins CLI (Alternative)

```bash
# Download Jenkins CLI
docker exec jenkins wget http://localhost:8080/jnkins/cli/jenkins-cli.jar

# Install plugins
docker exec jenkins java -jar jenkins-cli.jar -s http://localhost:8080/ -auth admin:password install-plugin git pipeline-stage-view shiningpanda htmlpublisher junit docker-workflow
```

## Pipeline Setup

### 1. Create New Pipeline Job

1. **New Item** > **Pipeline** > Enter name "messaging-app-pipeline"
2. **Configure Pipeline**:
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: `https://github.com/blip-cmd/alx-backend-python.git`
   - **Script Path**: `messaging_app/Jenkinsfile`

### 2. Configure GitHub Credentials

1. **Manage Jenkins > Manage Credentials**
2. **Global credentials > Add Credentials**
3. **Kind**: Username with password
4. **Username**: Your GitHub username
5. **Password**: GitHub Personal Access Token
6. **ID**: `github-credentials`

### 3. Configure Docker Hub Credentials

1. **Manage Jenkins > Manage Credentials**
2. **Global credentials > Add Credentials** 
3. **Kind**: Username with password
4. **Username**: Your Docker Hub username
5. **Password**: Docker Hub Access Token
6. **ID**: `docker-hub-credentials`

## Pipeline Configuration Details

### Environment Variables
The Jenkinsfile uses these environment variables:

```groovy
environment {
    DOCKER_HUB_REPO = 'your-dockerhub-username/messaging-app'
    DOCKER_HUB_CREDENTIALS = credentials('docker-hub-credentials')
}
```

**Update Required**: Replace `your-dockerhub-username` with your actual Docker Hub username.

### Pipeline Stages

1. **Checkout**: Pulls code from GitHub
2. **Setup Environment**: Creates Python virtual environment
3. **Code Quality Check**: Runs flake8 linting
4. **Run Tests**: Executes pytest with coverage
5. **Build Docker Image**: Creates container image
6. **Push Docker Image**: Publishes to Docker Hub

## Manual Trigger Setup

### Via Jenkins UI
1. Navigate to your pipeline job
2. Click **"Build Now"** to manually trigger
3. View **Console Output** for real-time logs

### Via Jenkins API
```bash
# Trigger build via API
curl -X POST http://admin:password@localhost:8080/job/messaging-app-pipeline/build
```

## Build Artifacts and Reports

### Test Reports
- **JUnit XML**: `messaging_app/test-reports/junit.xml`
- **Coverage HTML**: `messaging_app/htmlcov/index.html`
- **Flake8 Report**: `messaging_app/flake8-report.xml`

### HTML Publisher Configuration
The pipeline automatically publishes HTML coverage reports:

```groovy
publishHTML([
    allowMissing: false,
    alwaysLinkToLastBuild: true,
    keepAll: true,
    reportDir: 'messaging_app/htmlcov',
    reportFiles: 'index.html',
    reportName: 'Coverage Report'
])
```

## Troubleshooting

### Common Issues

1. **Permission Denied - Docker**
   ```bash
   # Add jenkins user to docker group
   docker exec -u root jenkins usermod -aG docker jenkins
   docker restart jenkins
   ```

2. **Python Virtual Environment Issues**
   ```bash
   # Install Python 3 in Jenkins container
   docker exec -u root jenkins apt-get update
   docker exec -u root jenkins apt-get install -y python3 python3-venv python3-pip
   ```

3. **Git Credentials Issues**
   - Verify GitHub credentials in Jenkins
   - Check repository permissions
   - Use Personal Access Token instead of password

4. **Docker Hub Push Failures**
   - Verify Docker Hub credentials
   - Check repository exists and permissions
   - Ensure access token has write permissions

### Debug Commands

```bash
# Check Jenkins logs
docker logs jenkins

# Access Jenkins container
docker exec -it jenkins bash

# Check available plugins
docker exec jenkins java -jar jenkins-cli.jar -s http://localhost:8080/ list-plugins
```

## Security Best Practices

1. **Use HTTPS**: Configure SSL for Jenkins
2. **Regular Updates**: Keep Jenkins and plugins updated
3. **Access Control**: Configure proper user permissions
4. **Secret Management**: Use Jenkins credentials store
5. **Backup**: Regular backup of jenkins_home volume

## Monitoring and Notifications

### Email Notifications
Configure in **Manage Jenkins > Configure System > E-mail Notification**

### Slack Integration
Install Slack Notification plugin and configure webhook

### Build Status Badge
Add to repository README:
```markdown
[![Build Status](http://localhost:8080/buildStatus/icon?job=messaging-app-pipeline)](http://localhost:8080/job/messaging-app-pipeline/)
```

## Performance Optimization

1. **Build Caching**: Use Docker layer caching
2. **Parallel Execution**: Configure parallel test execution
3. **Resource Allocation**: Adjust JVM heap size
4. **Cleanup**: Configure build retention policies

```bash
# Increase Jenkins heap size
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 \
  -e JAVA_OPTS="-Xmx2048m" \
  -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

## Testing the Pipeline

1. **Make a Code Change**: Modify a file in the repository
2. **Commit and Push**: Push changes to GitHub
3. **Manual Trigger**: Click "Build Now" in Jenkins
4. **Monitor Progress**: Watch the build stages in real-time
5. **Review Reports**: Check test results and coverage reports
6. **Verify Docker Image**: Confirm image was pushed to Docker Hub

The complete pipeline should execute successfully, running tests, generating reports, building the Docker image, and pushing it to Docker Hub.