#! /usr/bin/env python3

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, WindowOperations
import argparse
import sounddevice as sd
import numpy as np
import time

class NeuralOscillations():
    def __init__(self, sound_duration=0.5, sampling_rate=44100, timeout=0, board_id=BoardIds.SYNTHETIC_BOARD, ip_port=0,
                 ip_protocol=0, ip_address='', serial_port='', mac_address='',
                 streamer_params='', serial_number='', file='', master_board=BoardIds.NO_BOARD):
        self.sound_duration = sound_duration
        self.sampling_rate = sampling_rate
        self.timeout = timeout
        self.board_id = board_id
        self.ip_port = ip_port
        self.ip_protocol = ip_protocol
        self.ip_address = ip_address
        self.serial_port = serial_port
        self.mac_address = mac_address
        self.streamer_params = streamer_params
        self.serial_number = serial_number
        self.file = file
        self.master_board = master_board

        self.window_function = 3
        # NO_WINDOW = 0
        # HANNING = 1
        # HAMMING = 2
        # BLACKMAN_HARRIS = 3

        self.num_samples = 512

        self.delta_waves = self.DeltaWaves()
        self.theta_waves = self.ThetaWaves()
        self.alpha_waves = self.AlphaWaves()
        self.beta_waves = self.BetaWaves()
        self.gamma_waves = self.GammaWaves()

    class DeltaWaves:
        def __init__(self):
            self.lower = 0.5
            self.upper = 1.5
            self.means = list()

        def display_bounds(self):
            print(f'[{self.lower}, {self.upper}]')

        def display_means(self):
            print(self.means)

    class ThetaWaves:
        def __init__(self):
            self.lower = 4.0
            self.upper = 10.0
            self.means = list()

        def display_bounds(self):
            print(f'[{self.lower}, {self.upper}]')

        def display_means(self):
            print(self.means)

    class AlphaWaves:
        def __init__(self):
            self.lower = 8.0
            self.upper = 12.0
            self.means = list()

        def display_bounds(self):
            print(f'[{self.lower}, {self.upper}]')

        def display_means(self):
            print(self.means)

    class BetaWaves:
        def __init__(self):
            self.lower = 13.0
            self.upper = 30.0
            self.means = list()

        def display_bounds(self):
            print(f'[{self.lower}, {self.upper}]')

        def display_means(self):
            print(self.means)

    class GammaWaves:
        def __init__(self):
            self.lower = 30.0
            self.upper = 120.0
            self.means = list()

        def display_bounds(self):
            print(f'[{self.lower}, {self.upper}]')

        def display_means(self):
            print(self.means)

    def initialise_board(self):
        params = BrainFlowInputParams()
        params.timeout = self.timeout
        params.board_id = self.board_id
        params.ip_port = self.ip_port
        params.ip_protocol = self.ip_protocol
        params.ip_address = self.ip_address
        params.serial_port = self.serial_port
        params.mac_address = self.mac_address
        params.streamer_params = self.streamer_params
        params.serial_number = self.serial_number
        params.file = self.file
        params.master_board = self.master_board
        return BoardShim(self.board_id, params)

    def filter(self, eeg_data, lower_bound, upper_bound, window_function):
        psd = DataFilter.get_psd(eeg_data, BoardShim.get_sampling_rate(self.board_id), window_function)
        return DataFilter.get_band_power(psd, lower_bound, upper_bound)

    def overall_threshold(self, iteration, means):
        return sum(means) / (iterations + 1) * 1.04

    def moving_window_threshold(self, iteration, means, window_size):
        if iteration < window_size:
            return self.overall_threshold(iteration, means)
        return sum(means[-window_size:]) / window_size * 1.04

    def generate_tones(self, test_freq=440, faint_freq=880, loud_freq=220, amp=0.5):
        time_interval_arr = np.arange(self.sampling_rate * self.sound_duration) / self.sampling_rate
        test = amp * np.sin(2 * np.pi * test_freq* time_interval_arr)
        faint = amp * np.sin(2 * np.pi * faint_freq* time_interval_arr)
        loud = amp * np.sin(2 * np.pi * loud_freq* time_interval_arr)
        return test, faint, loud

    def play_tone(self, tone):
        sd.play(tone, self.sampling_rate)

    # Number of Samples has to be 512 to be compatible with all 5 waves
    def eeg_recorder(self, eeg_channel_count=8, delta=True, theta=True, alpha=True, beta=True, gamma=True):
        board = self.initialise_board()
        eeg_channels = BoardShim.get_eeg_channels(self.board_id)
        board.prepare_session()
        board.start_stream()
        time.sleep(3)
        try:
            while True:
                data = board.get_current_board_data(self.num_samples)
                dMean, tMean, aMean, bMean, gMean = 0, 0, 0, 0, 0
                for c in range(eeg_channel_count):
                    if delta:
                        dMean += np.mean(self.filter(data[eeg_channels[c]], self.delta_waves.lower, self.delta_waves.upper, self.window_function))
                    if theta:
                        tMean += np.mean(self.filter(data[eeg_channels[c]], self.theta_waves.lower, self.theta_waves.upper, self.window_function))
                    if alpha:
                        aMean += np.mean(self.filter(data[eeg_channels[c]], self.alpha_waves.lower, self.alpha_waves.upper, self.window_function))
                    if beta:
                        bMean += np.mean(self.filter(data[eeg_channels[c]], self.beta_waves.lower, self.beta_waves.upper, self.window_function))
                    if gamma:
                        gMean += np.mean(self.filter(data[eeg_channels[c]], self.gamma_waves.lower, self.gamma_waves.upper, self.window_function))
                dMean = dMean / eeg_channel_count
                tMean = tMean / eeg_channel_count
                aMean = aMean / eeg_channel_count
                bMean = bMean / eeg_channel_count
                gMean = gMean / eeg_channel_count

                print(f'Delta: {dMean:.6f}\tTheta: {tMean:.6f}\tAlpha: {aMean:.6f}\tBeta: {bMean:.6f}\tGamma: {gMean:.6f}\t')
                time.sleep(1)

                self.delta_waves.means.append(dMean)
                self.theta_waves.means.append(tMean)
                self.alpha_waves.means.append(aMean)
                self.beta_waves.means.append(bMean)
                self.gamma_waves.means.append(gMean)

        except KeyboardInterrupt:
            board.stop_stream()
            board.release_session()
            raise Exception

    def create_csv(self):
        pass



def get_args():
    parser = argparse.ArgumentParser(add_help=False)
    args, remaining = parser.parse_known_args()
    parser.add_argument('-b', '--board-id', type=int, help='CYTON_BOARD=0, SYNTHETIC_BOARD=-1')
    parser.add_argument('-e', '--eeg-channel-count', type=int, help='Number of EEG channels connected')
    parser.add_argument('-p', '--serial-port', type=str, help='Path to serial port')
    args = parser.parse_args(remaining)
    config = vars(args)
    return config


if __name__ == "__main__":
    config = get_args()
    # SERIAL_PORT = "/dev/cu.usbserial-D200QZLM" for John's MacBook!
    BOARD_ID = config.get('board_id')
    EEG_CHANNEL_COUNT = config.get('eeg_channel_count')
    SERIAL_PORT = config.get('serial_port')
    # neural_oscillations = NeuralOscillations(board_id=BOARD_ID, serial_port=SERIAL_PORT)
    neural_oscillations = NeuralOscillations(serial_port=SERIAL_PORT, board_id=BOARD_ID)
    neural_oscillations.eeg_recorder(eeg_channel_count=EEG_CHANNEL_COUNT)
