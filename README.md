
# LLM Evaluation Service 

his project is a lightweight evaluation service that checks if LLM outputs meet defined criteria. It’s built to handle high request volumes and runs in a local Kubernetes (Minikube) setup.

---

## Features

- Refer to the Design spec doc - `Design.md`
- `POST /evaluate` API to score LLM output based on `input`, `output`, and `criteria`
- Auto-scales to handle high throughput (100+ RPS design)
- Validates payload sizes and handles rate limits gracefully
- Runs in local Minikube for easy testing
- Supports pluggable LLMs via OpenRouter API

---


### Prerequisites

- Python 3.11+
- Docker + Minikube - Minikube to be downloaded and installed as per OS - https://minikube.sigs.k8s.io/docs/start
- `kubectl`

### Local Python (Dev/Test)

- Clone the repo
- Run the below steps
```bash
python -m venv venv -> create a virtual env
source venv/bin/activate   ->activate the virtual env
pip install -r requirements.txt -> install dependencies
uvicorn main:app --reload -> Start Fast API server locally
```
---------

### Deploy on Minikube

1. Download Minikube
2. Make sure docker engine is running on your local env/machine -> use docker desktop or any alternatives
3. Run the below commands after cloning the repo

```bash

minikube start
& minikube -p minikube docker-env --shell powershell | Invoke-Expression  # Windows PowerShell or
eval $(minikube docker-env) # makes sure Minikube uses the local docker engine
docker build -t evaluate-service .
kubectl apply -f k8s/
kubectl port-forward svc/evaluate-service 8000:80

```
4. Go to browser and visit http://localhost:8000/docs
5. Test with sample payloads given in test_data folder



To test throughtput scaling, use locust as mentioned below locally. If within minikube, include in dockerimage and deploy it in minikube as a k8 deployment

    1. Install Locust - pip install locust
    2. use the locust file under helper folder with valid payloads over 1KB.
    3. Run locust -f locustfile.py --host=http://localhost:8000
    4. Open http://localhost:8089 and set:

        Host: http://localhost:8000
        Users: 100
        Spawn rate: 10
    5. Locust will send traffic to your FastAPI app through port forwarding.
    6.Reach 100 requests/second and Monitor error rates and LLM 429/500 handling
    7. Change payload content size in locust to try out different behaviors

6. Refer to sample screenshots under `sample_outputs` folder
7. To counter load scaling and throlling issues, HPA can be used in minikube. Run the below cmd if we need to scale based on particular CPU usage. 

    ```bash
    kubectl autoscale deployment evaluate-service --cpu-percent=80 --min=1 --max=5
    ```
8. Define min and max number of pods for autoscale.
9. Use ```kubectl top pod``` to monitor  
## Bonus:

In best interest of time, I am not able to work on bonus segment of the assignment. I also would require to read up a little to work on the bonus segment of the assessment.

If more time permits, I would work on the bonus segment, provid a production grade k8s deployment pipeline in EKS to handle scale.
