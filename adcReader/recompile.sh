sudo systemctl stop pmic_service
gcc -o pmic_service pmic_service.c 
sudo cp pmic_service /usr/local/bin/
sudo systemctl daemon-reload
sudo systemctl start pmic_service
echo "PMIC service recompiled and restarted successfully."
