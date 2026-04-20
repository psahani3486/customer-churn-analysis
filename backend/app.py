"""
Flask Backend API for Customer Churn Analysis Dashboard.
Serves analytics data, model results, and predictions.
"""
import sys
import os

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, send_from_directory
from flask_cors import CORS

from backend.routes.analytics import analytics_bp
from backend.routes.predictions import predictions_bp


def create_app():
    app = Flask(__name__, static_folder=None)
    
    # Allow CORS from all origins for separate frontend/backend deployment
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(analytics_bp, url_prefix="/api")
    app.register_blueprint(predictions_bp, url_prefix="/api")

    # Serve frontend static files
    frontend_dir = os.path.join(PROJECT_ROOT, "frontend")

    @app.route("/")
    def serve_index():
        return send_from_directory(frontend_dir, "index.html")

    @app.route("/<path:path>")
    def serve_static(path):
        return send_from_directory(frontend_dir, path)

    @app.route("/api/health")
    def health():
        return {"status": "ok", "message": "Customer Churn Analysis API is running"}

    return app


if __name__ == "__main__":
    app = create_app()
    print("=" * 60)
    print("  [*] Customer Churn Analysis API")
    print("  [>] Dashboard: http://localhost:5000")
    print("  [>] API Base:  http://localhost:5000/api")
    print("=" * 60)
    app.run(debug=True, port=5000)
