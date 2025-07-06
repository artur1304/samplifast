import soundfile as sf
from PyQt5.QtWidgets import QFileDialog

def load_audio(self, track_index):
    try:
        file_path, _ = QFileDialog.getOpenFileName(self, "Выбрать аудиофайл", "", "Audio Files (*.wav *.flac *.aiff *.mp3)")
        if file_path:
            data, sr = sf.read(file_path)
            self.tracks[track_index]["data"] = data
            self.tracks[track_index]["original_data"] = data.copy()
            self.tracks[track_index]["sample_rate"] = sr
            self.plot_track(track_index)
    except Exception as e:
        print(f"Ошибка при загрузке аудио дорожки {track_index + 1}: {e}")

def update_volume(self, track_index, value):
    self.tracks[track_index]["volume"] = value / 100.0
