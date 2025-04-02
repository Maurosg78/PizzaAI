#!/usr/bin/env python3
"""
Script de monitoreo ligero para verificar el estado del código.
"""

import os
import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path
import json
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('monitor.log'),
        logging.StreamHandler()
    ]
)

class CodeMonitor:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.results = {
            'timestamp': '',
            'linting': {},
            'tests': {},
            'dependencies': {}
        }

    def run_command(self, command: list, cwd: Path = None) -> dict:
        """Ejecuta un comando y retorna su resultado."""
        try:
            result = subprocess.run(
                command,
                cwd=cwd or self.project_root,
                capture_output=True,
                text=True
            )
            return {
                'success': result.returncode == 0,
                'output': result.stdout,
                'error': result.stderr
            }
        except Exception as e:
            return {
                'success': False,
                'output': '',
                'error': str(e)
            }

    def check_linting(self):
        """Verifica el código con flake8."""
        self.results['linting'] = {
            'flake8': self.run_command(['flake8', 'src', 'tests'])
        }

    def check_tests(self):
        """Ejecuta los tests con pytest."""
        self.results['tests'] = self.run_command(['pytest'])

    def check_dependencies(self):
        """Verifica las dependencias con pip list."""
        self.results['dependencies'] = self.run_command(['pip', 'list'])

    def print_report(self):
        """Imprime un reporte del estado del código."""
        print("\n" + "="*50)
        print(f"Estado del Código - {self.results['timestamp']}")
        print("="*50)

        # Linting
        print("\nLinting:")
        for tool, result in self.results['linting'].items():
            status = "✅ OK" if result['success'] else "❌ Error"
            print(f"{tool}: {status}")
            if not result['success']:
                print(f"Errores: {result['error']}")

        # Tests
        print("\nTests:")
        test_result = self.results['tests']
        status = "✅ OK" if test_result['success'] else "❌ Error"
        print(f"Estado: {status}")
        if not test_result['success']:
            print(f"Errores: {test_result['error']}")

        # Dependencias
        print("\nDependencias:")
        deps_result = self.results['dependencies']
        if deps_result['success']:
            print("Lista de dependencias instaladas:")
            print(deps_result['output'])
        else:
            print("Error al obtener dependencias")

    def monitor(self, interval: int = 300):
        """Monitorea el código continuamente."""
        print("Iniciando monitoreo de código...")
        print(f"Intervalo de verificación: {interval} segundos")

        try:
            while True:
                self.results['timestamp'] = datetime.now().isoformat()
                
                self.check_linting()
                self.check_tests()
                self.check_dependencies()

                self.print_report()
                
                # Guardar resultados en JSON
                with open('monitor_results.json', 'w') as f:
                    json.dump(self.results, f, indent=2)

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\nMonitoreo detenido por el usuario")
            sys.exit(0)

if __name__ == "__main__":
    monitor = CodeMonitor()
    monitor.monitor() 