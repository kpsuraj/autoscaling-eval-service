# Problem Statement

We need a service that evaluates the output of LLMs based on given input and criteria. The goal is to build a simple, scalable, and reliable way to validate AI responses in real time at high volume (100+ requests/sec).

## Components

- FastAPI - API server exposing /evaluate

- OpenRouter = Sends prompts to LLM models

- Docker + Minikube -Local containerized deployment on Kubernetes for quick infra spin up for developers

- Locust - Load testing tool

## API Spec

Request:

`POST /evaluate`

Validates size (1KB -1MB)

Sends evaluation prompt to LLM

input, output, criteria: string (required)

Request:

{
  "input": "string",
  "output": "string",
  "criteria": "string"
}

Min size: 1 KB

Max size: 1 MB

Response:

{
  "success": true,
  "explanation": "Yes, this output is correct.",
  "confidence": null // optional
}

## Error Handling

Error                                           Status                                                      Response            

Payload too small (<1KB)                        411                                                     Validation error    
Payload too large (>1MB)                        413                                                      Validation error    
LLM rate-limited (429)                          502                                                      Try again later     
Invalid LLM response                            500                                                      Error explanation   
Missing input fields                            422                                                      Validation response 
Quota exhausted                                 402                                                      Error explanation

## Trade-offs

- LLM via OpenRouter is fast and easy to use, but has rate/credit limits.

- Prompt-based confidence is approximate, not always precise.

- In-memory processing is simple, but not durable under spikes.

- Minikube is easy to run locally but not for real prod loads.


## Machine Requirements

- Dev (local): Python 3.11+, Docker, 4 GB RAM, 2 CPUs

- K8s Pod: 512Mi RAM, 0.5 CPU

- Load Test: 1 CPU to simulate 100 RPS

- Baselining done taking into account of FastApi app + Uvicorn server

- Use kubectl top pod to baseline better during spikes under load

- HPA - Horizontal Pod Autoscaler can be integrated with this too.