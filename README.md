# Horizon-Vue
![alt text](https://github.com/dfoley84/Horizon-Vue/blob/main/vsphere/frontend/src/assets/2023-09-24%2016_12_39-search.py%20-%20Horizon%20-%20Visual%20Studio%20Code.png?raw=true)


# Horizon Portal
Portal to allow end users to powercycle their virtual Horzion VDI's
while also allowing users to connect to their VDI over horizon console, or ssh to a linux machine from the web broswer

# Actions Required
    1) PowerShell Script to pull Horizon VDI from Horizon to Database, 
    2) update logic code -> only allow Admins access to Search / Build vDesks
    3) Create Jenkins Free Style Jobs for Each PowerAction
    3) Configure RabbitMQ to Take PowerAction Required 
    6) Python Script to Get Message and Trigger Remote Jenkins -> Watcher for new messages. 


