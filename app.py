import sys
import os

# 1. Imports & configuration SSL
import certifi
ca = certifi.where()

# 2. Variables d'environnement 
from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGO_DB_URL")  # Récupère l'URL de connexion MongoDB
if not mongo_db_url:
    raise ValueError("MONGO_DB_URL not found in environment variables")

# 3. Import du Projet 
import pymongo
from networksecurity.exception.exception import NetworkSecurityException  
from networksecurity.logging.logger import logging                         
from networksecurity.pipeline.training_pipeline import TrainingPipeline  

# Imports FastAPI pour la création de l'API REST
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run                    # Serveur ASGI pour exécuter FastAPI
from fastapi.responses import Response
from starlette.responses import RedirectResponse      # Redirection HTTP
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object  
from networksecurity.utils.ml_utils.model.estimator import NetworkModel


# 4. Connexion MongoDB
from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME
client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

#5. Initialisation de l'application FastAPI + CORS

app = FastAPI() # Créer l'application API REST
origins = ["*"] # Autorise toutes les originies à appeler l'API 

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      
    allow_credentials=True,    
    allow_methods=["*"],         
    allow_headers=["*"]         
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

# 6. Route racine : redirige automatiquement vers /docs (Swagger UI)
# Facilite l'accès à la documentation interactive de l'API
@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

# 7. Route d'entraînement : déclenche le pipeline ML complet (ingestion, transformation, entraînement)
# Accessible via GET /train — retourne un message de succès ou propage l'exception
@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()  # Instancie le pipeline d'entraînement
        train_pipeline.run_pipeline()        # Exécute toutes les étapes du pipeline
        return Response("Training is succesful")
    except Exception as e:
        raise NetworkSecurityException(e, sys)  # Remonte l'erreur avec contexte système

@app.post("/predict")
async def predict_route(request:Request, file:UploadFile=File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred
        os.makedirs("prediction_output", exist_ok=True)
        df.to_csv("prediction_output/output.csv", index=False)
        table_html = df.to_html(classes=('table table-striped'))
        return templates.TemplateResponse(request, "table.html", {"table": table_html})
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)
                                          





# 8. Point d'entrée 
# Lance le serveur Uvicorn (serveur ASGI async) sur localhost:8000 quand le fichier est exécuté directement (python app.py).
if __name__ == "__main__" :
    app_run(app,host = "0.0.0.0", port = 8000)