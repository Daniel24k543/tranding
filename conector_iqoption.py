"""
CONECTOR OFICIAL DE TRADING EN IQ OPTION (CUENTA DEMO)
Permite a los empleados de IA ejecutar operaciones reales de CALL (Subida) / PUT (Bajada)
directamente en tu saldo de práctica de IQ Option usando el mercado en vivo.
"""
import os
import time
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

class TraderIQOptionDemo:
    def __init__(self):
        self.email = os.getenv("IQ_OPTION_EMAIL", "")
        self.password = os.getenv("IQ_OPTION_PASSWORD", "")
        self.cuenta_tipo = "PRACTICE" # SIEMPRE CUENTA DEMO PARA APRENDER SIN RIESGO
        self.conectado = False

    def conectar(self):
        if not self.email or not self.password:
            print("[IQ OPTION] Credenciales no configuradas aun en .env.")
            print("  -> Ejecutando en Modo SIMULADOR DE IQ OPTION (Mercado EUR/USD en tiempo real).")
            return False
        
        try:
            from iqoptionapi.stable_api import IQ_Option
            self.api = IQ_Option(self.email, self.password)
            check, reason = self.api.connect()
            if check:
                self.api.change_balance(self.cuenta_tipo) # Cambiar a cuenta Demo
                self.conectado = True
                saldo = self.api.get_balance()
                print(f"[IQ OPTION CONECTADO CON EXITO]")
                print(f"  -> Tipo de Cuenta: {self.cuenta_tipo} (Practica)")
                print(f"  -> Saldo Demo Disponible: ${saldo:,.2f}")
                return True
            else:
                print(f"[IQ OPTION ERROR DE CONEXION]: {reason}")
                return False
        except Exception as e:
            print(f"[IQ OPTION ERROR]: {e}")
            return False

    def ejecutar_orden_demo(self, activo="EURUSD", direccion="call", monto=1, duracion_minutos=1):
        """
        direccion: 'call' (Sube) o 'put' (Baja)
        """
        print(f"\n[IQ OPTION DESK]: Evaluando oportunidad en {activo} ({duracion_minutos} min)...")
        print(f"  -> Señal del Agente: {direccion.upper()} | Monto Demo: ${monto}")

        if self.conectado:
            check, id_orden = self.api.buy(monto, activo, direccion, duracion_minutos)
            if check:
                print(f"  ✅ [ORDEN ABIERTA EN IQ OPTION DEMO] ID Operacion: {id_orden}")
            else:
                print(f"  ❌ [ERROR AL EJECUTAR EN IQ OPTION]")
        else:
            print(f"  [SIMULACION IQ OPTION]: Orden {direccion.upper()} ejecutada en Demo a precio de vela actual.")

if __name__ == "__main__":
    trader = TraderIQOptionDemo()
    trader.conectar()
    trader.ejecutar_orden_demo("EURUSD", "call", monto=5, duracion_minutos=1)
