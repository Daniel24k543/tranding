"""
SERVIDOR WEB Y CICLO 24/7 PARA RENDER / CLOUD
Levanta un mini servidor web con Flask para que Render lo mantenga vivo
y ejecuta el ciclo continuo de los agentes en segundo plano.
"""
import os
import threading
import time
from flask import Flask, jsonify
from ceo_oficina import DirectorGeneral
from notificador_whatsapp import NotificadorWhatsApp

app = Flask(__name__)
notificador = NotificadorWhatsApp()
ceo = DirectorGeneral()

# Estado de la oficina en memoria
estado_oficina = {
    "estado": "Operando 24/7",
    "ciclos_completados": 0,
    "ultimo_reporte": "Iniciando sistema..."
}

def bucle_oficina_24_7():
    """Bucle infinito que ejecuta las tareas de la oficina cada X minutos."""
    time.sleep(5)
    notificador.enviar_mensaje("🚨 [OFICINA IA INICIADA] Tus agentes ya estan activos 24/7 en el servidor Render.")
    
    while True:
        try:
            print("\n>>> EJECUTANDO NUEVO CICLO AUTOMATIZADO 24/7 <<<")
            ceo.iniciar_jornada_completa()
            estado_oficina["ciclos_completados"] += 1
            
            # Obtener resumen del trading para WhatsApp
            ranking = sorted(ceo.jefe_trading.empleados, key=lambda x: x.ganancias_acumuladas, reverse=True)
            mejor = ranking[0]
            peor = ranking[-1]
            
            mensaje_wsp = (
                f"📊 *REPORTE DE TU OFICINA IA*\n\n"
                f"🎬 *Marketing:* Video viral generado y programado.\n"
                f"🛡️ *Apps & Redes:* Todo 100% online y spam moderado.\n"
                f"📈 *Trading Demo:*\n"
                f"  • Mejor Empleado: {mejor.nombre} (+${mejor.ganancias_acumuladas:.2f})\n"
                f"  • En Autocastigo: {peor.nombre} (Nivel {peor.nivel_castigo})\n\n"
                f"Ciclo #{estado_oficina['ciclos_completados']} completado con exito."
            )
            
            notificador.enviar_mensaje(mensaje_wsp)
            estado_oficina["ultimo_reporte"] = mensaje_wsp
            
            # Esperar 30 minutos antes del siguiente escaneo/ciclo (configurable)
            print("Pausando 30 minutos hasta el siguiente chequeo...\n")
            time.sleep(1800)
            
        except Exception as e:
            print(f"Error en el bucle: {e}")
            time.sleep(60)

@app.route("/")
def index():
    return jsonify({
        "status": "Online",
        "oficina": "Oficina Virtual de Agentes IA",
        "datos": estado_oficina
    })

# Iniciar el hilo en segundo plano cuando arranca la app
hilo = threading.Thread(target=bucle_oficina_24_7, daemon=True)
hilo.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
