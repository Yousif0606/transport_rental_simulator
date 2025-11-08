"""
CMPUT 175 - Assignment 1
Author: Yousif Al-Anbaki
Collaborators: None
References:
CMPUT 175 course notes, assignment PDF,
Stack Overflow (syntax reminders),
AI assistant (logic clarification and syntax fixes)
"""

import random

# constants 
BIKE_RATE = 0.50
SCOOTER_RATE = 0.30
MIN_MINUTES = 1
MAX_MINUTES = 30


# load users.txt
def load_users():
    user_info = {}
    with open("users.txt", "r") as f:
        header = f.readline()
        for line in f:
            line = line.strip()
            if line != "": 
                parts = line.split(",")
                uid = parts[0].strip()
                credit = int(parts[1].strip())
                total_time = int(parts[2].strip())
                user_info[uid] = {"Available_Credit": credit, "Total_Travel_Time": total_time}
    return user_info


# load transportation.txt 
def load_transportation():
    bike = {}
    scooter = {}
    area_transportation = {}

    with open("transportation.txt", "r") as f:
        header = f.readline()
        for line in f:
            line = line.strip()
            if line != "": 
                parts = line.split(",")
                pid = parts[0].strip()
                typ = parts[1].strip()
                area = parts[2].strip()
                total_time = int(parts[3].strip())

                if typ.lower() == "bike":
                    bike[pid] = {"Type": "Bike", "Area": area, "Total_Travel_Time": total_time}
                else:
                    scooter[pid] = {"Type": "Scooter", "Area": area, "Total_Travel_Time": total_time}

                if area not in area_transportation:
                    area_transportation[area] = {"Bikes": set(), "Scooters": set()}

                if typ.lower() == "bike":
                    area_transportation[area]["Bikes"].add(pid)
                else:
                    area_transportation[area]["Scooters"].add(pid)

    return bike, scooter, area_transportation


# pick user (Y/N)
def get_user(user_info):
    ans = input("Are you an existing user? (Y/N): ").strip().upper()
    while ans not in ("Y", "N"):
        ans = input("Please enter Y or N: ").strip().upper()

    if ans == "Y":
        keys = list(user_info.keys())
        idx = random.randrange(len(keys))
        uid = keys[idx]
    else:
        unique = False
        uid = ""
        while not unique:
            candidate = "U" + str(random.randint(1, 100))
            if candidate not in user_info:
                uid = candidate
                unique = True
        credits = random.randint(50, 200)
        user_info[uid] = {"Available_Credit": credits, "Total_Travel_Time": 0}

    print("Welcome " + uid + ". You have $ " + str(user_info[uid]["Available_Credit"]) + " available credits in RideIT")
    return uid


# choose kind
def choose_kind():
    choice = input("Which transportation do you want to ride? 1. Scooter, 2. Bike: ").strip()
    while choice not in ("1", "2"):
        choice = input("Please enter 1 or 2: ").strip()
    if choice == "1":
        return "Scooter"
    else:
        return "Bike"


# show areas where chosen kind is available
def print_available_areas(area_transportation, kind):
    areas = []
    for area in area_transportation:
        if kind == "Bike" and len(area_transportation[area]["Bikes"]) > 0:
            areas.append(area)
        if kind == "Scooter" and len(area_transportation[area]["Scooters"]) > 0:
            areas.append(area)

    if len(areas) == 0:
        print("Our " + kind + " is currently unavailable.")
    else:
        print("Our " + kind + " is currently available in " + ", ".join(areas) + ".")


# pick start area that actually has that kind
def choose_start_area(area_transportation, kind):
    candidates = []
    for area in area_transportation:
        if kind == "Bike" and len(area_transportation[area]["Bikes"]) > 0:
            candidates.append(area)
        if kind == "Scooter" and len(area_transportation[area]["Scooters"]) > 0:
            candidates.append(area)
    if len(candidates) == 0:
        return ""
    idx = random.randrange(len(candidates))
    return candidates[idx]


# pick a product id in that start area
def choose_product(area_transportation, kind, area):
    if kind == "Bike":
        pool = list(area_transportation[area]["Bikes"])
    else:
        pool = list(area_transportation[area]["Scooters"])
    idx = random.randrange(len(pool))
    return pool[idx]


