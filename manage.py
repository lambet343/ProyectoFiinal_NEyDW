#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

# Importa los módulos necesarios para interactuar con el sistema operativo y ejecutar comandos
import os
import sys

# Función principal que se encarga de ejecutar tareas administrativas de Django
def main():
    """Run administrative tasks."""
    
    # Configura la variable de entorno DJANGO_SETTINGS_MODULE que indica el archivo de configuración de Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PartyPack.settings')

    try:
        # Importa y ejecuta la utilidad de línea de comandos de Django
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Si no se puede importar Django, muestra un mensaje de error indicando qué podría estar mal
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Ejecuta el comando pasado en la línea de comandos (sys.argv) para realizar tareas administrativas
    execute_from_command_line(sys.argv)

# Verifica si este archivo se está ejecutando directamente (como un script) y llama a la función main()
if __name__ == '__main__':
    main()
