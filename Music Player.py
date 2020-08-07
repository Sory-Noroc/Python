# MP3 Player made by Sory

import vlc
from threading import Thread
from PyQt5 import QtCore, QtGui, QtWidgets
from tkinter import Tk
from time import sleep
from pygame import mixer


class UiMainWindow:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)
        mixer.init()  # For the volume
        # Initiating the music player
        self.init_ui()
        self.init_widgets()
        self.init_music()

    def init_music(self):
        self.vlc_instance = vlc.Instance()
        media = self.vlc_instance.media_new('')
        self.player = self.vlc_instance.media_player_new()
        self.player.set_media(media)

    def init_ui(self):
        self.main_window.setStyleSheet('background-color: gray')
        self.main_window.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self.main_window)

    def init_widgets(self):
        # Initiating the buttons and labels
        self.play_pause_button = QtWidgets.QPushButton(self.centralwidget)
        self.play_pause_button.setGeometry(QtCore.QRect(370, 50, 40, 24))
        self.play_pause_button.clicked.connect(self.play_pause_song)
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setGeometry(QtCore.QRect(260, 50, 40, 24))
        self.stop_button.clicked.connect(self.stop_song)
        self.add_new_song_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_new_song_button.setGeometry(QtCore.QRect(690, 50, 80, 24))
        self.add_new_song_button.clicked.connect(self.add_song)
        self.remove_song_button = QtWidgets.QPushButton(self.centralwidget)
        self.remove_song_button.setGeometry(QtCore.QRect(630, 50, 50, 24))
        self.remove_song_button.clicked.connect(self.remove_song)
        self.restart_button = QtWidgets.QPushButton(self.centralwidget)
        self.restart_button.setGeometry(QtCore.QRect(470, 50, 50, 24))
        self.restart_button.clicked.connect(self.restart_song)
        self.next_button = QtWidgets.QPushButton(self.centralwidget)
        self.next_button.setGeometry(QtCore.QRect(420, 50, 40, 24))
        self.next_button.clicked.connect(self.next_song)
        self.previous_button = QtWidgets.QPushButton(self.centralwidget)
        self.previous_button.setGeometry(QtCore.QRect(310, 50, 50, 24))
        self.previous_button.clicked.connect(self.previous_song)
        self.volume_slider = QtWidgets.QSlider(self.centralwidget)
        self.volume_slider.setMinimum(0)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(100)
        self.volume_slider.setGeometry(QtCore.QRect(20, 40, 160, 20))
        self.volume_slider.setOrientation(QtCore.Qt.Horizontal)
        self.volume_slider.valueChanged.connect(self.volume)
        self.checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkbox.stateChanged.connect(self.auto_play)
        self.checkbox.setGeometry(QtCore.QRect(540, 54, 70, 20))
        # Initiating the fonts for the labels
        font_7 = QtGui.QFont()
        font_7.setPointSize(7)
        font_12 = QtGui.QFont()
        font_12.setPointSize(12)
        # Initiating the labels
        self.player_label = QtWidgets.QLabel(self.centralwidget)
        self.player_label.setGeometry(QtCore.QRect(340, 16, 40, 20))
        self.player_label.setFont(font_12)
        self.volume_label = QtWidgets.QLabel(self.centralwidget)
        self.volume_label.setGeometry(QtCore.QRect(20, 20, 40, 20))
        self.volume_label.setFont(font_7)
        # Initiating the lists and music
        self.ui_song_list = QtWidgets.QListWidget(self.centralwidget)
        self.ui_song_list.setGeometry(QtCore.QRect(10, 90, 780, 480))
        self.ui_song_list.setEnabled(True)
        self.ui_song_list.setStyleSheet('background-color: lightblue;')
        self.saved_music()  # Adding all the previously saved music
        self.all_songs = self.ui_song_list.findItems('', QtCore.Qt.MatchContains)
        self.current_audio = ''
        self.checking_thread = None  # For the auto play
        self.ui_song_list.itemClicked.connect(self.play_song)
        self.retranslate_ui(self.main_window)
        QtCore.QMetaObject.connectSlotsByName(self.main_window)

    def saved_music(self):
        self.audio_paths = {}
        with open('audio files.txt', 'a+') as audio_f:
            audio_f.seek(0)  # go at the start of the file
            for audio in audio_f.readlines():
                audio_name_ = audio.split('/')[-1]  # the name with the extension
                audio_name = '.'.join(audio_name_.split('.')[:-1])  # taking the audio name from the full name
                self.audio_paths[audio_name] = audio[:-1]  # to avoid \n
                self.ui_song_list.addItem(audio_name)  # Adding the audio on the GUI

    def config_audio(self, audio=''):  # Changes the song of the player
        if not audio:
            media = self.vlc_instance.media_new(audio)
        else:
            media = self.vlc_instance.media_new(self.audio_paths[audio])
        self.player = self.vlc_instance.media_player_new()
        self.player.set_media(media)

    def play_song(self, song):  # This is called when a song is clicked
        self.current_audio = song.text()
        self.player.stop()
        self.config_audio(audio=self.current_audio)
        self.player.play()

    def play_pause_song(self):
        if self.player.is_playing():  # Pausing
            self.player.pause()
            self.play_pause_button.setText('Play')

        else:
            self.play_pause_button.setText('Pause')
            self.player.play()

    def stop_song(self):
        self.player.stop()
        self.play_pause_button.setText('Play')

    def previous_song(self):
        if self.current_audio:
            self.player.stop()
            if self.current_audio == self.all_songs[0].text():  # To start the last song if the first one is playing
                self.current_audio = self.all_songs[-1].text()
                self.config_audio(self.current_audio)
                self.ui_song_list.setCurrentItem(self.all_songs[-1])
            else:
                previous_audio = None
                for song in self.all_songs:
                    if song.text() == self.current_audio:
                        break
                    previous_audio = song.text()
                    self.ui_song_list.setCurrentItem(song)
                self.current_audio = previous_audio
        else:
            self.default_song()
        self.config_audio(audio=self.current_audio)
        self.player.play()

    def next_song(self):
        if self.current_audio:
            try:
                self.player.stop()
                count = 0
                for song in self.all_songs:
                    count += 1
                    if song.text() == self.current_audio:
                        self.current_audio = self.all_songs[count].text()
                        self.ui_song_list.setCurrentItem(self.all_songs[count])
                        break  # To prevent the loop from going after finishing it's purpose

            except IndexError:  # Will raise when the last song is skipped
                self.default_song()
        else:
            self.default_song()
        self.config_audio(audio=self.current_audio)
        self.player.play()

    def restart_song(self):
        self.stop_song()
        self.player.play()

    def remove_song(self):
        self.player.stop()
        for song in self.all_songs:
            if song.text() == self.current_audio:
                with open('audio files.txt', 'a+') as audio_f:
                    audio_f.seek(0)
                    list_of_paths = audio_f.readlines()
                    audio_f.truncate(0)
                    for path in list_of_paths:  # Scanning the music paths
                        if song.text() in path:
                            continue  # Will rewrite the file, ignoring the removed one
                        audio_f.write(path)
                self.all_songs.remove(song)
                self.ui_song_list.takeItem(self.ui_song_list.currentRow())  # Removing from the visual list
                break

    def add_song(self):
        try:
            Tk().withdraw()  # Creating the interface for choosing songs
            list_of_chosen_audio = tkinter.filedialog.askopenfilenames(title='Choose audio files')
            with open('audio files.txt', 'a+') as audio_f:
                audio_f.seek(0)
                for audio_path in list_of_chosen_audio:
                    if audio_path.endswith('mp3') or audio_path.endswith('wav'):
                        if audio_path not in audio_f.read():  # checking for duplicates
                            audio_f.write(f'{audio_path}\n')
                            audio_name_ = audio_path.split('/')[-1]  # the name with the format
                            audio_name = '.'.join(audio_name_.split('.')[:-1])  # taking just the audio name without mp3
                            self.audio_paths[audio_name] = audio_path
                            self.ui_song_list.addItem(audio_name)
                self.all_songs = self.ui_song_list.findItems('', QtCore.Qt.MatchContains)
        except:  # An undefined encoding exception
            print(f"Couldn't add song at location {audio_path}")

    def volume(self, _=None):  # _ is an unused argument that is passed
        self.player.audio_set_volume(self.volume_slider.value())

    def auto_play(self):  # This is called when the checkbox is checked
        if self.checkbox.isChecked():
            self.auto_next = True
            if not self.checking_thread:  # To avoid playing multiple songs at once when spamming next/previous button
                self.checking_thread = Thread(target=self.check_playing)
            self.checking_thread.start()
        else:
            self.auto_next = False

    def check_playing(self):  # A thread that will play the next song when the current one is done
        while self.auto_next:
            if self.player.is_playing():
                sleep(1)
            else:
                self.next_song()
                sleep(2)
                self.check_playing()

    def default_song(self):
        try:  # Can raise an exception if no music was added
            self.current_audio = self.all_songs[0].text()
            self.ui_song_list.setCurrentItem(self.all_songs[0])
        except IndexError:
            pass  # Do nothing if buttons are clicked, but there are no songs

    def retranslate_ui(self, main_window):  # Setting the text for all the buttons and labels
        self.main_window.setCentralWidget(self.centralwidget)
        main_window.setWindowTitle("MP3 Player")
        self.play_pause_button.setText("Play")
        self.stop_button.setText("Stop")
        self.add_new_song_button.setText("Add New Song")
        self.remove_song_button.setText("Remove")
        self.restart_button.setText("Restart")
        self.next_button.setText("Next")
        self.previous_button.setText("Previous")
        self.checkbox.setText("Auto-Play")
        self.player_label.setText("MP3 Player")
        self.volume_label.setText("Volume")
        self.player_label.adjustSize()
        self.volume_label.adjustSize()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
