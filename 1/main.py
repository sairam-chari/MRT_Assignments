class Vehicle:
    def __init__(self,vehicle,make,model,year,rate) -> None:
        self.vehicle_id = vehicle
        self.make = make
        self.model = model
        self.year = year
        self.rate = rate
        self.availability = True
        self.customer = None
        self.duration = 0
    def __str__(self) -> str:
        return f"{self.vehicle_id}"    
    def get_vehicle_details(self):
        print()
        print(f"Vehicle ID: {self.vehicle_id}")
        print(f"Make: {self.make}")
        print(f"Model: {self.model}")
        print(f"Year: {self.year}")
        print(f"Rate: {self.rate}")
        print(f"Availability: {self.availability}")
        if not self.availability:
            print(f"Customer ID: {self.customer.customer_id}")
            print (f"Customer Contact: {self.customer.contact}")
            print(f"Duration: {self.duration}")
        print()
    def rent_vehicle(self,customer,duration,discount=False):
        if self.customer == None:
            self.customer = customer
            self.availability =False
            print(f"Vehicle {self.vehicle_id} rented by customer {customer.customer_id}")
            customer.current_rental = self
            self.duration = duration
            customer.history.append(self)
        else :
            print(f"Vehicle is already rented by customer {self.customer.customer_id}")

    def return_vehicle(self):
        if self.customer == None:
            print(f"Vehicle is already available")
        self.availability = True
        print(f"Vehicle {self.vehicle_id} returned by customer {self.customer.customer_id}")
        self.customer = None
    

 

class LuxuryVehicle(Vehicle):
    def __init__(self,id,make,model,year,rate,extra_features = []) -> None:
        super().__init__(id,make,model,year,rate)
        self.rate = rate * 1.2
        self.extra_features = extra_features

class Customer:
    def __init__(self,id,name,contact) -> None:
        self.customer_id = id
        self.name = name
        self.contact = contact
        self.history = []
        self.current_rental = None
    def details(self):
        print(f"Customer ID: {self.customer_id}")
        print(f"Name: {self.name}")
        print(f"Contact: {self.contact}")
        if self.current_rental:
            print(f"Current Rental: {self.current_rental.vehicle_id}")
        else :
            print(f"Current Rental: None")
    def rental_history(self):
        print(f"Rental History: {self.history}")

class RegularCustumer(Customer):
    def __init__(self,id,name,contact) -> None:
        super().__init__(id,name,contact)
        self.factor = 1
        self.loyalty_points = 0

class PremiumCustomer(Customer):
    def __init__(self,id,name,contact) -> None:
        super().__init__(id,name,contact)
        self.factor = 0.9

