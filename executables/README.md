# Guía para crear los ejecutables de la aplicación

Los ejecutables creados con la herramienta de **build.sh** que se puede encontrar en el directorio previo a este.

Para crear un nuevo ejecutable se puede emplear los siguientes comandos:

1. Nos aseguramos que estamos en el directorio del build.sh

```
ls
```

2. Ejecutamos el siguiente comando para crear el ejecutable

```
./build.sh [-s] <versión>
```

También se puede crear el ejecutable manualmente mediante las instrucciones que se muestran a continuación:

## Requerimiento

   ```
   pip install pyinstaller
   ```

En caso de que queramos usar una herramienta interactiva de compilación:

   ```
   pip install auto-py-to-exe
   ```

## Windows

Puedes usar o bien esta herramienta:

   ```
   auto-py-to-exe
   ```

O directamente este comando:

   ```
   pyinstaller --noconfirm --onefile --windowed --icon "./icons/mqp.ico" --add-data "./icons;icons/" --add-data "./figures;figures/" --add-data "./locales;locales/" --add-data "./utils/auxi.py;." --add-data "./utils/config_menu.py;." --add-data "./utils/globals.py;." --add-data "./config.py;." "./main.py"
   ```

## MacOS

1. Copiar los ficheros en una carpeta llamada MyApp:
   ```
   cp -r MQP_Project/ MyApp
   ```

2. Ejecutar este comando:
   ```
   hdiutil create -volname "MyApp" -srcfolder MyApp -ov -format UDZO MyApp.dmg
   ```