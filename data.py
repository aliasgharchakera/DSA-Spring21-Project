import random
import csv
def create_time():
    hour = str(random.randint(0, 24))
    if len(hour) == 1:
        hour = "0" + hour
    minute = str(random.randrange(0, 60, 15))
    if len(minute) == 1:
        minute = "0" + minute
    return hour + ":" + minute
def create_day():
    week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return week[random.randint(0, 6)]
def time_taken():
    return random.randrange(60, 300, 15)
def main():
    return (create_time(), create_day(), time_taken())

def choice():
    lst = [-1, main()]
    return lst[random.randint(0, 1)]

#print(create_time())
#print(create_day())
print(main())
city = ["Karachi", "Islamabad", "Lahore", "Quetta", "Rawal-Pindi", "Hyderabad"]
flights = ["A-350", "A-220", "B-737", "B-747", "B-777"]
for i in range(len(flights)):
    name = 'flights/' + flights[i] + ".csv"
    with open(name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["", "Karachi", "Islamabad", "Lahore", "Quetta", "Rawal-Pindi", "Hyderabad"])
        for i in range(len(city)):
            row = [city[i], choice(), choice(), choice(), choice(), choice(), choice()]
            row[i + 1] = 0
            writer.writerow(row)
#name = 'c:/Users/alias/OneDrive - Habib University/Semester 2/DSA/Project/flights/time.csv'
#with open(name, 'w', newline='') as file:
#    writer = csv.writer(file)
#    writer.writerow(["", "Karachi", "Islamabad", "Lahore", "Quetta", "Rawal-Pindi", "Hyderabad"])
#    for i in range(len(city)):
#        row = [city[i], time_taken(), time_taken(), time_taken(), time_taken(), time_taken(), time_taken()]
#        row[i + 1] = 0
#        writer.writerow(row)