#Daniel J. Cowdery - 2016
#IFN701 - Network Attack Dataset (Masquerading Attack)

from Conveyor_Belt import*
from WaterTank import*
from Reactor import*
from Directory import *
from datetime import*
from time import*

log = []


def TimestampLog(log_msg):
    log_item = str(datetime.now()) + " " +log_msg
    print log_item
    log.append(log_item)


def WriteToLog():
    file_name = "Test_Log_File.log"
    file = open(file_name, 'w')
    for l in log:
        file.write(l + "\n")
    file.close()
    print "Logs saved in", file_name


def Restart(device):
    print "\nResetting connection..."
    device.client.disconnect()
    device.client.destroy()
    sleep(5)
    try:
        if target == "1":
            device = ConveyorBelt()
            print "Reconnected to Conveyor Belt\n"
        elif target == "2":
            device = WaterTank()
            print "Reconnected to Water Tank\n"
        elif target == "3":
            device = Reactor()
            print "Reconnected to Reactor\n"

        else:
            print "Failed to reconnect to device\n"

        return device

    except Snap7Exception:
        print "\nCould not connect to victim. Terminating application!"




try:
    target_chosen = False
    target = "0"
    device_type = ""
    attacks = {}

    while (not target_chosen):
        print "\nAVAILABLE TARGETS\n"
        print "1: Conveyor Belt"
        print "2: Water Tank"
        print "3: Reactor"
        target = raw_input("Please select a target system...")

        if target == "1":
            victim = ConveyorBelt()
            device_type = "Conveyor"
            target_chosen = True
            attacks = {
                0: victim.MotorOn,
                1: victim.FloodMotorOn,
                2: victim.MotorOff,
                3: victim.FloodMotorOff,
                4: victim.FlopgateLeft,
                5: victim.FloodFlopgateLeft,
                6: victim.PrintStatus,
            }

        elif target == "2":
            victim = WaterTank()
            device_type = "Tank"
            target_chosen = True

        elif target == "3":
            victim = Reactor()
            device_type = "Reactor"
            target_chosen = True

        else:
            print "Please choose a valid option"


    while (victim.run):

        # if victim.restart:
        #     victim = Restart(victim)

        victim.PrintOptions()
        victim.CheckStatus()
        #victim.LaunchAttack()

        if device_type == "Conveyor":
            if victim.option in attacks.keys():
                TimestampLog(attacks[victim.option].__name__ + " START")
                attacks[victim.option]()
                TimestampLog(attacks[victim.option].__name__ + " END")

            # if victim.option == 0:
            #     victim.MotorOn()
            #
            # elif victim.option == 1:
            #     victim.FloodMotorOn()
            #
            # elif victim.option == 2:
            #     victim.MotorOff()
            #
            # elif victim.option == 3:
            #     victim.FloodMotorOff()
            #
            # elif victim.option == 4:
            #     victim.FlopgateLeft()
            #
            # elif victim.option == 5:
            #     victim.FloodFlopgateLeft()
            #
            # elif victim.option == 99:
            #     victim.PrintStatus()



        elif device_type == "Reactor":
            if victim.option == 0:
                victim.ReactorOn()

            if victim.option == 1:
                victim.ReactorOff()

            elif victim.option == 2:
                victim.ChangeScaledPressure()

            elif victim.option == 3:
                victim.ChangeSolenoidOn()

            elif victim.option == 99:
                victim.PrintStatus()

        #elif device_type == "Tank":


        #elif victim.option == 2:
        #    victim.SetFlopgateRight()

        #elif victim.option == 22:
        #    victim.TestSetFlopgateRight()

        #elif victim.option == 222:
        #    victim.AltTestFlopgateRight()

        #elif victim.option == 3:
        #    victim.SetFlopgateLeft()

        #elif victim.option == 33:
        #    victim.TestSetFlopgateLeft()

        #elif victim.option == 7:
        #    victim.ToggleConveyorDirection()

        #elif victim.option == 8:
        #    victim.ToggleFlopgateDirection()

        #elif victim.option == 10:
        #    victim.AltToggleMotor()



except KeyboardInterrupt:
    print "\nTerminating application..."
    WriteToLog()
    victim.Exit()

except Snap7Exception:
    print "\nCould not connect to victim. Terminating application!"