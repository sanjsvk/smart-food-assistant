from pydantic import BaseModel

class FoodItem(BaseModel):
    name: str
    quantity: float
    unit: str