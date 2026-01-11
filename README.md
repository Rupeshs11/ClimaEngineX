# 🌦️ KnoxWeather — Containerized Weather App with CI/CD

> Real-time weather. Dockerized deployment. Fully automated CI/CD pipeline to AWS.

<!-- Modern 3D Badges -->
<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.12-FFD43B?style=plastic&logo=python&logoColor=blue" alt="Python" /></a>
  <a href="https://flask.palletsprojects.com/"><img src="https://img.shields.io/badge/Flask-2.3-00D4AA?style=plastic&logo=flask&logoColor=white" alt="Flask" /></a>
  <a href="https://www.docker.com/"><img src="https://img.shields.io/badge/Docker-🐳-00BFFF?style=plastic&logo=docker&logoColor=white" alt="Docker" /></a>
  <a href="https://gunicorn.org/"><img src="https://img.shields.io/badge/Gunicorn-WSGI-499848?style=plastic&logo=gunicorn&logoColor=white" alt="Gunicorn" /></a>
</p>

<p align="center">
  <a href="https://github.com/features/actions"><img src="https://img.shields.io/badge/CI%2FCD-GitHub_Actions-FF6F00?style=plastic&logo=githubactions&logoColor=white" alt="GitHub Actions" /></a>
  <a href="https://hub.docker.com/"><img src="https://img.shields.io/badge/Registry-Docker_Hub-066DA5?style=plastic&logo=docker&logoColor=white" alt="Docker Hub" /></a>
  <a href="https://aws.amazon.com/ec2/"><img src="https://img.shields.io/badge/Cloud-AWS_EC2-FF9900?style=plastic&logo=amazonec2&logoColor=white" alt="AWS EC2" /></a>
  <a href="https://openweathermap.org/"><img src="https://img.shields.io/badge/API-OpenWeather-E96E50?style=plastic&logo=openweathermap&logoColor=white" alt="OpenWeather" /></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Production_Ready-00C853?style=plastic" alt="Status" />
  <img src="https://img.shields.io/badge/License-MIT-A31F34?style=plastic" alt="License" />
  <img src="https://img.shields.io/badge/PRs-Welcome-FF69B4?style=plastic" alt="PRs Welcome" />
</p>

---

## ✨ What's New

| Feature | Description |
|---------|-------------|
| 🐳 **Dockerized** | Fully containerized with multi-stage builds |
| 🔄 **CI/CD Pipeline** | Automated build, push & deploy via GitHub Actions |
| 🚀 **One-Click Deploy** | Push to `main` → Auto deploys to EC2 |
| 🔐 **Secure Secrets** | Environment variables via GitHub Secrets |
| ⚡ **Production Ready** | Gunicorn WSGI server |

---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐      ┌─────────────┐
│   GitHub    │ ───▶ │   GitHub     │ ───▶ │  Docker Hub │ ───▶ │   AWS EC2   │
│   (Push)    │      │   Actions    │      │   (Image)   │      │ (Container) │
└─────────────┘      └──────────────┘      └─────────────┘      └─────────────┘
```

---

## 📁 Project Structure

```
KnoxWeather/
├── 📄 app.py                    # Flask application
├── 📄 Dockerfile                # Container configuration
├── 📄 .dockerignore             # Docker build exclusions
├── 📄 requirements.txt          # Python dependencies
├── 📁 templates/
│   └── index.html               # Weather UI template
├── 📁 static/
│   └── style.css                # Custom styles
├── 📁 .github/workflows/
│   └── deploy.yml               # CI/CD pipeline
├── 📄 .env                      # Local environment (not in repo)
└── 📄 README.md                 # You're here!
```

---

## � Quick Start

### Option 1: Run with Docker (Recommended)

```bash
# Pull from Docker Hub
docker pull yourusername/knoxweather:latest

# Run the container
docker run -d -p 80:5000 -e OPENWEATHER_API_KEY=your_api_key yourusername/knoxweather:latest

# Open http://localhost
```

### Option 2: Run Locally

```bash
# Clone the repo
git clone https://github.com/Rupeshs11/KnoxWeather.git
cd KnoxWeather

