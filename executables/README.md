# MQP_Project
Tutorial para crear estos ficheros en funcion del sistema operativo.

## Windows
Próximamente...

## MacOS
1. Copy the files to a folder named MyApp: <br>
    ```cp -r MQP_Project/ MyApp```
2. Execute this command: <br>
    ```hdiutil create -volname "MyApp" -srcfolder MyApp -ov -format UDZO MyApp.dmg```