from flask import Flask, jsonify
from flask_cors import CORS
from config import config_by_name
from app.database import init_db

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    CORS(app, origins=app.config['CORS_ORIGINS'])

    init_db(app)

    from app.routes import api, pages
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(pages)

    @app.route('/health')
    def health():
        return jsonify({'durum': 'aktif'})

    return app