from fastapi import FastAPI

app = FastAPI()

ingredients = {
    "flour": 1000,
    "eggs": 10,
    "yeast": 10,
    "water": 800,
    "salt": 200,
    "sugar": 1000
}


@app.get("/ingredients/{ingredient_name}")
async def get_ingredient(ingredient_name: str):
    return {"ingredient_name": ingredient_name, "quantity": ingredients.get(ingredient_name, 0)}


@app.get("/ingredients")
async def get_all_ingredients():
    return ingredients
