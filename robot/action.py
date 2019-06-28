# -*- coding: utf-8 -*-
import pos
import voice
import time
import sys
import serial

epoch = lambda: int(round(time.time() * 1000))
actionReset = True
actionQueue = []
arduino = serial.Serial('/dev/cu.usbmodem1421', 9600, timeout=0.1)

def queueAction(animation, voice_name):
    factor = 1.0
    ani_len = max(pos.animations[animation].keys())
    if voice_name != '':
        factor = voice.len(voice_name) / ani_len
    action = {}
    #print factor
    for timestamp, arr in pos.animations[animation].items():
        # expand all key frames
        # adjust time points
        timestamp = timestamp * factor
        if type(arr) is str:
            arr = pos.keyframes[arr]
        action[timestamp] = arr
    action["voice"] = voice_name
    # queue it to actionQueue
    actionQueue.append(action)
    #print action

def executeAction(animation, voice_name):
    actionReset = True
    actionQueue = []
    queueAction(animation, voice_name)

current = {0:50, 1:50, 2:50, 3:50, 4:50, 5:50}

def doAction():
    if len(actionQueue) == 0:
        return
    start_time = epoch()
    # take the first item in the queue
    action = actionQueue.pop(0)
    actionReset = False
    # play audio
    voc = action["voice"]
    voc_len = 0.0
    del action["voice"]
    if voc != "":
        voice.play(voc)
        voc_len = voice.len(voc)
    # read the first segment array, read all servo expected values
    last_ts = 0
    for ts, arr in sorted(action.items()):
        span = ts - last_ts
        last_ts = ts
        while(True):
            # ** for each servo, get its current value
            expected = {}
            for sub_pos in arr:
                servo_poses = pos.subpos[sub_pos]
                for servo, percent in servo_poses.items():
                    expected[servo] = percent
            # compare and compute the step length of each servo, add it to servo
            interval = 0.1
            for servo in expected.keys():
                diff = expected[servo] - current.get(servo, 0.0)
                step = diff / span * interval
                #print diff, span, step
                current[servo] = current.get(servo, 0.0) + step
            # delay for a certain time
            time.sleep(interval)
            span -= interval
            #print current
            c =  current
            #command 3
            cmd = '3 ' + str(int(round(c[0]))) + ' ' + str(int(round(c[1]))) + ' ' + str(int(round(c[2]))) + ' ' + str(int(round(c[3]))) + ' ' + str(int(round(c[4]))) + ' ' + str(int(round(c[5]))) + "\n"
            print "writing command ", cmd
            arduino.write(cmd)
            # check whether time passed voice length, if so, pause audio
            time_now = epoch()
            if (time_now - start_time) > voc_len*1000:
                voice.pause()
            # check whether action queue is reset, if so, stop and return
            if actionReset:
                return
            # check whether the step time passed, if passed, go to next segment array
            if (span <= 0):
                break
            # if not passed, repeat ** step

def getReady():
    arduino.write(0)

def startContestA():
    arduino.write(1)

def startContest():
    arduino.write(2)
'''
'''
executeAction("念诗", "床前明月光，疑是地上霜。举头望明月，低头思故乡")
doAction()
executeAction("测试", "讨厌讨厌，小拳拳锤你胸口，大坏蛋")
doAction()
executeAction("摇头", "不要不要，人家不要")
doAction()
executeAction("点头", "这个小伙子很帅，但是比我还差了那么一点点")
doAction()
executeAction("团体操", "讨厌讨厌，小拳拳锤你胸口，大坏蛋")
doAction()
'''
