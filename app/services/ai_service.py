import requests
from flask import current_app

class AIServiceError(Exception):
    pass

class AIService:
    def yanit_uret(self, mesaj, gecmis=None):
        api_key = current_app.config.get('GROQ_API_KEY')
        if not api_key:
            return "Sistem demo modunda calisiyor, lutfen .env dosyanizi kontrol edin."

        gecmis = gecmis or []
        mesajlar = [
            {"role": "system", "content": current_app.config['BUSINESS_CONTEXT']}
        ] + gecmis + [
            {"role": "user", "content": mesaj}
        ]

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}"},
                json={
                    "model": "openai/gpt-oss-20b",
                    "messages": mesajlar
                },
                timeout=15
            )
            response.raise_for_status()
            veri = response.json()
            return veri['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            raise AIServiceError(f"Yapay zeka servisine ulasilamadi: {str(e)}")

ai_service = AIService()