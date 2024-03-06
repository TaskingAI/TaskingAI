from app.models import Model
from app.operators import model_ops


__all__ = ["get_model"]


async def get_model(model_id: str) -> Model:
    return await model_ops.get(model_id=model_id)
