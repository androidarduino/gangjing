import action
import websocket

def on_message(ws, message):
    # here update the light strings
    global l
    print(message)
    # split message
	''' message example
		do:团体操:不要不要，人家不要不要
	'''
    (verb, action, voice) = message.split(":")
    if (receiver != "Robot"):
      return
    ''' Verbs: do, ready, startA, startB
    '''
    if (verb == "do"):
	  action.executeAction(action, voice)
    if (verb == "ready"):
      action.getReady()
    if (verb == "startA"):
      action.startContestA()
    if (verb == "startB"):
      action.startContestB()

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print "Connected to hub"

if __name__ == "__main__":
    websocket.enableTrace(True)
    global ws
    ws = websocket.WebSocketApp("ws://ec2-3-95-158-76.compute-1.amazonaws.com:8000",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

