from psychopy import visual, data, core
from psychopy.hardware import keyboard
import speech_recognition as sr
import json

kb = keyboard.Keyboard()

r = sr.Recognizer()
mic = sr.Microphone()

win = visual.Window([1920, 1080], fullscr=True, allowGUI=False, units="pix")
grating = visual.GratingStim(win, tex="sin", size = 200)
flash = visual.Circle(win, size = 500)
testing_text =  visual.TextBox2(win, text="Di algo y espera unos segundos", pos=(320, 300), letterHeight = 50)
listening_text =  visual.TextBox2(win, text="Escuchando...", pos=(320, 300), letterHeight = 50)
again =  visual.TextBox2(win, text="Otra vez?", pos=(320, 300), letterHeight = 50)
words = visual.TextBox2(win, text="?", pos=(300, 300), letterHeight = 50)


## Testing

testing_text.draw()
win.flip()

with mic as source:
    r.adjust_for_ambient_noise(source, duration=0.5)
    audio = r.listen(source, phrase_time_limit=5)

try:
    sentence = r.recognize_vosk(audio)
    sentence = json.loads(sentence)
    sentence_text = sentence['text']

except sr.UnknownValueError:
    print("Vosk could not understand audio")
except sr.RequestError as e:
    print("Vosk error; {0}".format(e))

words.text = sentence_text + "\nPulsa una tecla para continuar"
words.draw()
win.flip()

kb.waitKeys()

stimList = []
for contrast in [0.1, 0.5, 1.0]:
    stimList.append(
        {'contrast': contrast})

trials = data.TrialHandler(stimList, 10)

for thisTrial in trials:

    grating.contrast=thisTrial['contrast']

    for i in range(60):
        grating.draw()
        win.flip()

    win.flip()

    listening_text.draw()
    win.flip()

    response_done = False

    while not response_done:
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, phrase_time_limit=5)

        try:
            sentence = r.recognize_vosk(audio)
            sentence = json.loads(sentence)
            sentence_text = sentence['text']

        except sr.UnknownValueError:
            print("Vosk could not understand audio")
        except sr.RequestError as e:
            print("Vosk error; {0}".format(e))

        words.text = sentence_text + "?"
        words.draw()
        win.flip()

        keys = kb.waitKeys()
        for thisKey in keys:
            if thisKey == 'escape':
                core.quit()
            elif thisKey == 'space':
                response_done = True
            else:
                win.flip()
                again.draw()
                win.flip()

win.close()
core.quit()
