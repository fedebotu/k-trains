from SRT import SRT
from notify import notify
import time as python_time


ID = "010-3042-3555"
PW = "Giuggiolo22!"

srt = SRT(ID, PW)
srt.login()

dep = '수서'
arr = '대전'
date = '20221222'
time = '1600000'
trains = srt.search_train(dep, arr, date, time, time_limit='020000', available_only=False)


sender = 'berto.federico2@gmail.com'  # insert sender address here
receivers = [
                'fberto@kaist.ac.kr',
                'berto.federico2@hotmail.com'
                ]  # insert receiver addresses here
# sends email if upcoming conference exists
password = "vkvclddpjravaasd"


# Main loop
print("Starting main loop")
# print formatted time in KST
print("Current time at start: " + python_time.strftime("%Y-%m-%d %H:%M:%S", python_time.localtime()))
previous_state = False
while True:
    trains = srt.search_train(dep, arr, date, time, time_limit='180000', available_only=False)
    print(trains)
    # if any train has seats available, get its index
    
    if any(train.general_seat_available() for train in trains):
        # Get first train with seats available
        train = next(train for train in trains if train.general_seat_available())
        if not previous_state:
            message = f"Train\n{str(train)}\nhas seats now!"
            message += f"\nCurrent time: {python_time.strftime('%Y-%m-%d %H:%M:%S', python_time.localtime())}"
            notify(sender, receivers, message, password)
            print(message)
            previous_state = True
        # break
    else:
        if previous_state:
            message = f"Train\n{str(train)}\nhas no seats now!"
            message += f"\nCurrent time: {python_time.strftime('%Y-%m-%d %H:%M:%S', python_time.localtime())}"
            notify(sender, receivers, message, password)
            print(message)
            previous_state = False
    python_time.sleep(30)
