from server.send_udp_msg import udpMsg


class Button:

    def __init__(self, name, tag, hardwarebutton, linbutton, columbutton, sizebutton, color, colorup, options):
        self.options = options
        self.velue = 0
        self.tag = tag
        self.name = name
        self.sizebutton = sizebutton
        self.linbutton = linbutton
        self.columbutton = columbutton
        self.hardwarebutton = hardwarebutton
        self.color = color
        self.colorup = colorup
        self.coloraction = color
        self.status = False

    def buttonaction(self):

        if self.status:
            self.coloraction = self.color
            self.status = False
            self.velue = self.options[0]
        else:
            self.coloraction = self.colorup
            self.status = True
            self.velue = self.options[1]

        print('Action: ' + self.name + (' Ligado' if self.status else ' Desligado'))
        udpMsg(['{ ' + self.tag + ' : ' + str(self.velue) + ' }'])

    def buttonoptions(self):
        self.velue = (self.velue + 1) % len(self.options)
        print('Action:' + self.name + ' Val:' + str(self.velue))
        return self.options[self.velue]

    def buttonvelue(self):
        return self.options[self.velue]

