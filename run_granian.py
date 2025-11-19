import os
import subprocess
import sys

from app import create_app

os.environ.setdefault("BACKEND_ENV", "development")

app = create_app()


def main():

    cmd = [
        'granian',
        '--interface', 'wsgi',
        '--host', '0.0.0.0',
        '--port', '5001',
        '--workers', '1',  # Un worker para desarrollo
        'run_granian:app'
    ]
    
    print("🚀 Iniciando servidor con Granian...")
    print(f"📍 URL: http://localhost:5001")
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
