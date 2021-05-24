import csv

all_flights = {}
all_routes = []

def merge_sort(lst, ascending = True):
    if len(lst) > 1:
        mid = len(lst)//2
        left = lst[:mid]
        right = lst[mid:]
        merge_sort(left)
        merge_sort(right)
        x = y = z = 0
        while x < len(left) and y < len(right):
            if left[x] < right[y]:
                lst[z] = left[x]
                x += 1
            else:
                lst[z] = right[y]
                y += 1
            z += 1
        while x < len(left):
            lst[z] = left[x]
            x += 1
            z += 1
        while y < len(right):
            lst[z] = right[y]
            y += 1
            z += 1
    if ascending:
        pass
    else:
        lst = lst[::-1]
    return lst

def addNodes(G,nodes):
    for i in nodes:
        G[i]  = list()
    return G

def addEdges(G,edge_list):
    for i in edge_list:
        G[i[0]].append((i[1],i[2]))
    return G

#takes the flight name as a parameter and reads the corresponding csv file and adds it to the data structure
def data_structure(file_name):
    f = open('flights/' + file_name + '.csv', 'rt')
    plane = csv.reader(f)
    iteration = 0
    node_list = []
    edge_list = []
    if file_name not in all_flights:
        all_flights[file_name] = []

    for i in plane:
        iteration2 = 0
        if iteration==0:
            for j in i:
                if j:
                    node_list.append(j)
        else:
            temp_org = ""
            for j in i:
                if j not in node_list:
                    if j != '0' and j != '-1':
                        j = j.strip('()')
                        list_j = j.split(", ")
                        edge_list.append((temp_org, node_list[iteration2 - 1], int(list_j[2])))
                        all_flights[file_name].append((temp_org, node_list[iteration2-1], list_j[0], list_j[1]))
                else:
                    temp_org = j
                iteration2 += 1

        iteration+=1
    G = {}
    addNodes(G, node_list)
    addEdges(G, edge_list)
    return G
#calling data_structure to append each dictionary to the all_routes list
all_routes.append(data_structure('A-220'))
all_routes.append(data_structure('A-350'))
all_routes.append(data_structure('B-737'))
all_routes.append(data_structure('B-747'))
all_routes.append(data_structure('B-777'))
#print(all_flights)
#print(all_routes)
#finding the fastest path between 2 locations
def dijkstra(G, start, end):
    shortest_distance = {}
    DaWay = {}
    track_DaWay = []
    unvisited = G
    for i in unvisited:
        shortest_distance[i] = 9999999
    shortest_distance[start] = 0
    while unvisited:
        min_dist = None
        for i in unvisited:
            if not min_dist:
                min_dist = i
            elif shortest_distance[i] < shortest_distance[min_dist]:
                min_dist = i
        further_path = G[min_dist]
        for x,y in further_path:
            if y+shortest_distance[min_dist] < shortest_distance[x]:
                shortest_distance[x] = y+shortest_distance[min_dist]
                DaWay[x] = min_dist
        unvisited.pop(min_dist)
    #right here
    currentNode = end
    while currentNode!=start:
        try:
            track_DaWay.insert(0,(DaWay[currentNode],currentNode))
            currentNode = DaWay[currentNode]
        except:
            break
    if shortest_distance[end]!=9999999:
        return shortest_distance[end],track_DaWay
#print(dijkstra(all_routes[4], "Karachi", "Lahore"))
#finds the quickest flight between 2 locations using dijkstra algoritm
def shortest_distance(G, start, end):
    shortest = []
    flights = {0: "A-350", 1: "A-220", 2: "B-737", 3: "B-747", 4: "B-777"}
    for i in range(5):
        route = dijkstra(all_routes[i], start, end)
        #print(route)
        if route:
            shortest.append((route, flights[i]))
    #print(shortest)
    shortest = merge_sort(shortest)
    return shortest[0]
#inteprets the quickest flight and outputs in the desired manner
def intptr_shortest_distance(G, start, end):
    x = shortest_distance(G, start, end)
    time = x[0][0]
    hour = time//60
    minute = time%(60*hour)
    time = "{} hour(s) and {} minute(s)".format(hour, minute)
    origin = x[0][1][0][0]
    dest = x[0][1][0][1]
    flight = x[1]
    print("The fastest flight from {} to {} is {} which takes {}".format(origin, dest, flight, time))
