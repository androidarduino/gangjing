import pos
import time

epoch = lambda: int(round(time.time() * 1000))

# robot movement design

# for every movement instruction, calculate the distance and smooth transit
# a movement instruction consists of multiple timelines, each timeline describes a single movement

#Postures:

'''
postures (22 basic poses):
pos.look_front, pos.look_up, pos.look_45, pos.look_down, pos.look_left, pos.look_right, pos.look_pos.left_45, pos.look_pos.right_45
pos.left_down, pos.left_left, pos.left_45, pos.left_front, pos.left_front_45, pos.left_45_45, pos.left_45_front
pos.right_down, pos.right_right, pos.right_45, pos.right_front, pos.right_front_45, pos.right_45_45, pos.right_45_front
'''

# example posture:

pos.look_up = {
	head2: 90 # servo head2 turns to 90 degree
}

# actions (use 22 basic poses to construct actions):

LookRight = {
	'0-0.5': [pos.look_left, pos.left_up, pos.right_down] # in 0 - 0.5 seconds, make the postures listed
}

ShakeDance = {
	'0-0.5': [pos.look_left, pos.left_up, pos.right_down],
	'0.5-1': [pos.look_right, pos.left_down, pos.right_up],
	'1-1.5': [pos.look_left, pos.left_up, pos.right_down],
	'1.5-2': [pos.look_right, pos.left_down, pos.right_up],
	'2-2.5': [pos.look_front, pos.left_down, pos.right_down]
}

# matching it to a voice:

voice1 = { 'file': 'voice1.mp3', 'start': 0, 'end': 3.74 } # defines a voice segment

VoiceAction = { 'action': ShakeDance, 'voice': voice1, 'lenByVoice': True, 'lastExecuted': 0, 'commenced': 0 } # it will automatically adapt the timespan to the length of voice1.mp3

actionQueue = []
#TODO: 
# 1. figure out how to play sound segment in a large file
# 2. figure out how to do action steps
# 3. practice moving servos in ranges, make a servo range function mapping
# 4. connect hardware circuit

def takeStep(action):
	# calculate the action length based on all sub actions and the voice length
	actionLength = getActionLenth(action['action'])
	voice = action['voice']
	lengthFactor = 1
	voiceLength = voice['end'] - voice['start']
	if action['lenByVoice']:
		lengthFactor = voiceLength / totalLength(action['action'])
#TODO: according to whether  'lenByVoice' is set, calculate the factor for steps
	pos = action['lastExecuted']
	if pos != 0:
		#set the positions of motors
		currentPos = getCurrentPositions()
		#calculate step legnth
		steps = calculateSteps(action['initpos'], action['action']) * lengthFactor
		timeElapsed = epoch() - action['commenced']
		finishedCount = 0
		for timespan, postures in action['action']:
			#apply step to currentPos
			#update lastExecuted
			s, e = timespan.split('-')
			s, e = float(s), float(e)
			if timeElapsed - s > 0 and timespan < e - s:
				for p in postures:
					currentPos[p] += steps[p] * timeElapsed * lengthFactor
			else:
				finishedCount += 1
			if finishedCount == len(postures):
				return False
		action['lastExecuted'] = epoch()
	else:
		action['commenced'] = epoch()
		action['initPos'] = getCurrentPositions()
	return True

def doAction(action):
	actionQueue = []
	actionQueue.append(action)

def queueAction(action):
	actionQueue.append(action)

def loop():
	if actionQueue == []:
		return
	current = actionQueue[0]
	if (not takeStep(current)): # takeStep return false to indicate the action is finished 
		actionQueue = actionQueue(1:)
