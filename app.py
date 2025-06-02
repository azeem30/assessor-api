from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from utils.db_utils import create_db_pool
from utils.model_utils import EvaluatorModel
from routes.auth import register_auth_routes
from routes.tests import register_test_routes
from routes.responses import register_response_routes
from routes.profile import register_profile_routes
from routes.analytics import register_analytics_routes
from config import APP_CONFIG
from config import MODEL_CONFIG
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

db_pool = create_db_pool()
model = EvaluatorModel(MODEL_CONFIG["MODEL_NAME"])

# Routes
register_auth_routes(app, db_pool)
register_test_routes(app, model, db_pool)
register_response_routes(app, db_pool)
register_profile_routes(app, db_pool)
register_analytics_routes(app, db_pool)

if __name__ == "__main__":
    port = APP_CONFIG["PORT"]
    app.run(debug=True, host=APP_CONFIG["HOST"], port=port)
