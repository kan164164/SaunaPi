#!/usr/bin/python 
# coding:utf-8 

#リレーの制御にタクトスイッチを連携
#GPIO24をタクトスイッチ
#GPIO25をリレーのIN
#タクトスイッチONでファイルに時刻格納

import time
import smbus
import RPi.GPIO as GPIO
import datetime
import os

GPIO.setmode(GPIO.BCM)
GPIO.setup(24,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#リレー初期化
GPIO.setup(25, GPIO.OUT,initial=True)
GPIO.output(25, True)

sw_counter = 0
iRelay=0

while True:
    sw_status = GPIO.input(24)
    #print(sw_status)
    #print(iRelay)
    if sw_status == 0:
        sw_counter = sw_counter + 1
        if iRelay == 0:
            #0.1秒押し
            if sw_counter >= 1:
                #print("長押し検知・リレー起動")
                #リレー起動
                iRelay = 1

                GPIO.setup(25, GPIO.OUT,initial=True)
                GPIO.output(25, False)

                #ファイル格納
                t = datetime.datetime.today()
                #print ("起動：%s" % (t.strftime("%Y/%m/%d %H:%M:%S")))
                f = open('./tr_' + t.strftime("%Y%m%d") + '.txt', mode='a', encoding='utf-8')
                f.write("起動," + t.strftime("%Y/%m/%d %H:%M:%S") + "\n")
                f.close()

                sw_counter = 0
    elif sw_status == 1:
        if iRelay == 1:
           #リレーが起動していればリレー停止
           iRelay = 0
           sw_counter = 0
           GPIO.output(25, True)

           #ファイル格納
           t = datetime.datetime.today()
           #print ("停止：%s" % (t.strftime("%Y/%m/%d %H:%M:%S")))
           f = open('./tr_' + t.strftime("%Y%m%d") + '.txt', mode='a', encoding='utf-8')
           f.write("停止," + t.strftime("%Y/%m/%d %H:%M:%S") + "\n")
           f.close()
    else:
        sw_counter = 0
    time.sleep(.1)

