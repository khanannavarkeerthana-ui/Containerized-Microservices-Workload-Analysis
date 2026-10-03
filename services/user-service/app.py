from fastapi import FastAPI

app = FastAPI(title="User Service")


users = {
    1: {
        "id": 1,
        "name": "Sukanya",
        "email": "sukanya@example.com"
    },
    2: {
        "id": 2,
        "name": "Rahul",
        "email": "rahul@example.com"
    }
}


@app.get("/")
def home():
    return {
        "service": "User Service",
        "status": "running"
    }


@app.get("/users/{user_id}")
def get_user(user_id: int):

    if user_id not in users:
        return {
            "error": "User not found"
        }

    return users[user_id]