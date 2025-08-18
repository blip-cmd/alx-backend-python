# CI/CD Pipeline Setup Guide

This repository includes comprehensive CI/CD pipelines using both Jenkins and GitHub Actions for the Django messaging application.

## Overview

The project implements all required tasks:

1. **Jenkins Pipeline** - Complete CI/CD with testing, quality checks, and Docker builds
2. **GitHub Actions Testing** - Automated testing with MySQL database
3. **GitHub Actions Code Quality** - Strict linting and coverage reporting
4. **GitHub Actions Deployment** - Docker image building and pushing

## Files Structure

```
messaging_app/
├── Jenkinsfile                    # Jenkins pipeline configuration
├── .github/workflows/
│   ├── ci.yml                     # Testing and code quality workflow
│   └── dep.yml                    # Docker deployment workflow
├── pytest.ini                    # Pytest configuration
├── setup.cfg                     # Flake8 configuration
├── requirements.txt               # Python dependencies
└── Dockerfile                    # Production-ready container
```

## Jenkins Setup (Task 0 & 1)

### Prerequisites
1. Jenkins server with Docker support
2. Git plugin installed
3. Pipeline plugin installed
4. ShiningPanda plugin for Python support

### Pipeline Features
- **Source Code Management**: Pulls from GitHub repository
- **Environment Setup**: Creates Python virtual environment
- **Code Quality**: Runs flake8 linting with JUnit output
- **Testing**: Executes pytest with coverage reports
- **Docker Build**: Creates container images
- **Docker Push**: Publishes to Docker Hub

### Required Jenkins Credentials
- `docker-hub-credentials`: Docker Hub username/password

### Manual Trigger
Navigate to your Jenkins job and click "Build Now" to manually trigger the pipeline.

## GitHub Actions Setup (Tasks 2, 3 & 4)

### CI Workflow (.github/workflows/ci.yml)
**Triggers**: Push/PR to main, master, develop branches

**Features**:
- Multi-job setup with MySQL service
- Python 3.10 environment
- Dependency caching
- Django migrations
- Comprehensive testing
- Code coverage reporting
- Strict linting enforcement

**Services**:
- MySQL 8.0 database for testing
- Automated database setup

### Deployment Workflow (.github/workflows/dep.yml)
**Triggers**: Push to main/master, tags, releases

**Features**:
- Docker Buildx for multi-platform builds
- Metadata extraction for proper tagging
- Docker Hub publishing
- Security scanning with Trivy
- Layer caching for faster builds

### Required GitHub Secrets
Add these secrets in your repository settings:

```
DOCKER_HUB_USERNAME      # Your Docker Hub username
DOCKER_HUB_ACCESS_TOKEN  # Docker Hub access token (not password)
```

## Local Development

### Setup
```bash
cd messaging_app
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Running Tests
```bash
# Django tests
python manage.py test

# Pytest with coverage
pytest --cov=chats --cov-report=html

# Code quality check
flake8 chats/
black --check chats/
```

### Docker Build
```bash
docker build -t messaging-app .
docker run -p 8000:8000 messaging-app
```

## Configuration Details

### Database Configuration
- Production: MySQL with environment variables
- Testing: SQLite in-memory for speed
- GitHub Actions: MySQL service container

### Code Quality Standards
- Line length: 88 characters (Black standard)
- Flake8 compliance required
- Test coverage reporting
- Automated formatting with Black

### Docker Configuration
- Base: Python 3.10-slim
- Security: Non-root user
- Health checks included
- Multi-stage build optimized

## Monitoring and Reports

### Jenkins Reports
- JUnit test results
- HTML coverage reports
- Flake8 compliance reports
- Build artifacts

### GitHub Actions Artifacts
- Coverage reports (XML and HTML)
- Test results
- Security scan results
- Docker image metadata

## Troubleshooting

### Common Issues

1. **MySQL Connection Issues**
   - Ensure MySQL service is healthy
   - Check environment variables
   - Verify port mapping

2. **Docker Hub Push Failures**
   - Verify credentials are set
   - Check repository permissions
   - Ensure access token has write permissions

3. **Test Failures**
   - Check database configuration
   - Verify all dependencies installed
   - Review migration status

### Debug Commands
```bash
# Check Django configuration
python manage.py check --deploy

# Test database connection
python manage.py dbshell

# View migration status
python manage.py showmigrations
```

## Next Steps

1. **Jenkins Setup**: Install Jenkins with required plugins
2. **GitHub Secrets**: Add Docker Hub credentials
3. **Repository Configuration**: Set up branch protection rules
4. **Monitoring**: Configure notifications for failed builds
5. **Production**: Set up proper database and environment variables