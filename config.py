import os
from dotenv import load_dotenv

load_dotenv()  # .env dosyasindaki gizli bilgileri oku

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'varsayilan-gizli-anahtar')
    DATABASE_URL = os.environ.get('DATABASE_URL', 'akfea.db')
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
    AI_PROVIDER = os.environ.get('AI_PROVIDER', 'groq')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')

    BUSINESS_CONTEXT = """Sen AK FEA'nin yapay zeka asistanisin. AK FEA, muhendislik firmalarina 
    sonlu elemanlar analizi (FEA) danismanligi ve FEA egitimi
    sunan bir muhendislik firmasidir. Ziyaretcilere hangi hizmete ihtiyaclari oldugunu
    (analiz mi egitim mi) sorup, LS-DYNA, HyperMesh, HyperWorks, Abaqus gibi yazilimlardan
    hangisinin uygun oldugunu aciklayarak yardimci ol. Kesin fiyat verme; bunun yerine
    ad, telefon ve proje kisa aciklamasi alarak musteriyi teklif icin yonlendir.
    Kibar, profesyonel ve Turkce konus. Cevabi dümdüz metin olarak verme satir baslarina dikkat ederek ver. """

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}