# pick destination different from start
def choose_destination(area_transportation, start):
    areas = list(area_transportation.keys())
    j = random.randrange(len(areas))
    while areas[j] == start:
        j = random.randrange(len(areas))
    return areas[j]


# compute price
def trip_price(kind, minutes):
    if kind == "Bike":
        rate = BIKE_RATE
    else:
        rate = SCOOTER_RATE
    return round(rate * minutes, 2)


# make sure user has enough credit; keep asking to add until enough
def ensure_credit(user_info, uid, cost):
    enough = user_info[uid]["Available_Credit"] >= cost
    while not enough:
        add_str = input("Insufficient credit. Enter amount to add: ").strip()
        add_val = int(add_str)
        user_info[uid]["Available_Credit"] = user_info[uid]["Available_Credit"] + add_val
        enough = user_info[uid]["Available_Credit"] >= cost
    print("Enjoy your riding!")
    user_info[uid]["Available_Credit"] = user_info[uid]["Available_Credit"] - cost


# update user + product + area sets
def apply_updates(user_info, bike, scooter, area_transportation,
                  uid, kind, pid, start, dest, minutes):
    user_info[uid]["Total_Travel_Time"] = user_info[uid]["Total_Travel_Time"] + minutes

    if kind == "Bike":
        store = bike
    else:
        store = scooter

    store[pid]["Area"] = dest
    store[pid]["Total_Travel_Time"] = store[pid]["Total_Travel_Time"] + minutes

    if dest not in area_transportation:
        area_transportation[dest] = {"Bikes": set(), "Scooters": set()}

    if kind == "Bike":
        area_transportation[start]["Bikes"].discard(pid)
        area_transportation[dest]["Bikes"].add(pid)
    else:
        area_transportation[start]["Scooters"].discard(pid)
        area_transportation[dest]["Scooters"].add(pid)


# append one trip to trips.txt
def append_trip(uid, pid, start, dest, minutes, cost):
    with open("trips.txt", "a") as f:
        f.write(uid + ", " + pid + ", " + start + ", " + dest + ", " + str(minutes) + ", " + f"{cost:.2f}" + "\n")


# write users_info.txt 
def write_users_info(user_info):
    with open("users_info.txt", "w") as f:
        f.write("user_ID, Available_Credit, Total_Travel_Time\n")
        for uid in user_info:
            line = uid + ", " + str(user_info[uid]["Available_Credit"]) + ", " + str(user_info[uid]["Total_Travel_Time"]) + "\n"
            f.write(line)


# write transportations_info.txt 
def write_transportations_info(bike, scooter):
    with open("transportations_info.txt", "w") as f:
        f.write("Product_ID, Type, Area, Total_Travel_Time\n")
        for pid in bike:
            data = bike[pid]
            f.write(pid + ", " + data["Type"] + ", " + data["Area"] + ", " + str(data["Total_Travel_Time"]) + "\n")
        for pid in scooter:
            data = scooter[pid]
            f.write(pid + ", " + data["Type"] + ", " + data["Area"] + ", " + str(data["Total_Travel_Time"]) + "\n")


# main
def main():
    user_info = load_users()
    bike, scooter, area_transportation = load_transportation()

    # run 3 trips
    for _ in range(3):
        uid = get_user(user_info)
        kind = choose_kind()
        print_available_areas(area_transportation, kind)

        start = choose_start_area(area_transportation, kind)
        if start == "":
            print("No " + kind + " available right now.")
            return

        pid = choose_product(area_transportation, kind, start)
        dest = choose_destination(area_transportation, start)
        minutes = random.randint(MIN_MINUTES, MAX_MINUTES)
        cost = trip_price(kind, minutes)

        print("You will ride " + pid + " from " + start + " to " + dest + " for " + str(minutes) + " minutes. It will cost $ " + f"{cost:.2f}" + ".")

        ensure_credit(user_info, uid, cost)
        apply_updates(user_info, bike, scooter, area_transportation, uid, kind, pid, start, dest, minutes)
        append_trip(uid, pid, start, dest, minutes, cost)

    write_users_info(user_info)
    write_transportations_info(bike, scooter)



main()
