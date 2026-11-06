"""
POOL DE CEREBROS GRATUITOS (CONECTADO A TU GROQ API KEY)
Utiliza tu clave de Groq para dotar a los empleados de IA gratuita ultra-rapida.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

class CerebroGratuitoPool:
    def __init__(self):
        self.groq_api_key = os.getenv("GROQ_API_KEY", "")
        # Modelo gratuito de alto rendimiento verificado en tu cuenta
        self.modelo = "openai/gpt-oss-120b"

    def consultar(self, prompt, rol="Empleado IA"):
        if self.groq_api_key:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {"Authorization": f"Bearer {self.groq_api_key}"}
                payload = {
                    "model": self.modelo,
                    "messages": [
                        {"role": "system", "content": f"Eres {rol} en una empresa autonoma de IA. Responde de forma precisa y directa."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.6
                }
                res = requests.post(url, headers=headers, json=payload, timeout=10)
                if res.status_code == 200:
                    return res.json()["choices"][0]["message"]["content"].strip()
            except Exception as e:
                pass

        return f"[{rol}] Modo local activo para: {prompt[:30]}..."

if __name__ == "__main__":
    pool = CerebroGratuitoPool()
    print("Probando conexion directa con tu Groq API...")
    res = pool.consultar("Analiza en 1 oracion si conviene entrar en Long en Bitcoin hoy.", "Analista Cripto")
    print("\nRespuesta del Empleado (Potenciado por Groq):")
    print(res)
