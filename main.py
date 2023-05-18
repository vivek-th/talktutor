import speech_recognition as sr
def main():
    #this is main

    from tkinter import *

    top = Tk()

    top.geometry("200x100")

    b = Button(top, text="Simple bold")

    b.pack()

    top.mainaloop()
#this is end
    print("hello world")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)

        print("Please say something")

        audio = r.listen(source)

        print("Recognizing Now .... ")

        # recognize speech using google

        try:
            text = r.recognize_google(audio)
            print("You said: {}".format(text))
            from gingerit.gingerit import GingerIt

            parser = GingerIt()
            ct = parser.parse(text)
            print("the corrected text is:", ct["result"])
            print("you can speak again \n ")


        except Exception as e:
            print("Error :  " + str(e))

        # write audio
        with open("recorded.wav", "wb") as f:
            f.write(audio.get_wav_data())

if __name__ == "__main__":
    main()

    # from gingerit.gingerit import GingerIt
    # i
    # parser = GingerIt()
    # ct=parser.parse(text)
    # print ("the corrected text is:", ct["result"])



#this is the next part



