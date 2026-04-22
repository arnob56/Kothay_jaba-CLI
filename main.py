from abc import ABC, abstractmethod
import random

# ------------------ USER CLASSES ------------------

class User:
    def __init__(self, user_id, name, location):
        self.user_id = user_id
        self.name = name
        self.location = location


class Rider(User):
    def request_ride(self, ride_manager, destination):
        return ride_manager.create_ride(self, destination)


class Driver(User):
    def __init__(self, user_id, name, location):
        super().__init__(user_id, name, location)
        self.available = True
        self.rating = 5.0

    def accept_ride(self):
        self.available = False

    def complete_ride(self):
        self.available = True


# ------------------ RIDE CLASS ------------------

class Ride:
    def __init__(self, ride_id, rider, driver, distance):
        self.ride_id = ride_id
        self.rider = rider
        self.driver = driver
        self.distance = distance
        self.status = "Requested"
        self.fare = 0

    def complete(self):
        self.status = "Completed"
        self.driver.complete_ride()


# ------------------ PAYMENT STRATEGY ------------------

class PaymentStrategy(ABC):
    @abstractmethod
    def calculate_fare(self, distance):
        pass


class StandardPricing(PaymentStrategy):
    def calculate_fare(self, distance):
        return distance * 10


class SurgePricing(PaymentStrategy):
    def calculate_fare(self, distance):
        return distance * 20


# ------------------ DRIVER MANAGER ------------------

class DriverManager:
    def __init__(self):
        self.drivers = []

    def add_driver(self, driver):
        self.drivers.append(driver)

    def get_available_driver(self):
        for driver in self.drivers:
            if driver.available:
                return driver
        return None

    def show_drivers(self):
        for d in self.drivers:
            status = "Available" if d.available else "Busy"
            print(f"{d.name} | {status} | Rating: {d.rating}")


# ------------------ RIDE MANAGER ------------------

class RideManager:
    def __init__(self, driver_manager):
        self.driver_manager = driver_manager
        self.rides = []

    def create_ride(self, rider, destination):
        driver = self.driver_manager.get_available_driver()

        if not driver:
            print("❌ No drivers available right now.")
            return None

        driver.accept_ride()
        distance = random.randint(2, 15)

        # Surge logic
        if random.choice([True, False]):
            pricing = SurgePricing()
            print("⚡ Surge pricing applied!")
        else:
            pricing = StandardPricing()

        fare = pricing.calculate_fare(distance)

        ride = Ride(random.randint(1000, 9999), rider, driver, distance)
        ride.status = "Ongoing"
        ride.fare = fare

        self.rides.append(ride)

        print(f"\n🚕 Ride Started!")
        print(f"Driver: {driver.name}")
        print(f"Distance: {distance} km")
        print(f"Fare: {fare}\n")

        return ride

    def complete_ride(self, ride):
        ride.complete()
        print(f"✅ Ride Completed. Total Fare: {ride.fare}")

    def show_ride_history(self):
        if not self.rides:
            print("No rides yet.")
            return

        for r in self.rides:
            print(f"RideID: {r.ride_id} | Rider: {r.rider.name} | Driver: {r.driver.name} | Status: {r.status} | Fare: {r.fare}")


# ------------------ CLI APP ------------------

def main():
    driver_manager = DriverManager()
    ride_manager = RideManager(driver_manager)

    # Preload drivers
    driver_manager.add_driver(Driver(1, "Rahim", "A"))
    driver_manager.add_driver(Driver(2, "Karim", "B"))
    driver_manager.add_driver(Driver(3, "Jamal", "C"))

    rider = Rider(101, "Arnob", "Home")

    current_ride = None

    while True:
        print("\n====== 🚕 Ride Sharing App ======")
        print("1. Request Ride")
        print("2. Complete Ride")
        print("3. Show Drivers")
        print("4. Ride History")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            if current_ride and current_ride.status != "Completed":
                print("⚠️ You already have an ongoing ride.")
                continue

            destination = input("Enter destination: ")
            current_ride = rider.request_ride(ride_manager, destination)

        elif choice == "2":
            if not current_ride:
                print("No ride to complete.")
            else:
                ride_manager.complete_ride(current_ride)

        elif choice == "3":
            driver_manager.show_drivers()

        elif choice == "4":
            ride_manager.show_ride_history()

        elif choice == "5":
            print("👋 Exiting...")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()