# Create .env file
echo "OPENWEATHER_API_KEY=your_api_key" > .env

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Open http://localhost:5000
```

---

## 🐳 Docker

### Build Locally

```bash
docker build -t knoxweather .
docker run -p 5000:5000 -e OPENWEATHER_API_KEY=your_key knoxweather
```

### Dockerfile Overview

```dockerfile
FROM python:3.12-slim      # Lightweight Python image
WORKDIR /app               # Set working directory
COPY requirements.txt .    # Copy dependencies
RUN pip install ...        # Install dependencies
COPY . .                   # Copy app code
EXPOSE 5000                # Expose Flask port
CMD ["gunicorn", ...]      # Production server
```

---

## 🔄 CI/CD Pipeline

The project includes a fully automated CI/CD pipeline using GitHub Actions.

### Pipeline Flow

```
Push to main
     │
     ▼
┌─────────────────────────────────┐
│  📦 Build & Push to Docker Hub  │
│  ─────────────────────────────  │
│  • Checkout code                │
│  • Login to Docker Hub          │
│  • Build Docker image           │
│  • Push with :latest tag        │
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  🚀 Deploy to AWS EC2           │
│  ─────────────────────────────  │
│  • SSH into EC2                 │
│  • Pull latest image            │
│  • Stop old container           │
│  • Run new container            │
│  • Cleanup old images           │
└─────────────────────────────────┘
```

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `EC2_HOST` | EC2 public IP address |
| `EC2_USERNAME` | `ec2-user` or `ubuntu` |
| `EC2_SSH_KEY` | Contents of your `.pem` file |
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key |

---

## ☁️ AWS EC2 Setup

### Prerequisites

1. **Launch EC2 Instance**
   - AMI: Amazon Linux 2023 or Ubuntu 22.04
   - Instance Type: `t2.micro` (free tier)
   - Create/use a key pair (`.pem` file)

2. **Security Group Rules**

   | Type | Port | Source |
   |------|------|--------|
   | SSH | 22 | Your IP |
   | HTTP | 80 | 0.0.0.0/0 |

3. **Install Docker on EC2**

   ```bash
   # SSH into EC2
   ssh -i your-key.pem ec2-user@your-ec2-ip

   # Install Docker
   sudo yum update -y
   sudo yum install docker -y
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -aG docker ec2-user

   # Logout and login again
   exit
   ```

---

## 🔧 Features

| Feature | Description |
|---------|-------------|
| 🌡️ **Real-time Weather** | Live data from OpenWeatherMap API |
| 🏙️ **City Search** | Search weather for any city worldwide |
| 🌅 **Sunrise/Sunset** | Display sunrise and sunset times |
| 💨 **Wind Info** | Wind speed and direction |
| 💧 **Humidity** | Current humidity levels |
| 📱 **Responsive** | Works on all devices |
| ❤️ **Health Check** | `/health` endpoint for monitoring |

---

## �️ API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main weather UI |
| `/weather` | POST | Get weather data (JSON) |
| `/health` | GET | Health check endpoint |
| `/test-api` | GET | Test API configuration |

---

## 📊 Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | ✅ Yes |

Get your free API key at [OpenWeatherMap](https://openweathermap.org/api)

---

## 🧹 Cleanup AWS Resources

To avoid unexpected charges, delete these resources:

- [ ] EC2 Instance
- [ ] Security Group
- [ ] Key Pair (optional)
- [ ] VPC (if custom created)

> ⚠️ **Important:** Always terminate unused AWS resources!

---

## 🤝 Tech Stack

| Technology | Purpose |
|------------|---------|
| **Flask** | Web framework |
| **Gunicorn** | WSGI server |
| **Docker** | Containerization |
| **GitHub Actions** | CI/CD automation |
| **Docker Hub** | Container registry |
| **AWS EC2** | Cloud hosting |
| **OpenWeatherMap** | Weather API |

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙌 Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [OpenWeatherMap API](https://openweathermap.org/)
- [Docker](https://www.docker.com/)
- [GitHub Actions](https://github.com/features/actions)
- [AWS EC2](https://aws.amazon.com/ec2/)

---

<p align="center">
  <b>�️ Crafted with ❤️ by Knox 🚀</b>
</p>

<p align="center">
  <i>Push to main. Deploy to cloud. It's that simple.</i>
</p>
