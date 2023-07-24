# MQP_Project
Tutorial para crear estos ficheros en funcion del sistema operativo.

## Requerimiento
   ```
   pip install pyinstaller
   ```

## Windows
   ```
   pyinstaller --onefile -w main.py
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