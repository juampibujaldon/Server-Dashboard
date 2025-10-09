#!/usr/bin/env python3
"""
Script para ejecutar la aplicación con Granian en modo desarrollo.
"""

import os
import subprocess
import sys

def main():
    """Ejecutar la aplicación con Granian."""
    
    # Configurar variables de entorno para desarrollo
    os.environ.setdefault('BACKEND_ENV', 'development')
    
    # Comando para ejecutar con Granian
    cmd = [
        'granian',
        '--interface', 'wsgi',
        '--host', '0.0.0.0',
        '--port', '5000',
        '--workers', '1',  # Un worker para desarrollo
        '--reload',  # Auto-reload en desarrollo
        'granian_config:app'
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
