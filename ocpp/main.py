# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from jsonschema import validate
import json

schem = {
    "chargePointModel": "ELA007C01",
    "chargePointVendor": "EVAR",
    "chargePointSerialNumber": "EVSCA070007",
    "firmwareVersion": "0.0.13",
    "rssi": -42,
    "imsi": "450061222990181"
  }

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.

    schema = json.loads(open("ocpp-1.6-schemas/BootNotification.json").read())
    print(schema)
    validate(instance=schem, schema=schema)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
