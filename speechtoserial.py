import azure.cognitiveservices.speech as speechsdk # to do the speech to text
import serial # to talk to arduino
import time # to wait between lines
import re # regular expressions (to parse out words from the text)
serialLink = serial.Serial('/dev/tty.usbmodem14401', 9600)

# import my Azure Speech keys from another file
from azkeys import speech_key, service_region

def speechListener():
    # setup my credentials for speech config
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # initialize speech recognition using those credentials
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    # initialize LED to off
    ledCode = 'X'

    while(True):
        # TODO: switch to ascync continuous 
        # listen for text, wait for silence or timeout (15sec), and process response
        result = speech_recognizer.recognize_once()

        # if we get something back
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print(result.text) #print it out for debugging

            # pull out words from text (take out whitespace and punctuation)
            words = re.findall('\w+',result.text.lower())

            print(words)  #print it out for debugging
            
            # look for keywords to set LED color
            if("matt" in words):
                ledCode = 'G'
            elif ("mat" in words):
                ledCode = 'G'
            elif ("yo" in words):
                ledCode = 'G'
            elif ("hey" in words):
                ledCode = 'G'
            elif ("hi" in words):
                ledCode = 'G'
            elif ("hello" in words):
                ledCode = 'G'
            elif ("green" in words):
                ledCode = 'G'
            elif ("danger" in words):
                ledCode = 'R'
            elif ("bad" in words):
                ledCode = 'R'
            elif ("look out" in words):
                ledCode = 'R'
            elif ("red" in words):
                ledCode = 'R'
            elif ("blue" in words):
                ledCode = 'B'
            elif ("chill" in words):
                ledCode = 'B'
            elif ("white" in words):
                ledCode = 'W'
            elif ("light" in words):
                ledCode = 'W'
            elif ("awesome" in words):
                ledCode = 'W'
            elif ("great" in words):
                ledCode = 'W'
            elif ("sweet" in words):
                ledCode = 'W'
            else: 
                ledCode = 'X'
            
            # send out results to arduino
            serialLink.write(str.encode(result.text.ljust(64)[:16]+ledCode))
            time.sleep(0.75)
            serialLink.write(str.encode(result.text.ljust(64)[16:32]+ledCode))
            time.sleep(0.75)
            serialLink.write(str.encode(result.text.ljust(64)[32:48]+ledCode))
            time.sleep(0.75)
            serialLink.write(str.encode(result.text.ljust(64)[48:64]+ledCode))

if __name__ == "__main__":
    speechListener()


