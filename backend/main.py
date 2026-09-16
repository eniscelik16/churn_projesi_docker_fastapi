from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import shap # EKLENDİ

app = FastAPI(title="Bank Churn Prediction API")

try:
    model_pack = joblib.load('churn_thesis_model.pkl')
    model = model_pack['model']
    scaler = model_pack['scaler']
    expected_features = model_pack['features']
    # SHAP Explainer'ı sadece 1 kere belleğe yüklüyoruz (Performans için)
    explainer = shap.TreeExplainer(model)
except Exception as e:
    print(f"Model yüklenemedi: {e}")
    model, scaler, expected_features, explainer = None, None, None, None

class CustomerData(BaseModel):
    CreditScore: int
    Geography: str
    Gender: str
    Age: int
    Tenure: int
    Balance: float
    NumOfProducts: int
    HasCrCard: int
    IsActiveMember: int
    EstimatedSalary: float

# YENİ: Overview sekmesindeki "Driver Analysis" grafiği için model özelliklerini gönderen endpoint
@app.get("/model_info")
def get_model_info():
    if model is not None:
        return {
            "features": expected_features,
            "importances": model.feature_importances_.tolist()
        }
    return {"features": [], "importances": []}

@app.post("/predict")
def predict_churn(customer: CustomerData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model yüklenemedi.")

    customer_dict = customer.model_dump()
    df_input = pd.DataFrame([customer_dict])
    df_input = pd.get_dummies(df_input, drop_first=True)

    for col in expected_features:
        if col not in df_input.columns:
            df_input[col] = 0
    df_input = df_input[expected_features]

    scaled_input = scaler.transform(df_input)
    
    churn_probability = model.predict_proba(scaled_input)[0][1]
    churn_prediction = int(model.predict(scaled_input)[0])

    # YENİ: SHAP değerlerini hesaplayıp JSON ile gönderilebilir listeye çeviriyoruz
    shap_values = explainer.shap_values(scaled_input, check_additivity=False)
    if isinstance(shap_values, list):
        shap_vals = shap_values[1][0]
    else:
        shap_vals = shap_values[0, :, 1] if len(shap_values.shape) == 3 else shap_values[0]

    return {
        "churn_prediction": churn_prediction,
        "churn_probability": round(float(churn_probability), 4),
        "shap_values": np.array(shap_vals).flatten().tolist(), 
        "features": expected_features, # Frontend'e gidiyor
        "message": "Tahmin ve SHAP başarıyla hesaplandı."
    }