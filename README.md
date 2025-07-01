# 🌦️ KnoxWeather — Flask + AWS Weather App

> Real-time weather. Minimal design. Powered by Flask, AWS, and OpenWeatherMap.

## 🚀 Tech Stack

<p align="left">
  <img src="https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask" />
  <img src="https://img.shields.io/badge/Amazon_EC2-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white" alt="EC2" />
  <img src="https://img.shields.io/badge/Amazon_S3-569A31?style=for-the-badge&logo=amazonaws&logoColor=white" alt="S3" />
  <img src="https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap" />
  <img src="https://img.shields.io/badge/OpenWeather-FF6C00?style=for-the-badge&logo=openweathermap&logoColor=white" alt="OpenWeather" />
</p>


KnoxWeather is a simple weather web application built using Flask for backend, HTML/CSS/Bootstrap for frontend, and OpenWeatherMap API for live weather data. It is hosted on AWS EC2 (Amazon Linux 2023) with an optional AWS S3 bucket configured for future media/static storage. This project includes all major AWS setup steps and secure deployment using SSH and environment variables.

---

## 📁 Folder Structure

```
KnoxWeather/
├── app.py              # Flask application logic
├── templates/          # HTML files
├── static/             # CSS and JS
├── .env                # API key stored securely
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## 🔧 Features

- Real-time weather data using OpenWeatherMap API 🌍
- Beautiful and responsive frontend using Bootstrap 🎨
- Hosted on AWS EC2 (Amazon Linux 2023) ☁️
- API key stored securely in `.env` file 🔐
- S3 bucket created and ready for future storage needs 🗂️

---

## 🚀 How to Deploy (Step-by-Step)

### ✅ 1. Clone the Repository on Local Machine

```bash
git clone https://github.com/Rupeshs11/KnoxWeather.git
cd KnoxWeather
```

### ✅ 2. Create `.env` File

Inside the project root folder, create `.env`:

```env
API_KEY=your_openweathermap_api_key
```

### ✅ 3. Install Python Requirements

```bash
pip install -r requirements.txt
```

### ✅ 4. Launch AWS EC2 Instance (Amazon Linux 2023)

Follow these detailed steps to launch your EC2 instance and prepare it for deployment:

1. **Login to AWS Console**
   - Visit: https://aws.amazon.com/console/
   - Navigate to the **EC2** dashboard.

2. **Create a VPC (Virtual Private Cloud)**
   - Go to **VPC** → **Create VPC**
   - Choose: "VPC Only"
   - Name: `your-vpc-name`
   - IPv4 CIDR: `10.0.0.0/16`
   - Click **Create VPC**

3. **Create a Subnet**
   - Go to **Subnets** → **Create subnet**
   - Name: `your-subnet-name`
   - VPC: `your-vpc-name`
   - AZ: Select default (e.g., `ap-south-1a`)
   - IPv4 CIDR block: `10.0.1.0/24`
   - Create

4. **Create and Attach Internet Gateway**
   - Go to **Internet Gateways** → **Create**
   - Name: `your-igw-name`
   - Attach to: `your-vpc-name`

5. **Create a Route Table**
   - Go to **Route Tables** → **Create**
   - Name: `your-route-table`
   - VPC: `your-vpc-name`
   - After creation, go to **Routes** → **Edit routes** → **Add route**
     - Destination: `0.0.0.0/0`
     - Target: Select your **Internet Gateway**
   - Go to **Subnet Associations** → **Edit** → Add your subnet

6. **Create a Security Group**
   - Go to **Security Groups** → **Create**
   - Name: `your-security-group`
   - VPC: `your-vpc-name`
   - Inbound Rules:
     - **SSH**: TCP, Port `22`, Source `My IP`
     - **Custom TCP**: Port `5000`, Source `0.0.0.0/0` (to allow Flask app)
   - Outbound Rules: Default (All traffic allowed)

7. **Launch EC2 Instance**
   - Go to **EC2** → **Launch Instance**
   - Name: `your-ec2-name`
   - AMI: Amazon Linux 2023 (Free tier eligible)
   - Instance Type: `t2.micro`
   - Key Pair: Create new or use existing (`your-key.pem`)
   - Network Settings:
     - VPC: `your-vpc-name`
     - Subnet: `your-subnet-name`
     - Auto-assign Public IP: Enabled
     - Security Group: `your-security-group`
   - Click **Launch Instance**

8. **Copy Your EC2 Public IPv4 Address**
   - You'll use this address to SSH into your server and access your Flask app in the browser (e.g., `http://<your-ec2-ip>:5000`)

✅ Your EC2 instance is now ready!


### ✅ 5. SSH into EC2 from Git Bash / terminal

```bash
ssh -i "your-key.pem" ec2-user@your-ec2-public-ip
```


### ✅ 6. Install Python & Git on EC2

```bash
sudo yum update -y
sudo yum install python3 git -y
```

### ✅ 7. Upload Project to EC2 (from local system)

```bash
scp -i "your-key.pem" -r app.py templates static .env requirements.txt ec2-user@your-ec2-public-ip:/home/ec2-user/
```

### ✅ 8. Run Flask App on EC2

```bash
cd ~
pip3 install -r requirements.txt
nohup python3 app.py &
```

> 🔁 Flask will run on `http://0.0.0.0:5000`. Access using:
> `http://your-ec2-public-ip:5000`

> ⚠️ Note: This is suitable for demo/testing. For production, consider using Gunicorn + Nginx for better scalability.


---

## 🗃️ S3 Bucket (Optional)

- Created during initial AWS setup with proper IAM policies
- Used for storing static or media files in future
- Can be used for storing:
  - Weather icons or background images
  - Uploaded media
  - Static assets (if hosting frontend separately)


---

## ❌ Teardown (Optional)

To avoid charges, delete these:

1. EC2 instance
2. Associated VPC, Subnet, IGW, Route Table
3. Security group
4. S3 Bucket

> ⚠️ **Important:** Don't forget to delete your AWS resources to avoid unexpected charges.


---

## 📸 Screenshots

> Add screenshots of your frontend and AWS console here for demo purposes.

---

## 🙌 Acknowledgements

- [Flask](https://flask.palletsprojects.com/)
- [OpenWeatherMap API](https://openweathermap.org/)
- [AWS EC2](https://aws.amazon.com/ec2/)
- [Bootstrap](https://getbootstrap.com/)

---

---

## 💻 Common EC2 Commands (Cheat Sheet)

These commands help you manage the KnoxWeather Flask app on your AWS EC2 instance:

```bash
# 🔐 Connect to EC2 via SSH
ssh -i "weather_APPKEY.pem" ec2-user@<EC2_PUBLIC_IPV4>

# 📤 Upload all project files to EC2
scp -i "weather_APPKEY.pem" -r * ec2-user@<EC2_PUBLIC_IPV4>:/home/ec2-user/

# 🚀 Run Flask app in background (detached)
nohup python3 app.py &

# 📊 Check if port 5000 is in use
sudo lsof -i :5000

# ❌ Kill the process using port 5000 (replace <PID> with actual number)
kill -9 <PID>

# 📄 View Flask output logs
cat nohup.out


---
🛠️ Crafted for the clouds by **Knox** 🚀


