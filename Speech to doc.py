import speech_recognition as sr
import sys, os, queue
import argparse
import sounddevice as sd
import soundfile as sf
from threading import Thread
from datetime import datetime
from tkinter import Tk, Label, Button, StringVar, messagebox, CENTER
import numpy as np # Not used, but needs to be installed for soundfile
assert np

class Gui:
	def __init__(self, mw):
		self.mw = mw

		mw.title('Speech to text') # GUI Title
		width, height = 500, 100
		x = (mw.winfo_screenwidth() // 2) - (width // 2)
		y = (mw.winfo_screenheight() // 2) - (height // 2)
		mw.geometry(f'500x75+{x}+{y}') # GUI sizing

		# Making and placing the widgets
		self.start_button = Button(mw, text="Start", command=self.start_rec)
		self.start_button.place(x=190, y=10)

		self.stop_button = Button(mw, text="Stop", command=self.stop_rec)
		self.stop_button.place(x=250, y=10)

		self.labeltext = StringVar()
		self.label = Label(mw, textvariable=self.labeltext, anchor=CENTER, width=30)
		self.label.place(x=125, y=40)
		self.labeltext.set("Press 'Start' to initiate the recording")

	def start_rec(self):
		self.labeltext.set('Started recording')
		self.recording = True # For the recording loop thread

		def int_or_str(text):  # Helper function for argument parsing
		    try:
		        return int(text)
		    except ValueError:
		        return text

		def callback(indata, frames, time, status):  # This is called for every audio segment
		    self.progression.put(indata.copy())

		parser = argparse.ArgumentParser(add_help=False)
		parser.add_argument(
		    '-l', '--list-devices', action='store_true',
		    help='show list of audio devices and exit')

		args, remaining = parser.parse_known_args()

		parser = argparse.ArgumentParser(
		    description=__doc__,
		    formatter_class=argparse.RawDescriptionHelpFormatter,
		    parents=[parser])
		parser.add_argument(
		    'filename', nargs='?', metavar='FILENAME',
		    help='audio file to store recording to')
		parser.add_argument(
		    '-d', '--device', type=int_or_str,
		    help='input device (numeric ID or substring)')
		parser.add_argument(
		    '-r', '--samplerate', type=int, help='sampling rate')
		parser.add_argument(
		    '-c', '--channels', type=int, default=1, help='number of input channels')
		parser.add_argument(
		    '-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
		args = parser.parse_args(remaining)

		self.progression = queue.Queue() # Store the recorded sound bytes

		if not args.samplerate:
			device_info = sd.query_devices(args.device, 'input')
			# soundfile expects an int, sounddevice provides a float:
			args.samplerate = int(device_info['default_samplerate'])
		if not args.filename:
			args.filename = 'temporary_file.wav'

		thread = Thread(target=self.record_and_recognize, args=(args, callback))
		thread.start()


	def stop_rec(self):

		self.labeltext.set('Stopped recording')
		self.recording = False

	def record_and_recognize(self, args, callback_func):
		self.labeltext.set('Recording...')

		with sf.SoundFile(args.filename, mode='w', samplerate=args.samplerate,
		                      channels=args.channels, subtype=args.subtype) as file:
			with sd.InputStream(samplerate=args.samplerate, device=args.device,
		                            channels=args.channels, callback=callback_func):
				# Thread loop that writes sound to file until stopped
				while self.recording:
					file.write(self.progression.get())

		# Starting the recognizing process
		recognizer = sr.Recognizer()
		file = open('temporary_file.wav', 'rb') # didn't use "with" cuz the AudioFile was closing too, check below
		speech = sr.AudioFile(file) # If this was within the "with" block if would raise I/O on closed file later

		speech_text = None  # to check if any word was understood

		try:
			with speech as source:
				recognizer.adjust_for_ambient_noise(source)  # To make it more accurate
				audio = recognizer.record(source)  # Preparing for recognizing

		except ValueError:
			self.labeltext.set('Error! Audio file empty!')

		else:
			self.labeltext.set('Recognizing...')
			try:
				speech_text = recognizer.recognize_sphinx(audio)  # Taking the words from audio
			except sr.UnknownValueError:
				self.labeltext.set('Can\'t Understand')

			if speech_text:  # If any word was captured
				with open('Doc after speech.txt', 'a') as doc:
					doc.write(f'{datetime.now()}\n{speech_text}\n\n')
				self.labeltext.set('Finished!')

			else:
				self.labeltext.set('Finished! But no word was written...')
		file.close()
		os.remove('temporary_file.wav')  # To avoid junk files

	def on_closing(self):  # To prevent infinite loop threads
		self.recording = False   # In case the GUI is closed while still recording
		ui.destroy()
		sys.exit(0)

if __name__ == "__main__":
	ui = Tk()
	window = Gui(ui)
	ui.protocol("WM_DELETE_WINDOW", window.on_closing)  # To avoid infinite loops in background
	ui.mainloop()
