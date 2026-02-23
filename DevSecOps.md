# ClimaEngineX (knoxweather) DevOps Project Guide

This guide contains every single step, command, and configuration required to transform the `knoxweather` project into a full Enterprise-grade DevOps pipeline using **Jenkins, SonarQube, Trivy, Amazon EKS, and ArgoCD**.

---

## Prerequisites

Before you start, ensure you have the following on your local machine / AWS CloudShell:
- AWS CLI configured (`aws configure` with an IAM user that has Admin permissions)
- Terraform installed
- `eksctl` installed
- `kubectl` installed
- A DockerHub account
- A GitHub account

---

## Phase 1: Provision Support Infrastructure (Terraform)

We need to create the Jenkins and SonarQube servers.

1. Navigate to your Terraform directory:
   ```bash
   cd terraform
   ```

2. Assuming you have updated [ec2.tf](file:///d:/projects/AWS_projects/knoxweather/terraform/ec2.tf) and the `scripts/` folder as per the Implementation Plan:
   ```bash
   terraform init
   terraform plan
   terraform apply --auto-approve
   ```

3. Note down the Public IPs from the Terraform output:
   - **Jenkins IP**: `http://<JENKINS_IP>:8080`
   - **SonarQube IP**: `http://<SONARQUBE_IP>:9000`

---

## Phase 2: SonarQube Setup

1. Open a browser and go to `http://<SONARQUBE_IP>:9000`.
   - Wait a few minutes if it's not up yet (Docker is pulling the image).
   - Login with: `admin` / `admin`
   - Change your password when prompted.

2. **Create a Project**:
   - Go to **Projects** -> **Create Project** -> **Manually**.
   - Project display name: `knoxweather`
   - Project key: `knoxweather`
   - Setup: Click **Set Up**.

3. **Generate a Token**:
   - Go to **My Account** (top right profile icon) -> **Security**.
   - Under "Generate Tokens", type a name (e.g., `jenkins-token`).
   - Type: `User Token`.
   - Click **Generate**.
   - **COPY THIS TOKEN NOW!** You will need it for Jenkins.

---

## Phase 3: Create EKS Cluster & Install ArgoCD

1. **Create the EKS Cluster**:
   Open your terminal and run (this takes 15-20 minutes):
   ```bash
   eksctl create cluster \
     --name knoxweather-cluster \
     --region ap-south-1 \
     --nodegroup-name standard-workers \
     --node-type t3.medium \
     --nodes 2 \
     --managed
   ```

2. **Verify Cluster Access**:
   ```bash
   kubectl get nodes
   ```
   *You should see two nodes in `Ready` state.*

3. **Create the GitOps Repository**:
   - Go to GitHub and create a NEW, empty repository named `knoxweather-k8s-manifests`.
   - Add the `deployment.yaml` and `service.yaml` files (from the Implementation Plan) to this new repo.

4. **Install ArgoCD**:
   ```bash
   kubectl create namespace argocd
   kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
   ```

5. **Expose ArgoCD UI**:
   ```bash
   kubectl patch svc argocd-server -n argocd -p '{"spec": {"type": "LoadBalancer"}}'
   ```

6. **Get ArgoCD Login Info**:
   ```bash
   # Get the Load Balancer URL (Wait a few minutes for it to provision)
   kubectl get svc argocd-server -n argocd -o jsonpath="{.status.loadBalancer.ingress[0].hostname}"

   # Get the Admin Password
   kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
   ```

7. **Configure the ArgoCD Application**:
   - Log into the ArgoCD UI (using the Load Balancer URL, username `admin`, and password from above).
   - Click **+ NEW APP**.
   - **Application Name**: `knoxweather-app`
   - **Project Name**: `default`
   - **SYNC POLICY**: `Automatic` (Check 'Prune Resources' and 'Self Heal')
   - **Repository URL**: `https://github.com/<YOUR_GITHUB_USER>/knoxweather-k8s-manifests.git`
   - **Revision**: `HEAD`
   - **Path**: `.`
   - **Cluster URL**: `https://kubernetes.default.svc`
   - **Namespace**: `default`
   - Click **CREATE**.

---

## Phase 4: Jenkins Setup

1. Open `http://<JENKINS_IP>:8080`.
2. Extract the initial admin password from the Jenkins server:
   ```bash
   # SSH into Jenkins server
   ssh -i sage.pem ec2-user@<JENKINS_IP>
   sudo cat /var/lib/jenkins/secrets/initialAdminPassword
   ```
3. Paste the password into the UI, click **Install suggested plugins**, and create your Admin user.

### 4.1 Install Additional Plugins
1. Go to **Manage Jenkins** -> **Plugins** -> **Available plugins**.
2. Search for and check the following:
   - `SonarQube Scanner`
   - `Docker Pipeline`
3. Click **Install without restart**.

### 4.2 Add Credentials to Jenkins
Go to **Manage Jenkins** -> **Credentials** -> **System** -> **Global credentials (unrestricted)**. Add the following three:

1. **DockerHub**:
   - Kind: `Username with password`
   - Username: `<Your DockerHub Username>`
   - Password: `<Your DockerHub Access Token or Password>`
   - ID: `dockerhub-creds`

2. **SonarQube Token**:
   - Kind: `Secret text`
   - Secret: `<The SonarQube Token you generated earlier>`
   - ID: `sonar-token`

3. **GitHub Personal Access Token (PAT)**:
   - *First, go to GitHub -> Settings -> Developer Settings -> Personal access tokens (Tokens classic) -> Generate new token (Give it `repo` scope).*
   - Kind: `Username with password`
   - Username: `<Your GitHub Username>`
   - Password: `<Your GitHub PAT>`
   - ID: `github-creds`

### 4.3 Configure SonarQube in Jenkins
1. Go to **Manage Jenkins** -> **System**.
2. Scroll down to **SonarQube servers**.
3. Check `Environment variables`.
4. Click **Add SonarQube**.
   - Name: `sonarqube-server`
   - Server URL: `http://<SONARQUBE_IP>:9000`
   - Server authentication token: Select the `sonar-token` credential you created.
5. Click **Save**.

6. Go to **Manage Jenkins** -> **Tools**.
7. Scroll to **SonarQube Scanner**.
8. Click **Add SonarQube Scanner**.
   - Name: `sonar-scanner`
   - Check `Install automatically`.
9. Click **Save**.

---

## Phase 5: Create the Jenkins Pipeline

1. In the Jenkins dashboard, click **New Item**.
2. Name it `knoxweather-pipeline` and select **Pipeline**. Click OK.
3. Scroll down to the **Build Triggers** section and check:
   - `GitHub hook trigger for GITScm polling`
4. In the **Pipeline** section:
   - Definition: `Pipeline script from SCM`
   - SCM: `Git`
   - Repository URL: `https://github.com/<YOUR_GITHUB_USER>/knoxweather.git`
   - Branch Specifier: `*/main`
   - Script Path: `Jenkinsfile`
5. Click **Save**.

---

## Phase 6: Connect GitHub to Jenkins (Webhook)

For Jenkins to build automatically when you push code, GitHub needs to notify it.

1. Go to your main `knoxweather` GitHub repository.
2. Go to **Settings** -> **Webhooks** -> **Add webhook**.
3. **Payload URL**: `http://<JENKINS_IP>:8080/github-webhook/` *(Don't forget the trailing slash!)*
4. **Content type**: `application/json`
5. **Which events**: `Just the push event`
6. Click **Add webhook**.

---

## Phase 7: Run the Project!

1. Ensure the `Jenkinsfile` from the Implementation Plan is added to the root of your `knoxweather` code repository.
2. Push a small change to your Python code (e.g., add a comment in [app.py](file:///d:/projects/AWS_projects/knoxweather/app.py)).
3. **Watch the magic**:
   - GitHub sends the webhook to Jenkins.
   - Jenkins pulls the code, scans it with SonarQube, runs Trivy, builds the Docker image, and pushes it to DockerHub.
   - Finally, Jenkins pushes a commit to your `knoxweather-k8s-manifests` repository containing the new Image Tag.
   - ArgoCD sees the change in the manifest repo and triggers a rolling update in your EKS cluster!

4. View your application by checking the load balancer URL created by your K8s service:
   ```bash
   kubectl get svc knoxweather-svc -o jsonpath="{.status.loadBalancer.ingress[0].hostname}"
   ```

---

## Phase 8: Cleanup

When you are done experimenting, it is **CRITICAL** to tear everything down so you don't get charged by AWS.

1. **Delete the EKS Cluster**:
   ```bash
   eksctl delete cluster --name knoxweather-cluster --region ap-south-1
   ```

2. **Destroy EC2 Infrastructure**:
   ```bash
   cd terraform
   terraform destroy --auto-approve
   ```
