import sounddevice as sd
import numpy as np
import soundfile as sf
from PyQt5.QtWidgets import QFileDialog


def play_pause_track(self, track_index):
    track = self.tracks[track_index] 
    if track["data"] is None:
        return

    if track.get("playing", False):
        if track["stream"] is not None:
            track["stream"].stop()
            track["stream"].close()
            track["stream"] = None
        track["playing"] = False
    else:
        track["playing"] = True
        track["play_pointer"] = 0

        def callback(outdata, frames, time, status):
            data = track["data"]
            start = track["play_pointer"]
            end = start + frames
            chunk = data[start:end]
            if len(chunk) < frames:
                chunk = np.pad(chunk, (0, frames - len(chunk)), 'constant')
                track["playing"] = False
                raise sd.CallbackStop()

            chunk = chunk * track["volume"]
            if chunk.ndim == 1:
                chunk = chunk.reshape(-1, 1)
            outdata[:len(chunk)] = chunk
            track["play_pointer"] += frames

        track["stream"] = sd.OutputStream(
            samplerate=track["sample_rate"],
            channels=1 if track["data"].ndim == 1 else track["data"].shape[1],
            callback=callback
        )
        track["stream"].start()


def play_pause_all(self):
    any_playing = any(track.get("playing", False) for track in self.tracks)
    if any_playing:
        for track in self.tracks:
            if track["stream"] is not None:
                track["stream"].stop()
                track["stream"].close()
                track["stream"] = None
            track["playing"] = False
    else:
        for i in range(len(self.tracks)):
            play_pause_track(self, i)


def update_volume(self, track_index, value):
    self.tracks[track_index]["volume"] = value / 100.0


def export_all(self):
    file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить как", "", "WAV files (*.wav)")
    if not file_path:
        return

    max_length = max(len(track["data"]) for track in self.tracks if track["data"] is not None)

    mixed = None
    sample_rate = None

    for track in self.tracks:
        if track["data"] is not None:
            if sample_rate is None:
                sample_rate = track["sample_rate"]

            data = track["data"] * track["volume"]
            if len(data) < max_length:

                if data.ndim == 1:
                    data = np.pad(data, (0, max_length - len(data)), 'constant')
                else:
                    data = np.pad(data, ((0, max_length - len(data)), (0, 0)), 'constant')

            if mixed is None:
                mixed = data
            else:
                mixed += data

    if mixed is not None:

        mixed = mixed / np.max(np.abs(mixed))
        sf.write(file_path, mixed, sample_rate)
