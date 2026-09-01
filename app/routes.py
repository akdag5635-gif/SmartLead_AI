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
    veri = request.get_json(silent=True) or {}

    mesaj = veri.get('mesaj')
    gecmis = veri.get('gecmis', [])

    if not mesaj:
        return jsonify({
            'basari': False,
            'hata': 'Mesaj bos olamaz.'
        }), 400

    try:
        cevap = ai_service.yanit_uret(mesaj, gecmis)

        return jsonify({
            'basari': True,
            'cevap': cevap
        })

    except AIServiceError as e:
        return jsonify({
            'basari': False,
            'hata': str(e)
        }), 503


@api.route('/leads', methods=['POST'])
def yeni_lead():
    veri = request.get_json(silent=True) or {}

    isim = str(veri.get('isim', '')).strip()
    email = str(veri.get('email', '')).strip()
    telefon = str(veri.get('telefon', '')).strip()
    mesaj = str(veri.get('mesaj', '')).strip()

    if not isim or not email or not telefon:
        return jsonify({
            'basari': False,
            'hata': 'Ad Soyad, e-posta ve telefon zorunlu.'
        }), 400

    if '@' not in email:
        return jsonify({
            'basari': False,
            'hata': 'Gecerli bir e-posta adresi girin.'
        }), 400

    lead_ekle(
        isim=isim,
        email=email,
        telefon=telefon,
        mesaj=mesaj
    )

    return jsonify({
        'basari': True,
        'mesaj': 'Bilgiler basariyla kaydedildi.'
    }), 201


@api.route('/leads', methods=['GET'])
def leadleri_getir():
    return jsonify({
        'basari': True,
        'leadler': tum_leadler()
    })