import azure.cognitiveservices.speech as speechsdk # to do the speech to text
import serial # to talk to arduino
import time # to wait between lines
import re # regular expressions (to parse out words from the text)

# import my Azure Speech keys from another file
from azkeys import speech_key, service_region


def speechListener():
    # =========================================================================
    # Arduino setup
    # =========================================================================

    # TODO: make this an arguement to parse instead of hardcoded port
    serialLink = serial.Serial('/dev/tty.usbmodem14401', 9600, timeout=0.25)

    # initialize LED to off
    ledCode = 'X'

    # initialize LCD text
    toLCD = ""

    # initialize Button state
    buttonState = False

    keywords = {}
    threshold = 50

    # =========================================================================
    # Azure setup
    # =========================================================================

    # setup my credentials for speech config
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # initialize speech recognition using those credentials
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    # create a function for event callback
    def processResponse(evt):
        nonlocal buttonState
        nonlocal ledCode
        nonlocal toLCD
        nonlocal keywords
        nonlocal threshold

        if(evt.result.text != ""):
            print(evt.result.text)
            # make an array of the words in the response
            words = re.findall(r'\w+',evt.result.text.lower())
            if(buttonState == True):
                for eachword in words:
                    if (eachword in keywords):
                        keywords[eachword] = keywords[eachword]+10
                    else:
                        keywords[eachword] = 10
                ledCode = 'G'
                toLCD = evt.result.text
            else:
                print("words heard")
                score = 0
                print(words)
                for eachword in words:
                    print(eachword)
                    if (eachword in keywords):
                        keywords[eachword] = keywords[eachword] - 1
                    else:
                        keywords[eachword] = 0
                    print(score)
                    score = score + keywords[eachword]
                print("total score: ")
                print(score)
                if(score > threshold):
                    print("keywords found")
                    ledCode = 'R'
                    toLCD = evt.result.text
                else:
                    toLCD = " "
                    ledCode = 'X'

        else:
            toLCD = " "
            ledCode = 'X'
    
    # Link the callback function that processes text results with the event
    speech_recognizer.recognized.connect(processResponse)

    # start listening
    speech_recognizer.start_continuous_recognition_async()

    # =========================================================================
    # Main loop
    # =========================================================================
    try:
        print("Press CTRL-C to stop")

        while(True):
            # read button state from arduino
            linein = serialLink.readline()
            if(linein == b'0\r\n'):
                print("Button Off")
                buttonState = False
            elif(linein == b'1\r\n'):
                print("Button On")
                buttonState = True
            elif(linein != b''):
                print(linein)
            if(toLCD != ""):
                print("toLCD: "+toLCD)
                serialLink.write(str.encode(toLCD.ljust(64)[:16]+ledCode))
                toLCD = toLCD[16:]


    except KeyboardInterrupt:
        print("keyboard interupt")
        speech_recognizer.stop_continuous_recognition_async()
        print("stopped session")
        print(keywords)

if __name__ == "__main__":
    speechListener()


