import traceback
import random

from locust import HttpUser, task, between


class LocustUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def create_task(self):
        try:
            self.client.post("/api/v1/shorts/short-links",
                                        json={"url": "https://airbridge.io"})

        except:
            print(traceback.format_exc())

    @task
    def get_task(self):
        try:
            short_id_list = ["108", "10C", "10f", "10j", "10Jc", "10L", "10O", "10p", "10y", "10Z"]
            self.client.get(f"/api/v1/shorts/r/{short_id_list[random.randint(0, 9)]}")
        except:
            print(traceback.format_exc())