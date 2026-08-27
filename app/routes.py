from flask import Blueprint, request, jsonify, render_template
from app.database import lead_ekle, tum_leadler
from app.services.ai_service import ai_service, AIServiceError

api = Blueprint('api', __name__)
pages = Blueprint('pages', __name__)

@pages.route('/')
def index():
    return render_template('index.html')

@pages.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@api.route('/sohbet', methods=['POST'])
def sohbet():
    veri = request.json
    mesaj = veri.get('mesaj')
    gecmis = veri.get('gecmis', [])

    if not mesaj:
        return jsonify({'basari': False, 'hata': 'Mesaj bos olamaz.'}), 400

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)
        return jsonify({'basari': True, 'cevap': cevap})
    except AIServiceError as e:
        return jsonify({'basari': False, 'hata': str(e)}), 503

@api.route('/leads', methods=['POST'])
def yeni_lead():
    veri = request.json
    isim = veri.get('isim')
    telefon = veri.get('telefon')
    mesaj = veri.get('mesaj', '')

    if not isim or not telefon:
        return jsonify({'basari': False, 'hata': 'Isim ve telefon zorunlu.'}), 400

    lead_ekle(isim, telefon, mesaj)
    return jsonify({'basari': True}), 201

@api.route('/leads', methods=['GET'])
def leadleri_getir():
    return jsonify({'basari': True, 'leadler': tum_leadler()})