#!/bin/bash

# Colores para la salida
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directorios a monitorear
WATCH_DIRS="src tests"

# Función para verificar cambios
check_changes() {
    find $WATCH_DIRS -type f -mmin -1 | grep -q .
    return $?
}

# Función para imprimir el timestamp
print_timestamp() {
    echo -e "\n${YELLOW}=== $(date) ===${NC}\n"
}

# Función para verificar linting
check_linting() {
    echo -e "${YELLOW}Verificando linting...${NC}"
    flake8 src tests
}

# Función para ejecutar tests
run_tests() {
    echo -e "${YELLOW}Ejecutando tests...${NC}"
    pytest
}

# Bucle principal
echo -e "${GREEN}Iniciando monitoreo de cambios en: $WATCH_DIRS${NC}"
echo -e "${YELLOW}Presiona Ctrl+C para detener${NC}\n"

while true; do
    if check_changes; then
        print_timestamp
        check_linting
        run_tests
    fi
    sleep 10
done 