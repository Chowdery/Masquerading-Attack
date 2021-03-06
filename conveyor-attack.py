#Daniel J. Cowdery - 2016
#IFN701 - Network Attack Dataset (Masquerading Attack)

from Conveyor_Belt import*

from Directory import *


def Restart(device):
    print "\nResetting connection..."
    device.client.disconnect()
    device.client.destroy()
    time.sleep(5)
    try:
        device = ConveyorBelt()
        print "Reconnected to Conveyor Belt\n"
        return device
    except Snap7Exception:
        print "\nCould not connect to victim. Terminating application!"

try:
    victim = ConveyorBelt()

    while (victim.run):

        if victim.restart:
            victim = Restart(victim)

        victim.PrintOptions()
        victim.CheckStatus()

        if victim.option == 0:
            victim.MotorOn()

        if victim.option == 1:
            victim.MotorOff()

        elif victim.option == 3:
            victim.AltTestFlopgateLeft()

        elif victim.option == 99:
            victim.PrintStatus()

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