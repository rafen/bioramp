import machine
import urequests


class BioRamp(object):
    url = 'https://api.thingspeak.com/update?api_key=AUSV15I0KD94VFX6'

    def __init__(self):
        self.spi = machine.SPI(1, baudrate=200000, polarity=0, phase=0)
        self.spi.init(baudrate=200000)
        self.cs = machine.Pin(15, machine.Pin.OUT)
        self.cs.on()

    def read(self, size=48, export=True):
        self.cs.off()
        self.spi.write(b'. ')
        res = self.spi.read(size, 0xff)
        self.cs.on()

        results = res.split()
        # ignore results that do no have several params
        if len(results) < 4:
            return res

        # read params from SPI and generate query args
        params = []
        if export and len(results) > 4:
            if b'C' in results[1]:
                params.append("field1={}".format(results[0].decode('utf-8')))
            if b'%' in results[3]:
                params.append("field2={}".format(results[2].decode('utf-8')))
            if b'M' in results[4]:
                params.append("field3={}".format(results[4][1:].decode('utf-8')))
            if b'R' in results[5]:
                params.append("field4={}".format(results[5][1:].decode('utf-8')))
            if b'M' in results[6]:
                params.append("field5={}".format(results[6][1:].decode('utf-8')))
            if b'S' in results[7]:
                params.append("field6={}".format(results[7][1:].decode('utf-8')))
            if b'L' in results[8]:
                params.append("field7={}".format(results[8][1:].decode('utf-8')))

            response = urequests.get('{}&{}'.format(self.url, '&'.join(params)))
            response.close()
            print('{}&{}'.format(self.url, '&'.join(params)))
        return res
