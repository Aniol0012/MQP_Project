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
   pyinstaller --noconfirm --onefile --windowed --icon "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/icons/mqp.ico" --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/icons;icons/" --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/figures;figures/" --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/locales;locales/" --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/auxi.py;." --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/config.py;." --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/globals.py;." --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/movment.py;."  "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/main.py"
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