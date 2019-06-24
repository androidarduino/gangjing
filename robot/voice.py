# -*- coding: utf-8 -*-
import pygame
import time

sounddata = '''1560032347.mp3
2.84 请这边的朋友发言
8.54 我宣布，这次比赛的冠军就是我亚麻杠精
13.52 你问我爱你有多深，月亮代表我的心
18.62 好漂亮的姑娘，我可以要你的微信吗？
24.97 这个小伙子很帅，但是比我还差了那么一点点
27.46 此处可以有掌声
31.13 你说的都对，但我就是不信
37.66 我不是针对谁，我是说，在座的各位都是垃圾
41.03 高叉泳衣，高叉泳衣
46.73 讨厌，在西雅图怎么可以问伦家的性别咧
52.60 讨厌讨厌，小拳拳锤你胸口，大坏蛋
55.8 不要不要，人家不要
63.86 床前明月光，疑是地上霜。举头望明月，低头思故乡
71.75 亚麻奇葩说，奇葩赛着说。一个刚说完，一个又来说'''

_voice = {}

# sound apis:
def init():
	#init sounds from mp3 files
	data = sounddata.splitlines()
	file_name = data[0]
	start = 0.0
	for i in data[1:]:
		[end, text] = i.split(' ')
		end = float(end)
		_voice[text] = [start, end]
		start = end
	pygame.mixer.init()
	pygame.mixer.music.load("mp3/" + file_name)

def play(text):
	#play a particular segment for text
	if text not in _voice:
		return
	[start, end] = _voice[text]
	pygame.mixer.music.play(-1, start)
	time.sleep(end-start)
	pygame.mixer.music.pause()

def len(text):
	#get length in seconds for a segment matching text
	if text not in _voice:
		return
	[start, end] = _voice[text]
	return (end-start)

def getAll():
	#return all available voices
	return _voice.keys()

def pause():
    pygame.mixer.music.pause()

init()
print _voice
play("讨厌讨厌，小拳拳锤你胸口，大坏蛋")
