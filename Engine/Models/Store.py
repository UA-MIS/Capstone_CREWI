from flask import abort

import printFormatting
import globalStatus

class Store:
    def __init__(self, id, address, latitude, longitude):
        try:
            self.id = id
            self.address = address
            self.latitude = latitude
            self.longitude = longitude
            self.distance = float(0)
        except Exception as e:
            # print issue to terminal and update status
            printFormatting.printError(str(e))
            globalStatus.addFail("STORE_INIT_FAIL")

    def __str__(self):
        return "Store ID: " + str(self.id) + "\tAddress: " + str(self.address) + "\tLatitude: " + str(self.latitude) + "\tLongitude: " + str(self.longitude) + "\tDistance: " + str(self.distance)