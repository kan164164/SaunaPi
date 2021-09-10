#!/usr/bin/env python3
import LCD1602
import smbus
import time
import datetime

def main():

	t = datetime.datetime.today()
	fp = open('./tmp/sht31.txt', mode='a', encoding='utf-8')
	fp.write('SHT31起動:' + t.strftime("%Y/%m/%d %H:%M:%S") + "\n")
	fp.close()

	#i=0
	try:
		smb = smbus.SMBus(1)
		addr = 0x44
	except:
		LCD1602.write(0, 0, 'ERROR           ')
		LCD1602.write(0, 1, '                ')	
		exit()
		
	while True:
		try:
			t = datetime.datetime.today()
			# データの読み出し
			smb.write_i2c_block_data(addr, 0x2C, [0x06])
			time.sleep(0.1)
			data = smb.read_i2c_block_data(addr, 0x00, 6)
			# 気温
			st = data[0] <<8 | data[1]
			roomtemp = -45 + (175 * st/float((2**16 - 1)))
			# 湿度
			srh = data[3] <<8 | data[4]
			roomhum = 100 * srh/ float((2**16 - 1))

			print ("時間：%s, 湿度: %-3.1f %%, 温度: %-3.1f C" % (t.strftime("%Y/%m/%d %H:%M:%S") , roomhum , roomtemp))

			#i = i + 1
			#if i >= 5:
			#	break
			f = open('./sht31_' + t.strftime("%Y%m%d") + '.txt', mode='a', encoding='utf-8')
			f.write(t.strftime("%Y/%m/%d %H:%M:%S") + ",%-2.2f,%2.2f" % (roomtemp,roomhum) + "\n")
			f.close()
			f2 = open('./tmp/sht31_' + t.strftime("%Y%m%d") + '.txt', mode='a', encoding='utf-8')
			f2.write(t.strftime("%Y/%m/%d %H:%M:%S") + ",%-2.2f,%2.2f" % (roomtemp,roomhum) + "\n")
			f2.close()

			#LCD1602.write(0, 0,  ("\xb5\xdd\xc4\xde:%-3.1f" % (roomtemp)) + (" \xbc\xc2\xc4\xde:%-3.1f" % (roomhum)))
			LCD1602.write(0, 0,  ("%-2.1f\xdfC" % (roomtemp)) + (" %-2.1f%%" % (roomhum)))
			if (roomtemp >= 60):
				LCD1602.write(0, 1,  ("SAUNA!!         "))
			else:
				LCD1602.write(0, 1,  ("NOT SAUNA!!     "))
		except:
			try:
				LCD1602.write(0, 0, 'ERROR           ')
				LCD1602.write(0, 1, '                ')	
			except:
				pass
		time.sleep(10)

def setup():
	LCD1602.init(0x27, 1) # init(slave address, background light)
	LCD1602.write(0, 0, '')
	LCD1602.write(0, 1, '')


def destroy2():
	LCD1602.init(0x27, 0) # init(slave address, background light)
	LCD1602.write(0, 0, '')
	LCD1602.write(0, 1, '')	


if __name__ == '__main__':
	setup()
	try:
		main()
	except KeyboardInterrupt:
		destroy2()

