"""
CONECTOR PARA USAR TU SUSCRIPCION DE CLAUDE (CLAUDE CODE CLI)
Permite a tus agentes consultar a Claude directamente por terminal
usando tus $20 USD de suscripcion, sin pagar API adicional!
"""
import subprocess
import shutil

class ConectorClaudeCode:
    def __init__(self):
        self.disponible = shutil.which("claude") is not None

    def preguntar_a_claude(self, prompt):
        if not self.disponible:
            return "Claude CLI no encontrado en PATH."

        try:
            # Invocar Claude en modo print directo (-p)
            comando = ["claude", "-p", prompt]
            resultado = subprocess.run(
                comando,
                capture_output=True,
                text=True,
                shell=True,
                encoding="utf-8",
                errors="ignore"
            )
            if resultado.returncode == 0:
                return resultado.stdout.strip()
            else:
                return f"Error ejecutando Claude: {resultado.stderr.strip()}"
        except Exception as e:
            return f"Excepcion al conectar con Claude: {str(e)}"

if __name__ == "__main__":
    conector = ConectorClaudeCode()
    print("Probando conexion con Claude Code CLI...")
    respuesta = conector.preguntar_a_claude("Hola Claude! Dime en una sola oracion que tarea tienes hoy como CEO de mi oficina de agentes.")
    print("\nRespuesta de Claude:")
    print(respuesta)
