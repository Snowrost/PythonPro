from fastapi import FastAPI, HTTPException
from httpx import AsyncClient

app = FastAPI()


# Calculate buns based on ingredient data from the first service
async def calculate_buns():
    async with AsyncClient() as client:
        response = await client.get("http://localhost:8000/ingredients")
        ingredient_data = response.json()

    # Adjust the calculation based on the recipe
    flour_quantity = ingredient_data.get("flour", 0)
    yeast_quantity = ingredient_data.get("yeast", 0)
    water_quantity = ingredient_data.get("water", 0)

    buns = min(flour_quantity // 250, yeast_quantity // 5, water_quantity // 200)
    return buns


@app.get("/calculate_buns")
async def get_buns():
    buns = await calculate_buns()
    return {"buns": buns}