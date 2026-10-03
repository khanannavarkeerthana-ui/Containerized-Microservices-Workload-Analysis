from fastapi import FastAPI
import requests

app = FastAPI(title="Order Service")


USER_SERVICE_URL = "http://user-service:8001"
FOOD_SERVICE_URL = "http://food-service:8002"


@app.get("/")
def home():
    return {
        "service": "Order Service",
        "status": "running"
    }


@app.post("/orders")
def create_order(user_id: int, food_id: int):

    # Get user information
    user_response = requests.get(
        f"{USER_SERVICE_URL}/users/{user_id}"
    )

    # Get food information
    food_response = requests.get(
        f"{FOOD_SERVICE_URL}/foods/{food_id}"
    )

    if user_response.status_code != 200:
        return {
            "error": "Unable to contact User Service"
        }

    if food_response.status_code != 200:
        return {
            "error": "Unable to contact Food Service"
        }

    user = user_response.json()
    food = food_response.json()

    order = {
        "message": "Order created successfully",
        "customer": user,
        "food": food,
        "total_amount": food["price"]
    }

    return order