from fastapi import FastAPI

app = FastAPI(title="Food Service")


foods = {
    1: {
        "id": 1,
        "name": "Veg Burger",
        "price": 120,
        "category": "Burger"
    },
    2: {
        "id": 2,
        "name": "Pizza",
        "price": 250,
        "category": "Pizza"
    },
    3: {
        "id": 3,
        "name": "Masala Dosa",
        "price": 100,
        "category": "South Indian"
    }
}


@app.get("/")
def home():
    return {
        "service": "Food Service",
        "status": "running"
    }


@app.get("/foods/{food_id}")
def get_food(food_id: int):

    if food_id not in foods:
        return {
            "error": "Food item not found"
        }

    return foods[food_id]


@app.get("/foods")
def get_all_foods():
    return list(foods.values())