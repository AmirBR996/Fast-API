from pydantic import BaseModel, Field
from typing import Dict


class PredictionResponse(BaseModel):
    predicted_category: str = Field(..., description="Predicted insurance premium category")
    confidence: float = Field(..., description="Model confidence score (0-1)")
    class_probabilities: Dict[str, float] = Field(..., description="Probability distribution across classes")