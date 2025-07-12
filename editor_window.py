import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QSlider, QLabel, QFrame
)
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import music_control as mc
import track1_control as t1
import track2_control as t2


class AudioEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Samplifast 🎵")
        self.setGeometry(100, 100, 1400, 800)

        self.tracks = [
            {"data": None, "sample_rate": None, "original_data": None, "volume": 1.0, "playing": False, "stream": None, "play_pointer": 0},
            {"data": None, "sample_rate": None, "original_data": None, "volume": 1.0, "playing": False, "stream": None, "play_pointer": 0}
        ]

        self.track_axes = []
        self.track_canvases = []

        button_style = (
            "QPushButton { background-color: #2e2e2e; color: white; "
            "padding: 8px; font-weight: bold; border: 1px solid white; }"
        )

        main_layout = QHBoxLayout()
        left_panel = QVBoxLayout()

        # --- Track 1 Controls ---
        left_panel.addWidget(QLabel("🎚 Дорожка 1"))
        for label, func in [
            ("Загрузить", lambda: t1.load_audio(self, 0)),
            ("Воспроизвести", lambda: mc.play_pause_track(self, 0)),
        ]:
            btn = QPushButton(label)
            btn.setStyleSheet(button_style)
            btn.clicked.connect(func)
            left_panel.addWidget(btn)

        slider1 = QSlider(Qt.Horizontal)
        slider1.setMinimum(0)
        slider1.setMaximum(100)
        slider1.setValue(100)
        slider1.valueChanged.connect(lambda value: mc.update_volume(self, 0, value))
        left_panel.addWidget(slider1)

        left_panel.addWidget(self._divider())

        left_panel.addWidget(QLabel("🎚 Дорожка 2"))
        for label, func in [
            ("Загрузить", lambda: t2.load_audio(self, 1)),
            ("Воспроизвести", lambda: mc.play_pause_track(self, 1)),
        ]:
            btn = QPushButton(label)
            btn.setStyleSheet(button_style)
            btn.clicked.connect(func)
            left_panel.addWidget(btn)

        slider2 = QSlider(Qt.Horizontal)
        slider2.setMinimum(0)
        slider2.setMaximum(100)
        slider2.setValue(100)
        slider2.valueChanged.connect(lambda value: mc.update_volume(self, 1, value))
        left_panel.addWidget(slider2)

        left_panel.addWidget(self._divider())

        left_panel.addWidget(QLabel("🎛 Общие"))
        for label, func in [
            ("Воспроизвести все", lambda: mc.play_pause_all(self)),
            ("Экспорт", lambda: mc.export_all(self)),
            ("Undo", lambda: print("Undo")),
            ("Redo", lambda: print("Redo")),
            ("Настройки", lambda: print("Настройки")),
            ("🎛 Эффекты", lambda: print("Эффекты")),
            ("🎵 Метроном", lambda: print("Метроном")),
        ]:
            btn = QPushButton(label)
            btn.setStyleSheet(button_style)
            btn.clicked.connect(func)
            left_panel.addWidget(btn)

        left_container = QWidget()
        left_container.setLayout(left_panel)
        left_container.setFixedWidth(220)
        left_container.setStyleSheet("background-color: #1c1c1c; color: white;")

        plot_layout = QVBoxLayout()
        for i in range(2):
            fig, ax = plt.subplots()
            canvas = FigureCanvas(fig)
            canvas.setStyleSheet("background-color: black;")
            plot_layout.addWidget(canvas)
            self.track_axes.append(ax)
            self.track_canvases.append(canvas)

        plot_container = QWidget()
        plot_container.setLayout(plot_layout)
        plot_container.setStyleSheet("background-color: black;")

        main_layout.addWidget(left_container)
        main_layout.addWidget(plot_container)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def plot_track(self, index):
        if self.tracks[index]["data"] is None:
            return

        ax = self.track_axes[index]
        canvas = self.track_canvases[index]

        ax.clear()
        data = self.tracks[index]["data"]
        sr = self.tracks[index]["sample_rate"]
        time = np.arange(len(data)) / sr
        ax.plot(time, data, color='cyan')
        ax.set_facecolor("black")
        ax.set_title(f"Дорожка {index + 1}", color='white')
        ax.set_xlabel("Время (сек)", color='white')
        ax.set_ylabel("Амплитуда", color='white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        canvas.draw()

    def _divider(self):
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        divider.setStyleSheet("color: grey;")
        return divider
