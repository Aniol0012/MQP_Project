#!/bin/bash

sed -i 's/SCREEN_TO_OPEN_ROOT = 1  # 1 Para la segunda pantalla y 0 para la primera/SCREEN_TO_OPEN_ROOT = 0  # 1 Para la segunda pantalla y 0 para la primera/g' config.py

help_panel() {
    echo "Uso: $0 [nombre del ejecutable] [-h] [-s]"
    echo "  -h: Muestra este panel de ayuda."
    echo "  -s: Marca la versión como estable."
    echo "  -r: Removes all the previous versions"
    exit
}

stable=false

while getopts ":hsr" opt; do
  case ${opt} in
    h )
      help_panel
      ;;
    s )
      stable=true
      ;;
    r )
      rm executables/latest/*
      rm executables/old/*
      rm executables/stable/*
      ;;
    \? )
      echo "Opción inválida: -$OPTARG" 1>&2
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

if [[ -z $1 ]]; then
    echo "Debes introducir un parámetro con el nombre del ejecutable. Ejemplo: 9.0.2"
    exit 1
fi

# Comprueba si pyinstaller está instalado
if ! pip show pyinstaller > /dev/null; then
    pip install pyinstaller
fi

# Comprueba si las carpetas existen antes de intentar crearlas
if [ ! -d "executables/stable" ]; then
    mkdir -p executables/stable
fi
if [ ! -d "executables/latest" ]; then
    mkdir -p executables/latest
fi
if [ ! -d "executables/old" ]; then
    mkdir -p executables/old
fi

pyinstaller --noconfirm --onefile --windowed --icon "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/icons/mqp.ico" --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/icons;icons/" --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/figures;figures/" --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/locales;locales/" --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/auxi.py;." --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/config.py;." --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/globals.py;." --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/movment.py;." "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/main.py"

mv executables/latest/* executables/old

mv dist/main.exe executables/latest/MQP_V$1.exe


if [[ $stable = true ]]; then
    cp executables/latest/MQP_V$1.exe executables/stable/MQP_V$1.exe
fi

# Mueve todas las versiones que no sean estables a la carpeta 'old'
if [[ $stable = true ]]; then
    find executables/stable -type f ! -name "MQP_V$1.exe" -exec bash -c 'mv $0 executables/old/$(basename $0 .exe)_stable.exe' {} \;
fi

rm -rf build dist output main.spec

sed -i 's/SCREEN_TO_OPEN_ROOT = 0  # 1 Para la segunda pantalla y 0 para la primera/SCREEN_TO_OPEN_ROOT = 1  # 1 Para la segunda pantalla y 0 para la primera/g' config.py
