import argparse
import os
import shutil

from time import sleep

import lumos
from lumos.lumos import Lumos, LumosPowerState, LumosMode, LumosColor
from recom import RecomDevice, RecomDeviceException
from recom.backend.usb import get_vid_pid_on_port
from recom.util import get_drive_mount_point_from_usb_port_path


def print_info():
    board = Lumos()
    print(f"Number of LEDs = {board.interface.get_num_leds()}")
    print(f"Power state = {board.interface.get_power_state()}")
    print(f"Voltage = {board.interface.get_voltage_reading()}mV")
    print(f"Current = {board.interface.get_current_reading()}mA")
    print(f"Brightness = {board.interface.get_brightness()}")

def power_ctrl(arg):
    board = Lumos()
    if "on" in arg or "ON" in arg or "On" in arg:
        print("Turning power ON")
        board.interface.set_power_state(LumosPowerState.POWER_ON)
    else:
        print("Turning power OFF")
        board.interface.set_power_state(LumosPowerState.POWER_OFF)

def set_color(arg):
    board = Lumos()
    board.interface.set_power_state(LumosPowerState.POWER_ON)
    board.interface.set_mode(LumosMode.MANUAL)
    pattern = arg[0].lower()
    try:
        (r, g, b) = LumosColor[arg[0].lower()]
    except Exception as exp:
        print(f"Unknown color {arg[0]}, {exp}")
        return
    print(f"Setting color: {arg[0].lower()}")
    board.interface.set_all(r, g, b)


def set_led(arg):
    if len(arg) == 4:
        led_index = int(arg[0])
        r = int(arg[1])
        g = int(arg[2])
        b = int(arg[3])
    else:
        print("Not enough parameters (requires 4 - index, r, g, b)")
        return
    board = Lumos()
    board.interface.set_power_state(LumosPowerState.POWER_ON)
    board.interface.set_mode(LumosMode.MANUAL)
    print(f"Setting LED at index {led_index} to ({r}, {g}, {b})")
    board.interface.set_one(led_index, r, g, b)


def set_brightness(arg):
    brightness = int(arg[0])
    if brightness > 100:
        print(f"ERROR: Brightness should be a number between 0 and 100. You typed {brightness}")
        return
    print(f"Setting brightness to {brightness}")
    board = Lumos()
    board.interface.set_brightness(brightness)


def clear_all():
    board = Lumos()
    board.interface.clear_all()


def update_fw(arg):
    if arg is None:
        print("Missing binary file paramter")
    binary_file = arg[0]

    board = Lumos()
    print(f"Found Lumos board {board.interface.device.get_serial()}")
    print(f"Current FW Rev = {board.interface.device.getFwRev()}")

    # Check if the passed file is a valid file (does exist)
    file_ref = os.path.join(os.getcwd(), binary_file)
    if not os.path.exists(file_ref):
        print(f"ERROR: Cannot find the file/path {file_ref}")

    # Get port path and reset board
    port_path = board.interface.device._comsBackend.get_device_path()
    old_vp = get_vid_pid_on_port(port_path)

    # Reset board
    print("Rebooting to bootloader... ", end='')
    board.interface.device.reset(2)
    sleep(0.5)

    while True:
        new_vp = get_vid_pid_on_port(port_path)
        if new_vp is not None:
            if new_vp[0] != old_vp[0] or new_vp[1] != old_vp[1]:
                print("DONE")
                print("Found device with VID=%04X, PID=%04X" % (new_vp[0], new_vp[1]))
                break
        sleep(0.1)

    print("Looking for mass storage device... ", end='')
    for i in range(10):
        mp = get_drive_mount_point_from_usb_port_path(port_path, new_vp)
        if mp is not None:
            break
        sleep(1)
    if mp == None:
        print("\nERROR: Bootloader not found")
        return False
    else:
        print(mp)
    print(f"Updating device with {binary_file}")
    if not os.path.exists(mp):
        print(f"ERROR: Bootloader path does not exist ({mp})")
        return False
    dest_ref = os.path.join(mp, binary_file)
    try:
        shutil.copy(file_ref, dest_ref)
    except IOError as exp:
        print(f"ERROR: Failed to copy file {binary_file} ({exp})")
        return False
    print("DONE")
    return True


def cli(argv):
    parser = argparse.ArgumentParser(description="Lumos CLI to interract with an LED controller board.")
    parser.add_argument("cmd", type=str, help="Command/Action")
    parser.add_argument('--version', action='version', version=lumos.__version__,
                                                help="Print package version")
    parser.add_argument('-S', '--serial', help='Serial number to search for')

    args, remaining_args = parser.parse_known_args(argv)

    if args.cmd == "info":
        print_info()
    elif args.cmd == "power":
        power_ctrl(remaining_args)
    elif args.cmd == "color":
        set_color(remaining_args)
    elif args.cmd == "set":
        set_led(remaining_args)
    elif (args.cmd == "clear"):
        clear_all()
    elif args.cmd == "brightness":
        set_brightness(remaining_args)
    elif args.cmd == "update":
        update_fw(remaining_args)
