# Docker Usage
This guide shows general setup and usage with docker for this project. 
I split the different sections (frontend/backend) into their respective docker containers and have an image orchestration process down with docker-compose that uses a postgres image for the db in production. I will first show how to install Docker/Docker-Compose and then move on to how to use it with this specific project in deploy_steps.md. see [deploy_steps.md](deploy_steps.md) for more info on the deployment commands if you already have docker and docker-compose on your system. 

## Prerequisites

Ensure Docker and Docker Compose are installed on your system. If not, download and install them from [Docker's official website](https://www.docker.com/get-started).

## Basic Commands

### 1. **Create and Start Services**

Create and start services defined in the `docker-compose.yml` file:
```bash
docker-compose build -d
```
###
```bash
docker-compose up -d
```
### 2. Stop the services, bring down the api and db
```bash
docker-compose down
```

### 3. Check the status of the various services. 
```bash
docker-compose ps
```

### Install Docker on WSL Ubuntu using apt-get:
(may not be entirely accurate, platform dependent. If you need to install on normal linux distro look up guide.)

1. **Update Package Lists:**
   Open your terminal and run:

   ```bash
   sudo apt-get update
   ```

2. **Install Docker Dependencies:**
   Install packages to allow apt to use a repository over HTTPS:

   ```bash
   sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
   ```

3. **Add Docker GPG Key:**
   Add Docker's official GPG key:

   ```bash
   sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   ```

4. **Set Up Stable Docker Repository:**
   Set up the stable Docker repository:

   ```bash
   echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

5. **Install Docker:**
   Update the package lists and install Docker:

   ```bash
   sudo apt-get update
   sudo apt-get install -y docker-ce docker-ce-cli containerd.io
   ```

6. **Verify Docker Installation:**
   Check if Docker is installed correctly by running:

   ```bash
   docker --version
   ```

   You should see the Docker version information.

7. **Start Docker on Boot:**
   Start Docker and enable it to start on boot:

   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

### Install Docker Compose on Ubuntu using apt-get:

1. **Install Docker Compose:**
   Use `apt-get` to install Docker Compose:

   ```bash
   sudo apt-get install -y docker-compose
   ```

2. **Verify Docker Compose Installation:**
   Check if Docker Compose is installed correctly by running:

   ```bash
   docker-compose --version
   ```

   You should see the Docker Compose version information.



