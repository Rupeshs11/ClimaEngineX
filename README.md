# 🌦️ ClimaX — Containerized Weather App with Full CI/CD & IaC

> Real-time weather. Dockerized. Terraform-provisioned. Fully automated CI/CD pipeline to AWS.

<!-- Badges -->
<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.12-FFD43B?style=plastic&logo=python&logoColor=blue" alt="Python" /></a>
  <a href="https://flask.palletsprojects.com/"><img src="https://img.shields.io/badge/Flask-2.3-00D4AA?style=plastic&logo=flask&logoColor=white" alt="Flask" /></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-🐳-00BFFF?style=plastic&logo=docker&logoColor=white" alt="Docker" /></a>
  <a href="https://gunicorn.org/"><img src="https://img.shields.io/badge/Gunicorn-WSGI-499848?style=plastic&logo=gunicorn&logoColor=white" alt="Gunicorn" /></a>
</p>

<p align="center">
  <a href="https://github.com/features/actions"><img src="https://img.shields.io/badge/CI%2FCD-GitHub_Actions-FF6F00?style=plastic&logo=githubactions&logoColor=white" alt="GitHub Actions" /></a>
  <a href="https://www.terraform.io/"><img src="https://img.shields.io/badge/IaC-Terraform-844FBA?style=plastic&logo=terraform&logoColor=white" alt="Terraform" /></a>
  <a href="https://aws.amazon.com/ec2/"><img src="https://img.shields.io/badge/Cloud-AWS_EC2-FF9900?style=plastic&logo=amazonec2&logoColor=white" alt="AWS EC2" /></a>
  <a href="https://aws.amazon.com/s3/"><img src="https://img.shields.io/badge/State-AWS_S3-569A31?style=plastic&logo=amazons3&logoColor=white" alt="AWS S3" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Production_Ready-00C853?style=plastic" alt="Status" />
  <img src="https://img.shields.io/badge/License-MIT-A31F34?style=plastic" alt="License" />
  <img src="https://img.shields.io/badge/PRs-Welcome-FF69B4?style=plastic" alt="PRs Welcome" />
</p>

---

## ✨ Highlights

| Feature                       | Description                                         |
| ----------------------------- | --------------------------------------------------- |
| 🐳 **Dockerized**             | Fully containerized with Gunicorn production server |
| 🔄 **CI/CD Pipeline**         | 3-stage pipeline: Build → Provision → Deploy        |
| 🏗️ **Infrastructure as Code** | Terraform provisions EC2, VPC, Security Groups      |
| 📦 **Remote State**           | Terraform state stored in S3 for consistency        |
| 🚀 **One-Click Deploy**       | Push to `main` → Auto deploys to AWS                |
| � **One-Click Destroy**       | Manual workflow to tear down all infrastructure     |
| 🔐 **Secure Secrets**         | All credentials via GitHub Secrets                  |

---

## 🏗️ Architecture

<p align="center">
  <img src="assets/architecture-climax.png" alt="ClimaX Architecture" width="100%"/>
</p>

### Flow

```
Developer pushes code to GitHub (main branch)
  │
  ├─► Job 1: Build & Push Docker image to Docker Hub
  │
  ├─► Job 2: Terraform provisions AWS infrastructure
  │     ├── Creates Default VPC & Security Group (ports 22, 80, 8000)
  │     ├── Launches EC2 instance (t3.micro, Amazon Linux)
  │     ├── Installs Docker via user_data script
  │     ├── Stores state in S3 bucket
  │     └── Outputs EC2 public IP
  │
  └─► Job 3: Deploys Docker container to EC2 via SSH
        ├── Pulls image from Docker Hub
        ├── Runs container on port 80
        └── Passes API key as env variable
```

---

## 📁 Project Structure

```
ClimaX/
├── app.py                         # Flask application
├── Dockerfile                     # Container config
├── .dockerignore                  # Docker exclusions
├── requirements.txt               # Python dependencies
├── templates/
│   └── index.html                 # Weather UI
├── static/
│   └── style.css                  # Styles
├── terraform/
│   ├── ec2.tf                     # EC2, VPC, Security Group
│   ├── variable.tf                # Input variables
│   ├── output.tf                  # EC2 IP output
│   ├── provider.tf                # AWS provider (ap-south-1)
│   └── terraform.tf               # Backend config (S3)
├── assets/
│   └── architecture-climax.png    # Architecture diagram
├── .github/workflows/
│   ├── deploy.yml                 # Build + Terraform + Deploy
│   └── destroy.yml                # Destroy infrastructure
└── README.md
```

