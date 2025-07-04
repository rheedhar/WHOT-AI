import os

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI()
model = None
label_encoder = None


def load_model():
    global model, label_encoder
    if model is None or label_encoder is None:
        model = joblib.load("src/models/whot_model.pkl")
        label_encoder = joblib.load("src/models/action_encoder.pkl")
    return model, label_encoder


class WhotData(BaseModel):
    card_1: str
    card_2: str
    card_3: str
    card_4: str
    call_card: str
    requested_suit: str
    special_state: str


class PredictionOutput(BaseModel):
    action: str


@app.post("/predict", response_model=PredictionOutput)
async def predict(request: WhotData):
    global model, label_encoder
    model, label_encoder = load_model()
    df = pd.DataFrame(data=[[request.card_1, request.card_2, request.card_3, request.card_4,
                             request.call_card, request.requested_suit, request.special_state]],
                      columns=["Card 1", "Card 2", "Card 3", "Card 4", "Call Card", "Requested Suit", "Special State"])
    predict_encoded = model.predict(df)
    predict_label = label_encoder.inverse_transform(predict_encoded)
    return {"action": predict_label[0]}
