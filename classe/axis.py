from server.send_udp_msg import udpMsg


class Axis:

    def __init__(self, name, tag, hardwarebutton, initvelueout, invertveluein, minveluein, maxveluein, minvelueout,
                 maxvelueout, color, colorup):
        self.name = name
        self.tag = tag
        self.hardwarebutton = hardwarebutton
        self.invertveluein = invertveluein
        if self.invertveluein:
            self.maxveluein = minveluein
            self.minveluein = maxveluein
        else:
            self.maxveluein = maxveluein
            self.minveluein = minveluein

        self.maxvelueout = maxvelueout
        self.maxvelueoutset = maxvelueout
        self.minvelueout = minvelueout
        self.color = color
        self.colorup = colorup
        self.coloraction = color
        self.veluein = 0
        self.velueout = initvelueout

    def setvelue(self, value):
        print('Axis: ' + str(self.name) + ' Val: ' + str(self.getvelueout()))

        if (value >= self.minveluein) and (value <= self.maxveluein):
            self.veluein = value

            if self.invertveluein:
                if self.maxvelueout != self.maxvelueoutset:
                    self.velueout = self.map(value, self.maxveluein, self.minveluein, self.minvelueout,
                                             self.maxvelueoutset)
                    udpMsg(['{ ' + self.tag + ' : ' + str(self.getvelueout()) + ' }'])
                else:
                    self.velueout = self.map(value, self.maxveluein, self.minveluein, self.minvelueout,
                                             self.maxvelueoutset)
                    udpMsg(['{ ' + self.tag + ' : ' + str(self.getvelueout()) + ' }'])
            else:
                if self.maxvelueout != self.maxvelueoutset:
                    self.velueout = self.map(value, self.minveluein, self.maxveluein, self.minvelueout,
                                             self.maxvelueout)
                    udpMsg(['{ ' + self.tag + ' : ' + str(self.getvelueout()) + ' }'])
                else:
                    self.velueout = self.map(value, self.minveluein, self.maxveluein, self.minvelueout,
                                             self.maxvelueout)
                    udpMsg(['{ ' + self.tag + ' : ' + str(self.getvelueout()) + ' }'])

        else:
            print('Velue fora dos valores Min e Max defindos')

    def setmaxout(self, velue):
        if (velue >= self.minvelueout) and (velue <= self.maxvelueout):
            self.maxvelueoutset = velue
            print('Set maxvelueoutset: ' + str(velue))
        else:
            print('VelueMAX fora dos valores Min e Max defindos')

    def getmaxout(self):
        return self.maxvelueout

    def getvelueout(self):
        return self.velueout

    def getveluein(self):
        return self.veluein

    def map(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
