# MQP_Project
Tutorial para crear estos ficheros en funcion del sistema operativo.

## Requerimiento
   ```
   pip install pyinstaller
   ```
   
   ```
   pip install auto-py-to-exe
   ```

## Windows
   ```
   auto-py-to-exe
   ```

   ```
   pyinstaller --noconfirm --onefile --windowed --icon "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/icons/mqp.ico" --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/icons/mqp.png;." --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/config.py;."  "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/main.py"
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