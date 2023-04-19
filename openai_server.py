import pystray, time
from PIL import Image, ImageDraw
from threading import Thread, Event
import zmq, openai

class ExampleThread(Thread):
    def __init__(self):
        super().__init__()
        self._stop_event = Event()
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://127.0.0.1:5555")

    def prompt_ai(self, text, stop=None):
                openai.api_key = "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"
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=text,
                    temperature=0.5,
                    max_tokens=2000,
                    n=1,
                    stop=stop,
                )
                sanitized_response = response.choices[0].text.strip()
                return sanitized_response

    def run(self):
        while not self._stop_event.is_set():
            message = self.socket.recv_string()
            response = self.prompt_ai(message)
            print("Received request:", message)
            print(response)
            response = "Hello from server!"
            self.socket.send_string(response)
        print('closing')

    def stop(self):
        self._stop_event.set()
        self.socket.close()
        self.context.term()

def on_clicked(icon, query):
    if str(query) == "receiver":
        if len(threads) == 0:
            threads.append(ExampleThread())
            threads[0].start()
        elif len(threads) == 1:
            if threads[0].is_alive():
                pass
            else:
                threads.pop()
                threads.append(ExampleThread())
                threads[0].start()
        else:
            print('error')
    elif str(query) == "receiver stop":
        threads[0].stop()
        threads[0].join()
    elif str(query) == "Exit":
        icon.stop()

def create_image(width, height, color1, color2):
    # Generate an image and draw a pattern
    image = Image.new('RGB', (width, height), color1)
    dc = ImageDraw.Draw(image)
    dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
    dc.rectangle((0, height // 2, width // 2, height), fill=color2)
    return image

# image = Image.open("icon.png")
image = create_image(64, 64, 'black', 'white')
 
icon = pystray.Icon("Jenova", image, "JENOVA", menu=pystray.Menu(
    pystray.MenuItem("receiver", on_clicked),
    pystray.MenuItem("receiver stop", on_clicked),
    pystray.MenuItem("Exit", on_clicked)))

threads = [] 
icon.run()