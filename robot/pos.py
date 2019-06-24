# -*- coding: utf-8 -*-

# poses
look_front, look_up, look_45, look_down, look_left, look_right, look_left_45, look_right_45 = 101, 102, 103, 104, 105, 106, 107, 108
left_down, left_up, left_45, left_front, left_up_45, left_45_45, left_45_front = 201, 202, 203, 204, 205, 206, 207
right_down, right_up, right_45, right_front, right_up_45, right_45_45, right_45_front = 301, 302, 303, 304, 305, 306, 307
#servos' alias
'''
head1: nod servo, head2: head turn servo
left1: left shoulder rotate servo, left2: left shoulder up servo
right1: right shoulder rotate servo, right2: right shoulder up servo
'''
head1, head2, left1, left2, right1, right2 = 0, 1, 2, 3, 4, 5
# all values are percentages

#sub postures
subpos = {
    look_front: { head1: 50, head2: 50 },
    look_up: { head1: 0, head2: 50},
    look_45: { head1: 25, head2: 50},
    look_down: { head1: 100, head2: 50 },
    look_left: { head1: 50, head2: 100 },
    look_right: { head1: 50, head2: 0 },
    look_left_45: { head1: 25, head2: 100 },
    look_right_45: { head1: 25, head2: 0 },

    left_down: { left1: 0,  left2: 0 },
    left_up: { left1: 100, left2: 0 },
    left_45: { left1: 50, left2: 0 },
    left_front: { left1: 0, left2: 100 },
    left_up_45: { left1: 50, left2: 100 },
    left_45_45: { left1: 50, left2: 50 },
    left_45_front: { left1: 50, left2: 100 },

    right_down: { right1: 0, right2: 0 },
    right_up: { right1: 100, right2: 0 },
    right_45: { right1: 50, right2: 0 },
    right_front: { right1: 0, right2: 100 },
    right_up_45: { right1: 50, right2: 100 },
    right_45_45: { right1: 50, right2: 50 },
    right_45_front: { right1: 50, right2: 100 }
}

#key frames
keyframes = {
    "站立": [look_front, left_down, right_down],
    "张开双臂": [look_front, left_up, right_up],
    "指左看左": [look_left, left_up, right_down],
    "指右看右": [look_right, left_down, right_up],
    "四十五度仰望": [look_left_45, left_up, right_front],
    "僵尸": [left_front, right_front],
    "平举双臂": [left_up, right_up],
    "左手前指低头": [left_front, look_down],
    "skr": [left_front, right_up, look_down],
    "左直角": [left_up, right_front],
    "右直角": [right_up, left_front]
}

#animations
animations = {
    "团体操": {
        # each item could be either an array of pos, or a keyframe, program will altomatically inteprete keyframes into array of poses
        1: "站立",
        2: [left_up],
        3: [right_up],
        4: [left_front],
        5: [right_front],
        6: "站立"
    },
    "摇头": {
        1: [look_left],
        2: [look_right],
        3: [look_left],
        4: [look_right],
        5: [look_left],
        6: [look_right]
    },
    "点头": {
        1: [look_front],
        2: [look_down],
        3: [look_front],
        4: [look_down],
        5: [look_front],
        6: [look_down]
    },
    "念诗": {
        1: "站立",
        2: [left_front],
        3: [left_up],
        4: [left_down],
        5: [right_front],
        6: [right_up],
        7: [right_down],
        8: [left_front],
        9: [left_up],
        10: [left_down],
        11: [right_front],
        12: [right_up],
        13: [right_down],
        14: "站立"
    },
    "在座的各位都是垃圾": {
    },
    "小拳拳锤你胸口": {
    },
    "欢呼雀跃": {
    }
}
