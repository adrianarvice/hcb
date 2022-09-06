import time
from flask_socketio import emit



def start_all():
    print("WORKING")
    for c in range(20):
        print(c)
        emit('polyphonic_decryption_analyzer', c)
        time.sleep(5)
