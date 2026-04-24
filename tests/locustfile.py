# tests/locustfile.py
import os

from locust import HttpUser, between, task

_FORM_DATA = {
    "CRIM": "0.00632",
    "ZN": "18.0",
    "INDUS": "2.31",
    "CHAS": "0",
    "NOX": "0.538",
    "RM": "6.575",
    "AGE": "65.2",
    "DIS": "4.09",
    "RAD": "1",
    "TAX": "296.0",
    "PTRATIO": "15.3",
    "B": "396.9",
    "LSTAT": "4.98",
}


class BostonHousingUser(HttpUser):
    wait_time = between(1, 2)

    @task(1)
    def home(self):
        self.client.get("/")

    @task(2)
    def predict(self):
        self.client.post("/predict", data=_FORM_DATA)
