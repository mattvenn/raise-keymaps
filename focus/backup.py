#! /usr/bin/env python
import serial
import time
import argparse

def run_cmd(ser, cmd):
    print(cmd)
    ser.write (cmd + "\n")
    output = ""
    while True:
        resultLine = ser.readline ()

        if resultLine == "\r\n" or resultLine == "\n":
            resultLine = " "
        else:
            resultLine = resultLine.rstrip ()

        if resultLine == ".":
            break

        if resultLine:
            output += resultLine

    return output

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="backup and restore layers to Dygma Raise")
    parser.add_argument('--backup', action='store_true')
    parser.add_argument('--restore', action='store_true')
    parser.add_argument('--port', default='/dev/ttyACM0')
    parser.add_argument('--filename', required=True)

    args = parser.parse_args()

    if not (args.backup or args.restore or args.custom):
        exit("must choose either backup or restore")
    settings = ["keymap.custom", "colormap.map", "palette", "keymap.onlyCustom", "hardware.keyscan", 
                "idleLeds.idleTimeLimit", "led.mode"]
    with serial.Serial (args.port, 9600, timeout = 1) as ser:
        if args.backup:
            for conf in settings:
                with open(args.filename + conf, 'w') as fh:
                    data = run_cmd(ser, conf)
                    fh.write(data + "\n")
            
        if args.restore: 
            for conf in settings:
                with open(args.filename + conf, 'r') as fh:
                    data = fh.readline()
                    data = data.strip()
                    print(run_cmd(ser, "%s %s" % (conf, data)))