#prints the flight schedule for the day
def print_schedule(G, day):
    flights = []
    paths = []
    for key, item in G.items():
        for k in item:
            if k[3][1:-1] == day:
                flights.append(key)
                paths.append(k)
    if flights:
        string = "The following flights are available on {}\n".format(day)
        for i in range(len(paths)):
            string += "{}: From {} to {} at {}\n".format(flights[i], paths[i][0], paths[i][1], paths[i][2][1:-1])
    else:
        string = "No flights are available on {}\n".format(day)
    print(string[:-1])
#finds and prints the flight between two locations on a specific day
def flight_finder(G, start, end, day):
    flights = []
    for key, item in G.items():
        for k in item:
            if k[0] == start and k[1] == end and k[3][1:-1] == day:
                flights.append((key, k[2]))
    if flights:
        string = "The following flights are available from {} to {} on {}\n".format(start, end, day)
        for i in range(len(flights)):
            string += "{}: From at {}\n".format(flights[i][0], flights[i][1][1:-1])
    else:   
        string = "No flights are available from {} to {} on {}\n".format(start, end, day)
    print(string[:-1])
#prints the flight schedule between two locations
def flight_schedule(G, start, end):
    flights = []
    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for key, item in G.items():
        for k in item:
            if k[0] == start and k[1] == end:
                flights.append((key, k[2], k[3]))
    string = "The following flights are available from {} to {}\n".format(start, end)
    for day in week:
        string += "\n{}: ".format(day)
        for j in flights:
            if j[2][1:-1] == day:
                string += "{} at {} | ".format(j[0], j[1][1:-1])
    print(string)
#checks if a certain flight flies between 2 locations
def is_flight(G, flight, start, end):
    for key, item in G.items():
        if key == flight:
            for k in item:
                if k[0] == start and k[1] == end:
                    day, time = k[3][1:-1], k[2][1:-1]
    try:
        string = "The {} flies from {} to {} at {} on {}".format(flight, start, end, time, day)
    except:
        string = "The {} does not fly from {} to {}".format(flight, start, end)
    print(string)
#get_flight(all_flights, "B-747", "Islamabad", "Karachi")
#flight_schedule(all_flights, "Karachi", "Pindi")
#flight_finder(all_flights, "Islamabad", "Hyd", "Tuesday")
#print_flights(all_flights, "Tuesday")
#intptr_shortest_distance(all_routes, "Islamabad", "Karachi")

def main():
    cities = {1: "Karachi", 2: "Islamabad", 3: "Lahore", 4: "Quetta", 5: "Rawal-Pindi", 6: "Hyderabad"}
    week = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
    flights = {1: "A-350", 2: "A-220", 3: "B-737", 4: "B-747", 5: "B-777"}
    print("WELCOME TO THE ADA ")
    print("What would you like to do to:")
    print("1. Search \n2. Print Schedule")
    i = int(input())
    if i == 1:
        print("Please choose your origin: \n")
        for code, city in cities.items():
            print("{}. {}".format(code, city))
        origin = int(input())
        print("Please choose your destination: \n")
        for code, city in cities.items():
            if code == origin:
                pass
            else:
                print("{}. {}".format(code, city))
        dest = int(input())
        print("1. Search by quickest flight\n2. Search by day\n3. Search by flight\n4. Show all flights available")
        k = int(input())
        if k == 1:
            intptr_shortest_distance(all_flights, cities[origin], cities[dest])
        elif k == 2:
            print("Choose the day of the week: ")
            for code, day in week.items():
                print("{}. {}".format(code, day))
            day = int(input())
            flight_finder(all_flights, cities[origin], cities[dest], week[day])
        elif k == 3:
            print("Choose the flight: ")
            for code, flight in flights.items():
                print("{}. {}".format(code, flight))
            flight = int(input())
            is_flight(all_flights, flights[flight], cities[origin], cities[dest])
        elif k == 4:
            flight_schedule(all_flights, cities[origin], cities[dest])
    elif i == 2:
        print("Choose the day for which you would like to generate a schedule: ")
        for code, day in week.items():
            print("{}. {}".format(code, day))
        l = int(input())
        print_schedule(all_flights, week[l])
main()