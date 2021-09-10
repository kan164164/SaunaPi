#!/usr/bin/python 
# coding:utf-8 
import time
import LCD1602
import smbus
import RPi.GPIO as GPIO
import os
 
GPIO.setmode(GPIO.BCM)
 
#GPIO18pinを入力モードとし、pull up設定とします 
GPIO.setup(18,GPIO.IN,pull_up_down=GPIO.PUD_UP)
 
sw_counter = 0
while True:
    sw_status = GPIO.input(18)
    if sw_status == 0:
        sw_counter = sw_counter + 1
        if sw_counter >= 50:
            #print("長押し検知！")
            try:
                smb = smbus.SMBus(1)
                addr = 0x44
                os.system("sudo kill -9 `ps aux|grep python3|grep SHTLCD|grep -v grep|awk '{print $2}'`")
                os.system("sudo kill -9 `ps aux|grep python3|grep tact_relay|grep -v grep|awk '{print $2}'`")
                time.sleep(3)
                LCD1602.init(0x27, 1) # init(slave address, background light)
                LCD1602.write(0, 0, 'Shutdown')
                LCD1602.write(0, 1, '')	
                time.sleep(10)
                LCD1602.init(0x27, 1) # init(slave address, background light)
                LCD1602.write(0, 0, 'Shutdown!!')
                LCD1602.write(0, 1, '')	
            except:
                pass
            os.system("sudo shutdown -h now")
            break
    else:
        sw_counter = 0

    time.sleep(0.1)


