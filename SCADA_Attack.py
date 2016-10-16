#Daniel J. Cowdery - 2016
#IFN701 - Network Attack Dataset (Masquerading Attack)

from Conveyor_Belt import*
from WaterTank import*
from Reactor import*
from Directory import *


def Restart(device):
    print "\nResetting connection..."
    device.client.disconnect()
    device.client.destroy()
    time.sleep(5)
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

        return device

    except Snap7Exception:
        print "\nCould not connect to victim. Terminating application!"

try:
    target_chosen = False
    target = "0"

    while (not target_chosen):
        print "\nAVAILABLE TARGETS\n"
        print "1: Conveyor Belt"
        print "2: Water Tank"
        print "3: Reactor"
        target = raw_input("Please select a target system...")

        if target == "1":
            victim = ConveyorBelt()
            target_chosen = True

        elif target == "2":
            victim = WaterTank()
            target_chosen = True

        elif target == "3":
            victim = Reactor()
            target_chosen = True

        else:
            print "Please choose a valid option"



    while (victim.run):

        if victim.restart:
            victim = Restart(victim)

        victim.PrintOptions()
        victim.CheckStatus()
        victim.LaunchAttack()


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
    victim.Exit()

except Snap7Exception:
    print "\nCould not connect to victim. Terminating application!"