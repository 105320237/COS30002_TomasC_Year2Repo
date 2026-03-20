#variables

passengers = 0
capacity = 20

states = ['Glenferrie','Burnley','Hawthorn', 'Richmond', 'East Richmond']
current_state = 'Glenferrie'


moving = True
#ammount of people waiting at each station
waiting = [5, 7, 1, 2, 8]
stations_passed = 0

while moving and stations_passed <= 5:
    stations_passed += 1

    if current_state == 'Glenferrie':
        print("Just arrived at Glenferrie Station")
        print (str(waiting[0]) + " passengers waiting to get on" + " and " + str(passengers) + " passengers on board. The capacity is " + str(capacity))

        seats_available = capacity - passengers
        if waiting[0] <= seats_available:
            passengers += waiting[0]
            print(str(waiting[0]) + " passengers got on the train")
            waiting[0] = 0
            print("Next station is Burnley")
            current_state = 'Burnley'
        else:
            print("Not enough seats for all passengers waiting at Glenferrie Station")
            print("Next station is Burnley")
            current_state = 'Burnley'
    
    elif current_state == 'Burnley':
        print("Just arrived at Burnley Station")
        print (str(waiting[1]) + " passengers waiting to get on" + " and " + str(passengers) + " passengers on board. The capacity is " + str(capacity))

        seats_available = capacity - passengers
        if waiting[1] <= seats_available:
            passengers += waiting[1]
            print(str(waiting[1]) + " passengers got on the train")
            waiting[1] = 0
            print("Next station is Hawthorn")
            current_state = 'Hawthorn'
        else:
            print("Not enough seats for all passengers waiting at Burnley Station")
            print("Next station is Hawthorn")
            current_state = 'Hawthorn'
    elif current_state == 'Hawthorn':
        print("Just arrived at Hawthorn Station")
        print (str(waiting[2]) + " passengers waiting to get on" + " and " + str(passengers) + " passengers on board. The capacity is " + str(capacity))

        seats_available = capacity - passengers
        if waiting[2] <= seats_available:
            passengers += waiting[2]
            print(str(waiting[2]) + " passengers got on the train")
            waiting[2] = 0
            print("Next station is Richmond")
            current_state = 'Richmond'
        else:
            print("Not enough seats for all passengers waiting at Hawthorn Station")
            print("Next station is Richmond")
            current_state = 'Richmond'
    elif current_state == 'Richmond':
        print("Just arrived at Richmond Station")
        print (str(waiting[3]) + " passengers waiting to get on" + " and " + str(passengers) + " passengers on board. The capacity is " + str(capacity))

        seats_available = capacity - passengers
        if waiting[3] <= seats_available:
            passengers += waiting[3]
            print(str(waiting[3]) + " passengers got on the train")
            waiting[3] = 0
            print("Next station is East Richmond")
            current_state = 'East Richmond'
        else:
            print("Not enough seats for all passengers waiting at Richmond Station")
            print("Next station is East Richmond")
            current_state = 'East Richmond'
    elif current_state == 'East Richmond':
        print("Just arrived at East Richmond Station")
        print (str(waiting[4]) + " passengers waiting to get on" + " and " + str(passengers) + " passengers on board. The capacity is " + str(capacity))

        seats_available = capacity - passengers
        if waiting[4] <= seats_available:
            passengers += waiting[4]
            print(str(waiting[4]) + " passengers got on the train")
            waiting[4] = 0
            print("The train is reaching the end of the track")
            moving = False
            print("Train crashed at the end of the track")
            print("The End")
        else:
            print("Not enough seats for all passengers waiting at East Richmond Station")
            print("The train is reaching the end of the track")
            moving = False
            print("Train crashed at the end of the track")
            print("The End")



