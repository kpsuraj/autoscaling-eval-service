
from locust import HttpUser, task, between

payload = {
  "input": "Explain the impact of T20 cricket on traditional forms of the game including One Day Internationals and Test cricket. Consider factors such as fan engagement, viewership, commercial interests, and player skill development. Explain the impact of T20 cricket on traditional forms of the game including One Day Internationals and Test cricket. Consider factors such as fan engagement, viewership, commercial interests, and player skill development. Explain the impact of T20 cricket on traditional forms of the game including One Day Internationals and Test cricket. Consider factors such as fan engagement, viewership, commercial interests, and player skill development. ",
  "output": "T20 cricket has revolutionized the game by introducing a faster-paced format that appeals to a wider audience. While it has increased fan engagement and commercial revenue, some critics argue that it detracts from the strategic depth of Test cricket. The format has encouraged more aggressive batting and innovative bowling techniques. T20 cricket has revolutionized the game by introducing a faster-paced format that appeals to a wider audience. While it has increased fan engagement and commercial revenue, some critics argue that it detracts from the strategic depth of Test cricket. The format has encouraged more aggressive batting and innovative bowling techniques. T20 cricket has revolutionized the game by introducing a faster-paced format that appeals to a wider audience. While it has increased fan engagement and commercial revenue, some critics argue that it detracts from the strategic depth of Test cricket. The format has encouraged more aggressive batting and innovative bowling techniques. ",
  "criteria": "Does the output analyze both the positive and negative impacts of T20 cricket on traditional formats in a balanced and comprehensive manner?"
}

class EvaluateUser(HttpUser):
    wait_time = between(0.01, 0.05)

    @task
    def evaluate(self):
        self.client.post("/evaluate", json=payload)
