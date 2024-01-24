import traceback

from locust import HttpUser, task, between


class LocustUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def check_task(self):
        try:
            response = self.client.post("/api/v1/shorts/short-links",
                                        json={"url": "https://airbridge.io"})
            short_id = response.json()["shortId"]
            self.client.get(f"/api/v1/shorts/r/{short_id}")
        except:
            print(traceback.format_exc())
