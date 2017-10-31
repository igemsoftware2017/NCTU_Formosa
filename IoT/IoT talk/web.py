import time, DAN, requests, random


ServerIP = '140.113.199.199' #Change to your IoTtalk IP or None for autoSearching
Reg_addr = None # if None, Reg_addr = MAC address

DAN.profile['dm_name']='data_show'
DAN.profile['df_list']=['get_Precp', 'get_RH', 'get_StnPres', 'get_Temperature']
DAN.profile['d_name']= None # None for autoNaming
DAN.device_registration_with_retry(ServerIP, Reg_addr)

url = 'https://api.thingspeak.com/update?api_key=W0286CQGMR5QO11U'

while True:
    try:
       value_1 = DAN.pull('get_Precp')
       value_2 = DAN.pull('get_RH')
       value_3 = DAN.pull('get_StnPres')
       value_4 = DAN.pull('get_Temperature')
       
        
       
       url += "&field1=" + str(value_1[0]) + "&field2=" + str(value_2[0]) +"&field3=" + str(value_3[0]) +"&field4=" + str(value_4[0])
       
       requests.get(url)
       
       
       print(value_1)
       print(value_2)
       print(value_3)
       print(value_4)
         
    except Exception as e:
        print(e)
        DAN.device_registration_with_retry(ServerIP, Reg_addr)
    time.sleep(5.0)
    

    
    
    
    
    
    
    
    
