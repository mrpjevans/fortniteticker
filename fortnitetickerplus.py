'''
This is an example for how to use the Fortnite API and
Sense HAT using Python instead of Node-RED

This version allows you to get score for up to four different players
(or multiple platforms). Edit the users dictionary below to set up
each one. Then, when running, moving the joystick on the Sense HAT
will get that user's score. Depressing the joystick will get the
current server status.

You can customise this code to get other information from the API.
See https://fortniteapi.com for more details.

If using without a Sense HAT, you can enter directions instead of
the joystick.

Installation:
pip install requests

If on a Pi:
sudo apt install sense-hat
'''

import requests

isPi = True

try:
    from sense_hat import SenseHat
    sense = SenseHat()
except:
    isPi = False

# Maintain an internal list of User UIDs so we don't make extra calls
idCache = {}

# Four usernames/platforms, one for each joystick direction
users = {
    "up": {"username": "BlstEndedSkrewt", "platform": "pc"},
    "down": {"username": "BlstEndedSkrewt", "platform": "nintendo"},
    "left": {"username": "BlstEndedSkrewt", "platform": "pc"},
    "right": {"username": "BlstEndedSkrewt", "platform": "pc"}
}

# Gets the unique ID of a user
def getUserId(username):

    # If we've already looked it up once, don't bother again
    if username in idCache:
        uid = idCache[username]
    else:
        
        # Make the call
        fullUrl = "https://fortnite-public-api.theapinetwork.com/prod09/users/id?username=" + username
        response = requests.get(fullUrl)

        # Add to the cache
        uid = response.json()['uid']
        idCache[username] = uid

    return(uid)

# Return the user's current solo score
def getScore(username, platform):

    print('Getting stats for ' + username + ' on ' + platform)

    # Before we can look up stats for a user, we need their unique ID (uid)
    userId = getUserId(username)
    
    # Make the call - there's lots of data to look through
    # if you want it to do different things
    fullUrl = "https://fortnite-public-api.theapinetwork.com/prod09/users/public/br_stats?user_id=" + userId + "&platform=" + platform
    response = requests.get(fullUrl)
    return(response.json()['stats']['score_solo'])

# Check the current server status
def getServerStatus():

    print('Getting server status')
    fullUrl = "https://fortnite-public-api.theapinetwork.com/prod09/status/fortnite_server_status"
    response = requests.get(fullUrl)
    return(response.json()['status'])

# Main Loop
print('Running')

try:

    while True:

        user = None

        if isPi:
            event = sense.stick.wait_for_event()
            if event.direction != "middle" and event.action == 'pressed':
                sense.clear(0, 0, 0)
                user = users[event.direction]
            elif event.action == 'pressed':
                status = getServerStatus()
                print('Status: ' + status)
                if status == 'UP':
                    sense.clear(0, 255, 0)
                else:
                    sense.clear(255, 0, 0)
        else:
            direction = input("Choose a direction or fire (u/d/l/r/s): ")
            if direction == 'u':
                user = users['up']
            elif direction == 'd':
                user = users['down']
            elif direction == 'l':
                user = users['left']
            elif direction == 'r':
                user = users['right']
            elif direction == 's':
                status = getServerStatus()
                print('Status: ' + status)

        # Get a user's score and display
        if user is not None:
            score = getScore(user['username'], user['platform'])
            print(user['username'] + " on " + user['platform'] + ": " + str(score))
            if isPi:
                sense.show_message(user['username'] + " on " + user['platform'] + ": " + str(score))

except KeyboardInterrupt:
    sense.clear(0, 0, 0)
