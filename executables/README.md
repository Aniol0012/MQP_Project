# MQP_Project
Tutorial para crear estos ficheros en funcion del sistema operativo.

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