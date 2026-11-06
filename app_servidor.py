"""
SERVIDOR EN LA NUBE 24/7 PARA RENDER
Mantiene vivo el servicio web para que Render no lo apague
y corre el Ecosistema de Trading Protegido en segundo plano.
"""
import os
import threading
import time
from datetime import datetime
from flask import Flask, jsonify
from radar_centinela import RadarCentinelaMercado

app = Flask(__name__)
centinela = RadarCentinelaMercado()

estado_nube = {
    "servidor": "Activo 24/7 en Render",
    "mercado_actual": "Vigilando...",
    "ultima_revision": "Iniciando...",
    "apto_para_operar": False
}

def bucle_vigilante_en_la_nube():
    """Bucle infinito que escanea el mercado cada 20 segundos sin detenerse."""
    time.sleep(3)
    print("\n[NUBE RENDER 24/7]: Ecosistema de Trading Iniciado con exito.\n")
    
    while True:
        try:
            ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
            salud = centinela.analizar_salud_mercado_binance("BTCUSDT")
            
            estado_nube["ultima_revision"] = ahora
            estado_nube["mercado_actual"] = f"BTC: ${salud.get('precio', 0):,.2f} | Eficiencia: {salud.get('eficiencia', 0)}"
            estado_nube["apto_para_operar"] = salud.get("apto", False)
            
            if salud.get("apto", False):
                print(f"[{ahora}] [ALERTA NUBE]: LUZ VERDE EN MERCADO -> {salud.get('diagnostico')}")
            else:
                print(f"[{ahora}] [STANDBY NUBE]: {salud.get('diagnostico')} -> Capital Protegido.")
                
            time.sleep(20)
        except Exception as e:
            print(f"[ERROR BUCLE NUBE]: {e}")
            time.sleep(30)

@app.route("/")
def index():
    return jsonify({
        "status": "Online",
        "mensaje": "Servidor de IA y Trading 24/7 Operativo",
        "datos": estado_nube
    })

# Iniciar el vigilante en segundo plano
hilo = threading.Thread(target=bucle_vigilante_en_la_nube, daemon=True)
hilo.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
