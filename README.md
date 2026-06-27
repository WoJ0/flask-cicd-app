# Flask CI/CD Pipeline (Jenkins + GitHub + Docker)

A minimal Flask app wired into a Jenkins CI/CD pipeline that, on every push to
GitHub, automatically builds, tests, containerizes, and pushes a Docker image to
Docker Hub (`wojtek0/flask-cicd-app`).

## Project structure
```
flask-cicd-app/
├── app.py            # Flask app (3 routes + add() logic)
├── test_app.py       # pytest unit tests (4 tests)
├── requirements.txt  # Flask + pytest
├── Dockerfile        # Container build
├── Jenkinsfile       # Declarative CI/CD pipeline
├── .dockerignore
└── .gitignore
```

## Pipeline stages (Jenkinsfile)
1. **Checkout** – pull the latest commit from GitHub.
2. **Build / Install deps** – create a venv and install requirements.
3. **Test** – run `pytest`, publish JUnit results.
4. **Build Docker image** – `docker build` tagged with the build number + `latest`.
5. **Push to Docker Hub** – `docker login` with stored credentials, then `docker push`.

---

## Setup steps

### 1. Push this project to GitHub
```bash
cd flask-cicd-app
git init
git add .
git commit -m "Initial commit: Flask CI/CD app"
git branch -M main
git remote add origin https://github.com/<your-github-user>/flask-cicd-app.git
git push -u origin main
```

### 2. Add credentials in Jenkins
Jenkins → **Manage Jenkins → Credentials → System → Global → Add Credentials**

- **Docker Hub**: Kind = *Username with password*
  - Username: `wojtek0`
  - Password: your Docker Hub password or access token
  - **ID: `dockerhub-creds`**  (must match the Jenkinsfile)
- **GitHub** (only if the repo is private): add a Personal Access Token credential
  and select it in the job's SCM config.

### 3. Make sure the Jenkins agent can run Docker
The machine running the build needs the Docker CLI and access to the daemon, and
the `jenkins` user must be in the `docker` group:
```bash
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### 4. Create the pipeline job
Jenkins → **New Item → Pipeline** (or **Multibranch Pipeline**).
- Pipeline → *Pipeline script from SCM*
- SCM = Git, Repository URL = your GitHub repo
- Branch = `main`, Script Path = `Jenkinsfile`
- Save.

### 5. Auto-trigger on push (the "CI" part)
Pick one:

**A. GitHub webhook (recommended)**
- In the job: enable **Build Triggers → GitHub hook trigger for GITScm polling**.
- GitHub repo → **Settings → Webhooks → Add webhook**
  - Payload URL: `http://<your-jenkins-host>:8080/github-webhook/`
  - Content type: `application/json`
  - Event: *Just the push event*.
- (If Jenkins is on localhost, expose it with a tunnel such as ngrok so GitHub
  can reach it.)

**B. Polling fallback**
- Build Triggers → **Poll SCM**, schedule `H/2 * * * *` (every ~2 min).

### 6. Verify
Push any change to `main`. Jenkins should start a build automatically, run the
4 tests, build the image, and push:
```
wojtek0/flask-cicd-app:<build-number>
wojtek0/flask-cicd-app:latest
```
Confirm at https://hub.docker.com/r/wojtek0/flask-cicd-app/tags

## Run locally (optional)
```bash
pip install -r requirements.txt
pytest -v
python app.py            # http://localhost:5000
# or with Docker:
docker build -t wojtek0/flask-cicd-app .
docker run -p 5000:5000 wojtek0/flask-cicd-app
```
