import printFormatting
import globalStatus

# STORE.PY: Class for Store Locations in the database

class Store:
    # constructor takes in all the arguments, distance is initialized to 0
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

    # allows stores to be printed to the terminal, useful for debugging
    def __str__(self):
        return "Store ID: " + str(self.id) + "\tAddress: " + str(self.address) + "\tLatitude: " + str(self.latitude) + "\tLongitude: " + str(self.longitude) + "\tDistance: " + str(self.distance)