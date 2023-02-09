# Horizon-Vue
![alt text](https://github.com/dfoley84/Horizon-Vue/blob/main/frontend/assets/2023-02-09%2010_20_04-frontend.png?raw=true)


# Horizon Portal
Portal to allow end users to powercycle their virtual Horzion VDI's
while also allowing them to RDP/SSH into their Machines from within the Console

# Actions Required
    1) PowerShell Script to pull Horizon VDI from Horizon to Database, 
    2) Create Jenkins Free Style Jobs for Each PowerAction
    3) Configure RabbitMQ to Take PowerAction Required 
    4) Configure VMware Player Redirect
    5) Configure SSH Redirect
    6) Python Script to Get Message and Trigger Remote Jenkins Job


