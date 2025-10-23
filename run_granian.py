#!/usr/bin/env python3
"""
Script para ejecutar la aplicación con Granian en modo desarrollo.
"""

import os
import subprocess
import sys

from app import create_app

# Configurar variables de entorno por defecto antes de construir la app
os.environ.setdefault("BACKEND_ENV", "development")

# Objeto que usará Granian cuando se invoque como `run_granian:app`
app = create_app()


def main():
    """Ejecutar la aplicación con Granian."""

    # Comando para ejecutar con Granian
    cmd = [
        'granian',
        '--interface', 'wsgi',
        '--host', '0.0.0.0',
        '--port', '5000',
        '--workers', '1',  # Un worker para desarrollo
        '--reload',  # Auto-reload en desarrollo
        'run_granian:app'
    ]
    
    print("🚀 Iniciando servidor con Granian...")
    print(f"📍 URL: http://localhost:5000")
    print(f"⚙️  Comando: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al ejecutar Granian: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
