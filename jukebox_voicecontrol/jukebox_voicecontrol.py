#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import speech_recognition as sr
from pygame import mixer
import os
import time
import random
import threading


# add microphone names for other devices here, top microphone at the end
mic_names = ['Built-in Microphone', 'Mikrofonarray (Realtek High Def', 'USB PnP Sound Device: Audio (hw:1,0)']
#           #    Julian Laptop    #          Patrick Laptop          #       mini-usb-microphone (RPi)       #

# expand speech_recognition.Microphone class
class Microphone(sr.Microphone):

    # init with microphone names (strings) in a list as parameters (top microphone at list end)
    def __init__(self, mic_names):

        for mic_index, mic_name in enumerate(self.list_microphone_names()):  # get right microphone-device
            for mic_name_searched in mic_names:                              #
                if mic_name == mic_name_searched:                            #
                    self.device_index = mic_index                            #
                    self.name = mic_name                                     #

        assert self.name is not None, 'no microphone with one of the given names found'  # check if at least one of given microphones was found
        super().__init__(self.device_index)  # init super-class with determined microphone-device-index

    # simple __str__ to return selected microphone-name
    def __str__(self):
        return self.name

    # returns string with all available an the selected micropohne-device -> print out for debugging
    def str_selected_mic_list(self):
        str_selected_mic_list = ''
        for mic_index, mic_name in enumerate(self.list_microphone_names()):
            if mic_index == self.device_index:
                str_selected_mic_list += '-> '
            else:
                str_selected_mic_list += '   '
            str_selected_mic_list += str(mic_index) + ' ' + mic_name + '\n'

        return str_selected_mic_list


# WIP: controls all audio-outputs and LEDs (LED stuff will be added later) -> only use one class-object to control Audio/LEDs
class Audio_LED_Controller():
    def __init__(self):

        # playback parameters ###################################################################################################################################
        self.volume = 0.15   # music-playback volume (0.0 - 1.0) -> runtime: only change volume via function set_volume()
        self.listening_music_volume = 0.01  # music-playback volume (0.0 - 1.0) for music playback while speech_recognition is listening (after keyword detected)
        self.listening_fade_time = 3  # time (seconds) to fade volume from music-volume to music-listening-volume
        self.listening_sound_volume = 0.2   # listening-soundeffect volume (0.0 - 1.0)
        #########################################################################################################################################################

        self.play_all_songs_active = False  # Variable which stores, if all-song-playback (thread) is active -> only for internal use

        mixer.init()

        self.available_songs = []   # list for all available songs (.wav) in audio_files/songs
        for file_name in os.listdir('audio_files/songs'):   # append all available songs (song-names, without .wav) to available_songs-list
            if file_name[-4:] == '.wav':
                self.available_songs.append(file_name[:-4])


    # plays all available songs in random order (opens new thread)
    def play_all_songs(self):
        self.player_thread = threading.Thread(target=self.player_play_all_songs)
        self.player_thread.start()  # start new thread to play songs


    # plays all available songs in random order, always runs in own thread, started by play_all_songs()
    def player_play_all_songs(self):
        assert len(self.available_songs) > 0, 'no song found'   # check if atleast one song is available

        mixer.music.stop()
        self.play_all_songs_active = True   # this variable is used to stop all-song-playback (+thread) with stop_playback()

        shuffled_song_order = sorted(self.available_songs, key=lambda x: random.random())   # creates new song-list with radomized order
        while(self.play_all_songs_active):  # checks if all-song-playback (+thread) should be stopped
            if(not mixer.music.get_busy()):  # checks if last song ended -> new song will be stated
                mixer.music.load('audio_files/songs/' + shuffled_song_order[0] + '.wav')    # play first song in random-order list
                mixer.music.set_volume(self.volume)                                         #
                mixer.music.play()                                                          #
                shuffled_song_order = shuffled_song_order[1:] + shuffled_song_order[:1]  # rotate list by one to start the next song next time


    #  play single song (name as parameter), all available song (-names) stored ins self.available_songs
    def play_single_song(self, song_name):
            assert any(song_name in available_song for available_song in self.available_songs), 'no song named ' + song_name + ' found'  # check if song is available

            self.stop_playback()                                         # play song
            mixer.music.load('audio_files/songs/' + song_name + '.wav')  #
            mixer.music.set_volume(self.volume)                          #
            mixer.music.play()                                           #


    # stop active playback -> always use this function, never mixer.music.stop() -> use this function to stop all-song-playback to stop thread
    def stop_playback(self):
        if self.player_thread.is_alive():       # end player_play_all_songs thread
            self.play_all_songs_active = False  #

        mixer.music.stop()  # stop active playback


    # puse active playback, playback can be resumed later with resume_playback()
    def pause_playback(self):
        mixer.music.pause()

    # resume paused playback
    def resume_playback(self):
        mixer.music.unpause()

    # WIP
    def listening(self):
        if(mixer.music.get_busy() and self.volume > self.listening_music_volume and self.listening_fade_time > 0):
            fade_start_time = time.clock()
            while(time.clock() - fade_start_time < self.listening_fade_time):
                mixer.music.set_volume(self.volume - ((time.clock() - fade_start_time) / self.listening_fade_time * (self.volume - self.listening_music_volume)))


    # WIP
    def listening_end(self):
        pass


    # set new volume (0.0 - 1.0) for playback, never use mixer.music.set_volume(), always use this function
    def set_volume(self, new_volume):
        assert new_volume >= 0.0 and new_volume <= 1.0, 'volume range: 0.0 - 1.0'
        self.volume = new_volume
        mixer.music.set_volume(new_volume)
        pass



# WIP
def Main():
    x = Audio_LED_Controller()
    exit()
    recognizer = sr.Recognizer()
    with Microphone(mic_names) as microphone:   # getting right microphone for all audio inputs

        print('Microphone selection:')
        print(microphone.str_selected_mic_list() + '\n')
        while True:
            print('start: adjust for ambient noise before hotword detection')
            recognizer.adjust_for_ambient_noise(microphone)
            print('waiting for hotword...')
            if os.name == 'nt':  # windows
                input('hotword:')       # because snowboy is not available for windows
            elif os.name == 'posix':  # mac/linux
                input('hotword:')       # snowboy hotword detection instead of input() here

            print('hotword detected')
                                        # if audio is played stop it and adjust for ambient noice again
                                        # audio: listening
            print('listening ...')
            microphone_input = recognizer.listen(microphone)
            print('listen end, analysing audio')
                                        # audio: listen end



if __name__ == '__main__':
    Main()
