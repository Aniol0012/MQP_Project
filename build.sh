if [[ $1 == "" ]]; then
  echo "Debes introducir un parametro con el nombre del ejectuable. Ejemplo: MQP_V9"
fi

pip install pyinstaller

pyinstaller --noconfirm --onefile --windowed --icon "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/icons/mqp.ico" --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/icons;icons/" --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/figures;figures/" --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/locales;locales/" --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/auxi.py;." --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/config.py;." --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/globals.py;." --add-data "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/movment.py;." "C:/Users/aniol/OneDrive/Escriptori/Githubs/MQP_Project/main.py"

mv dist/main.exe executables/$1.exe
