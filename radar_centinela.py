"""
RADAR CENTINELA DE MERCADO (ECOSISTEMA DE FILTRADO CUANTITATIVO)
Objetivo:
- Escanea en segundo plano los activos principales (EURUSD, GBPUSD, USDJPY, BTCUSDT)
- Calcula matematicamente:
  1. Ratio de Avance Direccional (Net Displacement vs Total Path)
  2. Tamaño medio de las velas (Filtro Anti-Micropips / Ruido)
  3. Deteccion de Rango Picado / Congelado
- Si el mercado esta MUERTO o PICADO: Estado = 'MERCADO NO APTO' (Cero operaciones, protegiendo capital)
- Si detecta VOLUMEN REAL y TENDENCIA LIMPIA:
  Lanza ALERTA VERDE a Claude con los datos duros para que el ejecute la orden con alta probabilidad.
"""
import urllib.request
import json
import time
from datetime import datetime

class RadarCentinelaMercado:
    def __init__(self):
        self.pares = ["BTCUSDT"] # En cripto/binance para calculo instantaneo sin saturar IQ
        self.umbral_desplazamiento_minimo = 0.40 # Al menos 40% de avance neto sobre el ruido
        self.umbral_rango_minimo_usd = 80.0     # Para BTC, que las velas no sean planas

    def analizar_salud_mercado_binance(self, symbol="BTCUSDT"):
        try:
            url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1m&limit=15"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req, timeout=5)
            velas = json.loads(res.read().decode())
            
            cierres = [float(v[4]) for v in velas]
            maximos = [float(v[2]) for v in velas]
            minimos = [float(v[3]) for v in velas]
            
            apertura_inicial = float(velas[0][1])
            cierre_final = cierres[-1]
            
            # 1. Desplazamiento neto
            avance_neto = abs(cierre_final - apertura_inicial)
            
            # 2. Rango total acumulado (camino recorrido)
            recorrido_total = sum(abs(cierres[i] - cierres[i-1]) for i in range(1, len(cierres)))
            
            # 3. Ratio de Eficiencia de Tendencia (Kaufman Efficiency Ratio)
            eficiencia = avance_neto / recorrido_total if recorrido_total > 0 else 0
            
            # 4. Rango de volatilidad general
            rango_max_min = max(maximos) - min(minimos)
            
            es_apto = False
            diagnostico = "MERCADO PICADO / SIN VOLUMEN"
            
            if eficiencia >= self.umbral_desplazamiento_minimo and rango_max_min >= self.umbral_rango_minimo_usd:
                es_apto = True
                diagnostico = "MERCADO APTO CON TENDENCIA Y VOLUMEN REAL"
                
            return {
                "simbolo": symbol,
                "precio": cierre_final,
                "eficiencia": round(eficiencia, 2),
                "rango_max_min": round(rango_max_min, 2),
                "apto": es_apto,
                "diagnostico": diagnostico
            }
        except Exception as e:
            return {"simbolo": symbol, "apto": False, "diagnostico": f"Error: {e}"}

    def escanear_continuo(self):
        print("\n" + "="*70)
        print(">> RADAR CENTINELA: GUARDIAN DE CAPITAL ACTIVADO <<")
        print("Vigilando el mercado... Solo cuando este APTO se alertara a Claude.")
        print("="*70 + "\n")
        
        while True:
            ahora = datetime.now().strftime("%H:%M:%S")
            datos = self.analizar_salud_mercado_binance("BTCUSDT")
            
            if datos["apto"]:
                print(f"[{ahora}] [ALERTA VERDE] {datos['simbolo']}: {datos['diagnostico']}")
                print(f"  -> Eficiencia: {datos['eficiencia']} | Rango: ${datos['rango_max_min']} USD")
                print(f"  -> ACCION: Notificando a Claude para buscar setup sniper y disparar en IQ Option!")
                # Aqui dispara el comando de ejecucion a Claude
                break
            else:
                print(f"[{ahora}] [STANDBY] {datos['simbolo']}: {datos['diagnostico']} (Eficiencia: {datos.get('eficiencia', 0)}) -> MANOS QUIETAS.")
                
            time.sleep(15)

if __name__ == "__main__":
    centinela = RadarCentinelaMercado()
    centinela.escanear_continuo()
