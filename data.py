carwashes: list = []
employees: list = []
clients: list = []

def get_carwashes()-> list:
    return [obj.name for obj in carwashes]