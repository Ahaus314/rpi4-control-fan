# RaspberryPi 4 Control Fan

### Manual launch

1. Open a command prompt
2. Navigate to the folder
3. Make sure the manual.sh is executable
```bash
chmod +x manual.sh
``` 
4. Launch the script
```bash
./manual.sh
``` 
5. Use CTRL+C to stop the script


### Create and launch the service

1. Open a command prompt
2. Navigate to 
```bash
cd /lib/systemd/system/
``` 
2. Create the service file
```bash
sudo nano control-fan.service
``` 
3. Here's the content that you should put in the service file
```bash
[Unit]
Description=Control Fan based on CPU temperature
After=multi-user.target

[Service]
Type=simple
ExecStart=/usr/bin/python /home/pi/Projects/rpi4-control-fan/control.py

[Install]
WantedBy=multi-user.target
```  
4. Change the permission of the file
```bash
sudo chmod 644 /lib/systemd/system/ control-fan.service
``` 
5. Enable the service
```bash
sudo systemctl enable --now control-fan.service
``` 
6. Useful commands
```bash
sudo systemctl start control-fan.service
sudo systemctl stop control-fan.service
sudo systemctl daemon-reload
sudo systemctl status control-fan.service
``` 

Thanks
