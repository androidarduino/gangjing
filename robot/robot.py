# -*- coding: utf-8 -*-
import pos
import voice
import time

epoch = lambda: int(round(time.time() * 1000))
actionReset = True

def queueAction(animation, voice_name):
    factor = 1.0
    if voice_name != '':
        factor = voice.len(voice_name)
    action = {}
    for timestamp, arr in animation:
        # expand all key frames
        # adjust time points
        if 
        timestamp = timestamp * factor
        if type(arr) == 'str':
            arr = keyframes[arr]
        action[timestamp] = arr
    action["voice"] = voice_name
    # queue it to actionQueue
    actionQueue.append(action)

def doAction(animation, voice_name):
    actionReset = True

def doAction():
    if len(actionQueue) == 0:
        return
    start_time = epoch
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
    for ts, arr in action:
        while(True):
            # ** for each servo, get its current value
            expected = {}
            for sub_pos in arr:
                servo_poses = pos.subpos[sub_pos]
                for servo, percent in servo_poses:
                    expected[servo] = percent
            # compare and compute the step length of each servo, add it to servo
            for servo in expected.keys():
                diff = expected[servo] - current[servo]
                step = diff / ts
                current[servo] = current[servo] + step
            # delay for a certain time
            time.sleep(0.05)
            ts -= 0.05
            # check whether time passed voice length, if so, pause audio
            if (epoch - start_time) > voc_len*1000:
                voice.pause()
            # check whether action queue is reset, if so, stop and return
            if actionReset:
                return
            # check whether the step time passed, if passed, go to next segment array
            if (ts <= 0):
                break
            # if not passed, repeat ** step