class RentalManager():
    def __init__(self) -> None:
        self.vehicles = []
        self.luxury_vehicles = []
        self.Regularcustomers = []
        self.Premiumcustomers = []
    def add_vehicle(self,vehicle,make,model,year,rate,luxury=False):
        if not luxury: 
            self.vehicles.append(Vehicle(vehicle,make,model,year,rate))
        else:
            self.luxury_vehicles.append(LuxuryVehicle(vehicle,make,model,year,rate))
    def add_customer(self,customer_id,name,contact,premium=False):
        if premium:
            self.Premiumcustomers.append(PremiumCustomer(customer_id,name,contact))
        else:
            self.Regularcustomers.append(RegularCustumer(customer_id,name,contact))

    def rent_vehicle(self,vehicle_id,customer_id,discount=False): #Didnt really use discount here
        vehicle = None
        customer = None
        for v in self.vehicles:
            if v.vehicle_id == vehicle_id:
                vehicle = v
                break
        for v in self.luxury_vehicles:
            if v.vehicle_id == vehicle_id:
                vehicle = v
                break    
        for c in self.Regularcustomers:
            if c.customer_id == customer_id:
                customer = c
                discount = False
                break
        for c in self.Premiumcustomers:
            if c.customer_id == customer_id:
                customer = c
                break
        if vehicle and customer:
            vehicle.rent_vehicle(customer,discount)
        else:
            if  not vehicle:
                print(f"Vehicle with ID {vehicle_id} not found")
            if not customer:
                print(f"Customer with ID {customer_id} not found")

    def return_vehicle(self,vehicle_id,customer_id):
        vehicle = None
        customer = None
        for v in self.vehicles:
            if v.vehicle_id == vehicle_id:
                vehicle = v
                break
        for v in self.luxury_vehicles:
            if v.vehicle_id == vehicle_id:
                vehicle = v
                break
        for c in self.Regularcustomers:
            if c.customer_id == customer_id:
                customer = c
                break
        for c in self.Premiumcustomers:
            if c.customer_id == customer_id:
                customer = c
                break
        if vehicle and customer:
            vehicle.return_vehicle(customer)
        else:
            if  not vehicle:
                print(f"Vehicle with ID {vehicle_id} not found")
            if not customer:
                print(f"Customer with ID {customer_id} not found")
    def list_available_vehicles(self):
        print ("Normal Vehicles")
        for v in self.vehicles:
            if v.availability:
                v.get_vehicle_details()
        print ("Luxury Vehicles")
        for v in self.luxury_vehicles:
            if v.availability:
                v.get_vehicle_details()
    def list_rented_vehicles(self):
        print ("Normal Vehicles")
        for v in self.vehicles:
            if not v.availability:
                v.get_vehicle_details()
        print ("Luxury Vehicles")
        for v in self.luxury_vehicles:
            if not v.availability:
                v.get_vehicle_details()
    def remove_vehicle(self,vehicle_id):
        for v in self.vehicles:
            if v.vehicle_id == vehicle_id:
                self.vehicles.remove(v)
                print(f"Vehicle {vehicle_id} removed")
                break
        for v in self.luxury_vehicles:
            if v.vehicle_id == vehicle_id:
                print(f"Vehicle {vehicle_id} removed")
                self.luxury_vehicles.remove(v)
                break


def help():
    print("[1] Rent Vehicle")
    print("[2] Return Vehicle")
    print("[3] List Available Vehicles")
    print("[4] List Rented Vehicles")
    print("[5] Remove Vehicle")
    print("[6] Add Vehicle")
    print("[7] Add Customer")
    print("[0] Exit")
    print()
def cli():
    while True:
        x = input("> ").lower().strip()
        if x == "0":
            break
        else:
            help()
        if x == "1":
            vehicle_id = input("Vehicle ID: ")
            customer_id = input("Customer ID: ")
            discount = input("Discount(y/n): ")
            discount = True if discount == "y" else False
            
            
            rm.rent_vehicle(vehicle_id,customer_id,discount)  
        elif x == "2":
            vehicle_id = input("Vehicle ID: ")
            for v in rm.vehicles:
                if v.vehicle_id == vehicle_id:
                    vehicle = v
                    break
            for v in rm.luxury_vehicles:
                if v.vehicle_id == vehicle_id:
                    vehicle = v
                    break
            vehicle.return_vehicle()
        elif x == "3":
            rm.list_available_vehicles()
        elif x == "4":
            rm.list_rented_vehicles()
        elif x == "5":
            vehicle_id = input("Vehicle ID: ")
            rm.remove_vehicle(vehicle_id)
        elif x == "6":
            vehicle_id = input("Vehicle ID: ")
            make = input("Make: ")
            model = input("Model: ")
            year = int(input("Year: "))
            rate = float(input("Rate: "))
            luxury = input("Luxury(y/n): ").strip().lower()
            luxury = True if luxury == "y" else False
            rm.add_vehicle(vehicle_id,make,model,year,rate,luxury)
        elif x == "7":
            customer_id = input("Customer ID: ")
            name = input("Name: ")
            contact = input("Contact: ")
            premium = input("Premium(y/n): ").strip().lower()
            premium = True if premium == "y" else False
            rm.add_customer(customer_id,name,contact,premium)
if __name__ == "__main__":
    rm = RentalManager()
    rm.add_vehicle("1","Toyota","Corolla",2015,100) #Example vehicles
    rm.add_vehicle("2","Ferrari","F40",1990,1000,True)
    rm.add_customer("1","John","123456")

    cli()           
                
                
            
    

  