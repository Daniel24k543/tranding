"""
ECOSISTEMA INTELIGENTE DE TRADING (GUARDIAN + CLAUDE MCP EN IQ OPTION)
1. El Radar Centinela escanea la salud del mercado en segundo plano.
2. Si el mercado esta congelado o picado: MANTIENE A CLAUDE DURMIENDO Y TU CAPITAL SEGURO.
3. Si el mercado rompe con volumen y da LUZ VERDE:
   - Despierta a Claude
   - Claude audita el activo con IQ Option MCP (iqoption-turbo)
   - Si Claude aprueba, ejecuta la orden de $1 en la cuenta demo de IQ Option
"""
import time
import subprocess
from datetime import datetime
from radar_centinela import RadarCentinelaMercado

centinela = RadarCentinelaMercado()

def despertar_a_claude_y_operar(simbolo="EURUSD"):
    print(f"\n[!] [DESPERTANDO A CLAUDE]: El Radar dio LUZ VERDE en el mercado!")
    print(f"  -> Claude analizando con herramientas oficiales de IQ Option...")
    
    prompt = (
        f"ALERTA DEL RADAR: El mercado acaba de dar confirmacion de volumen y tendencia real. "
        f"Usa iqoption-turbo get_candles de {simbolo} (ultimas 15 velas de 1m). "
        f"Si la tendencia es limpia, ejecuta place_trade por 1 dolar en la cuenta training de demo. "
        f"Si la vela se frena, di: 'ENTRADA CANCELADA' y no operes."
    )
    
    cmd = ["claude", "--dangerously-skip-permissions", "-p", prompt]
    res = subprocess.run(cmd, capture_output=True, text=True, shell=True, encoding="utf-8", errors="ignore")
    print("\n--- RESPUESTA DE CLAUDE EN IQ OPTION ---")
    print(res.stdout.strip())
    print("----------------------------------------\n")

def bucle_ecosistema():
    print("\n" + "="*70)
    print("[GUARDIAN]  ECOSISTEMA DE TRADING PROTEGIDO: RADAR + CLAUDE EN IQ OPTION")
    print("======================================================================")
    print("Regla: Prohibido operar a ciegas. Cero operaciones sin luz verde del Radar.")
    print("="*70 + "\n")
    
    ciclo = 1
    while True:
        ahora = datetime.now().strftime("%H:%M:%S")
        salud = centinela.analizar_salud_mercado_binance("BTCUSDT")
        
        eficiencia = salud.get("eficiencia", 0)
        diagnostico = salud.get("diagnostico", "Sin datos")
        
        if salud.get("apto", False):
            print(f"[{ahora}] [CICLO #{ciclo}] [LUZ VERDE] ¡LUZ VERDE DEL RADAR! (Eficiencia: {eficiencia})")
            print(f"  -> Condicion: {diagnostico}. Llamando a Claude...")
            despertar_a_claude_y_operar("EURUSD")
            print("Pausa de 3 minutos tras la operacion para evaluar el resultado...")
            time.sleep(180)
        else:
            print(f"[{ahora}] [CICLO #{ciclo}] [ROJO] RADAR: {diagnostico} (Eficiencia: {eficiencia} / Minimo: 0.40) -> Capital a salvo.")
            time.sleep(20)
            
        ciclo += 1

if __name__ == "__main__":
    bucle_ecosistema()
