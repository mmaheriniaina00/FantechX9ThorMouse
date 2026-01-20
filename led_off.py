#!/usr/bin/env python3
"""
Simple command-line script to turn off Fantech X9 Thor mouse LED
Usage: python led_off.py
"""

import usb.core
import usb.util
import sys


class MouseLEDController:
    def __init__(self):
        self.x9_vendorid = 0x18f8
        self.x9_productid = 0x0fc0
        self.bmRequestType = 0x21
        self.bRequest = 0x09
        self.wValue = 0x0307
        self.wIndex = 0x0001
        self.mouse = None
        self.conquered = False

    def find_device(self):
        """Find the mouse device"""
        print("Looking for Fantech X9 Thor mouse...")
        self.mouse = usb.core.find(idVendor=self.x9_vendorid, idProduct=self.x9_productid)
        
        if self.mouse is None:
            print("ERROR: Device not found. Please check:")
            print("  - Mouse is plugged in")
            print("  - USB connection is working")
            return False
        
        print("Device found!")
        return True

    def check_permissions(self):
        """Check if we have permission to access the device"""
        try:
            is_busy = self.mouse.is_kernel_driver_active(self.wIndex)
            return True
        except usb.core.USBError as e:
            if e.errno == 13:
                print("ERROR: Insufficient permissions!")
                print("Try running with sudo or add a udev rule:")
                print("https://wiki.archlinux.org/index.php/udev#Accessing_firmware_programmers_and_USB_virtual_comm_devices")
                return False
            print(f"USB Error: {e}")
            return False

    def conquer(self):
        """Take control of the device"""
        try:
            if self.mouse.is_kernel_driver_active(self.wIndex):
                self.mouse.detach_kernel_driver(self.wIndex)
            usb.util.claim_interface(self.mouse, self.wIndex)
            self.conquered = True
            return True
        except Exception as e:
            print(f"Failed to claim device: {e}")
            return False

    def liberate(self):
        """Release the device back to the kernel"""
        if self.conquered:
            try:
                usb.util.release_interface(self.mouse, self.wIndex)
                self.mouse.attach_kernel_driver(self.wIndex)
                self.conquered = False
            except Exception as e:
                print(f"Warning: Failed to release device: {e}")

    def create_led_off_payload(self):
        """Create payload to turn off LED"""
        payload = [0x07, 0x13, 0x7F, 0x87, 0x00, 0x00, 0x00, 0x00]
        return payload

    def send_payload(self, payload):
        """Send payload to the mouse"""
        try:
            self.mouse.ctrl_transfer(
                self.bmRequestType,
                self.bRequest,
                self.wValue,
                self.wIndex,
                payload
            )
            return True
        except Exception as e:
            print(f"Failed to send payload: {e}")
            return False

    def turn_off_led(self):
        """Main function to turn off the LED"""
        if not self.find_device():
            return False
        
        if not self.check_permissions():
            return False
        
        if not self.conquer():
            return False
        
        print("Turning off LED...")
        payload = self.create_led_off_payload()
        success = self.send_payload(payload)
        
        self.liberate()
        
        if success:
            print("LED turned off successfully!")
            return True
        else:
            print("Failed to turn off LED")
            return False


def main():
    controller = MouseLEDController()
    success = controller.turn_off_led()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()