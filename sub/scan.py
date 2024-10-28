import bluepy
import cv2


key = cv2.waitKey(1)


while(True):
    scanner = bluepy.btle.Scanner(0)
    devices = scanner.scan(3)
    for device in devices:
         if device.addr == "f9:49:3e:93:cf:25":
              print('======================================================')
    #           print('address : %s' % device.addr)
    #           print('addrType: %s' % device.addrType)
              print('RSSI    : %s' % device.rssi)
    #           print('Adv data:')
              for (adtype, desc, value) in device.getScanData():
                print(' (%3s) %s : %s ' % (adtype, desc, value))
    if key == ord('q'):
        break