---

## 🚀 Quick Start

### Run with Docker

```bash
docker pull yourusername/knoxweather:latest
docker run -d -p 80:5000 -e OPENWEATHER_API_KEY=your_key yourusername/knoxweather:latest
```

### Run Locally

```bash
git clone https://github.com/Rupeshs11/ClimaEngineX.git
cd ClimaEngineX
echo "OPENWEATHER_API_KEY=your_key" > .env
pip install -r requirements.txt
python app.py
```

---

## � CI/CD Pipeline

### `deploy.yml` — 3 Connected Jobs

| Job              | What it does                               |
| ---------------- | ------------------------------------------ |
| **Build & Push** | Builds Docker image → Pushes to Docker Hub |
| **Terraform**    | Provisions EC2, SG, VPC → Outputs EC2 IP   |
| **Deploy**       | SSHs into EC2 → Runs Docker container      |

### `destroy.yml` — Manual Trigger

Tears down all Terraform-managed infrastructure. Run from **Actions** tab → `Destroy Infrastructure` → **Run workflow**.

### Required GitHub Secrets

| Secret                  | Description                  |
| ----------------------- | ---------------------------- |
| `AWS_ACCESS_KEY_ID`     | IAM access key for Terraform |
| `AWS_SECRET_ACCESS_KEY` | IAM secret key for Terraform |
| `EC2_SSH_KEY`           | Private key (`.pem`) for SSH |
| `DOCKERHUB_USERNAME`    | Docker Hub username          |
| `DOCKERHUB_TOKEN`       | Docker Hub access token      |
| `OPENWEATHER_API_KEY`   | OpenWeatherMap API key       |

---

## 🏗️ Terraform (IaC)

### Resources Created

| Resource           | Details                                      |
| ------------------ | -------------------------------------------- |
| **Default VPC**    | Uses existing default VPC                    |
| **Security Group** | Ports 22 (SSH), 80 (HTTP), 8000              |
| **EC2 Instance**   | t3.micro, Amazon Linux, Docker pre-installed |
| **S3 Backend**     | Stores `terraform.tfstate` remotely          |

### Key Commands

```bash
cd terraform
terraform init          # Initialize + connect to S3 backend
terraform plan          # Preview changes
terraform apply         # Create infrastructure
terraform destroy       # Tear down everything
```

---

## 🔧 App Features

| Feature                    | Description                       |
| -------------------------- | --------------------------------- |
| 🌡️ **Real-time Weather**   | Live data from OpenWeatherMap API |
| 🏙️ **City Search**         | Search any city worldwide         |
| 🌅 **Sunrise/Sunset**      | Display sunrise and sunset times  |
| 💨 **Wind Info**           | Speed and direction               |
| 💧 **Humidity & Pressure** | Atmospheric data                  |
| ❤️ **Health Check**        | `/health` endpoint for monitoring |

---

## 🛠️ API Endpoints

| Endpoint    | Method | Description             |
| ----------- | ------ | ----------------------- |
| `/`         | GET    | Weather UI              |
| `/weather`  | POST   | Get weather data (JSON) |
| `/health`   | GET    | Health check            |
| `/test-api` | GET    | Test API config         |

---

## 🤝 Tech Stack

| Technology         | Purpose                 |
| ------------------ | ----------------------- |
| **Flask**          | Web framework           |
| **Gunicorn**       | WSGI server             |
| **Docker**         | Containerization        |
| **Terraform**      | Infrastructure as Code  |
| **GitHub Actions** | CI/CD automation        |
| **Docker Hub**     | Container registry      |
| **AWS EC2**        | Cloud compute           |
| **AWS S3**         | Terraform state storage |
| **OpenWeatherMap** | Weather API             |

---

## 🧹 Cleanup

### Option 1: Automated (Recommended)

Go to **Actions** → `Destroy Infrastructure` → **Run workflow**

### Option 2: Manual

Delete from AWS Console:

- EC2 Instance
- Security Group
- S3 Bucket (if no longer needed)

> ⚠️ **Always terminate unused AWS resources to avoid charges!**

---


<p align="center">
  <i>Push to main. Terraform provisions. Docker deploys. It's that simple.</i>
</p>
