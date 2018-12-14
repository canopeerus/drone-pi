import requests,json
class drone:
    max_speed = 0
    min_alt = 0
    max_angle_attack = 0
    max_rate_ascend = 0
    max_distance_home = 0
    low_battery_level = 0
    tot_time_flight = 0
    drone_category = 0

    def __init__(self,listdata):
        self.max_speed = listdata[0]
        self.min_alt = listdata[1]
        self.max_angle_attack = listdata[2]
        self.max_rate_ascend = listdata[3]
        self.max_distance_home = listdata[4]
        self.low_batttery_level = listdata[5]
        self.tot_time_flight = listdata[6]
        self.drone_category = listdata[7]

    def show_props(self):
        print(self.max_speed,end="\t")
        print(self.min_alt,end="\t")
        print(self.max_angle_attack,end="\t")
        print(self.max_rate_ascend,end="\t")
        print(self.max_distance_home,end="\t")
        print(self.low_batttery_level,end="\t")
        print(self.tot_time_flight,end="\t")
        print(self.drone_category)


def main():
    r = requests.get("http://localhost:5000/dump")
    json_op = r.json()
    drone_list = []
    for x in json_op:
        drone_instance = drone(x)
        drone_list.append(drone_instance)
    for x in drone_list:
        x.show_props()

if __name__ == "__main__":
    main()
