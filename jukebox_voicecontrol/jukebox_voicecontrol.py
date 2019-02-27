#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import speech_recognition as sr
import os

# add microphone names for other devices here, top microphone at the end
mic_names = ['Built-in Microphone', 'Mikrofonarray (Realtek High Def', 'USB PnP Sound Device: Audio (hw:1,0)']


# expand speech_recognition.Microphone class
class Microphone(sr.Microphone):

    def __init__(self, mic_names):

        for mic_index, mic_name in enumerate(self.list_microphone_names()):
            for mic_name_searched in mic_names:
                if mic_name == mic_name_searched:
                    self.device_index = mic_index
                    self.name = mic_name

        assert self.name is not None, 'no microphone with one of the given names found'
        super().__init__(self.device_index)

    def __str__(self):
        return self.name

    # returns string for debugging
    def str_selected_mic_list(self):
        str_selected_mic_list = ''
        for mic_index, mic_name in enumerate(self.list_microphone_names()):
            if mic_index == self.device_index:
                str_selected_mic_list += '-> '
            else:
                str_selected_mic_list += '   '
            str_selected_mic_list += str(mic_index) + ' ' + mic_name + '\n'

        return str_selected_mic_list


# controls all audio-outputs and LEDs
class Audio_LED_Controller():
    def __init__(self):
        self.available_songs = []
        self.volume = 100
        self.listening_volume = 15

        for file_name in os.listdir('audio_files/songs'):
            if file_name[-4:] == '.wav':
                self.available_songs.append(file_name[:-4])

    def play_all_songs():
        pass

    def play_single_song():
        pass

    def pause():
        pass

    def resume():
        pass

    def listening():
        pass

    def listening_end():
        pass

    def set_volume():
        pass


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
