from app.models import Model

__all__ = ["get_model"]


async def get_model(model_id: str) -> Model:
    from app.operators import model_ops

    return await model_ops.get(model_id=model_id)
