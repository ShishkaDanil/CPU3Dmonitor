import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import psutil
import time
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import winreg

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("System Monitor")
        self.setGeometry(0, 0, 400, 400)  # Уменьшаем размер окна
        self.setWindowFlag(Qt.FramelessWindowHint)  # Убираем рамку окна
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.setAttribute(Qt.WA_TranslucentBackground)  # Делаем фон прозрачным

        # Помещаем график немного левее и в правый верхний угол
        screen_geometry = QApplication.desktop().availableGeometry()
        self.move(screen_geometry.width() - 400, -70)

        # Создаем фигуру Matplotlib
        self.fig = Figure(figsize=(5, 3), facecolor='none')
        self.canvas = FigureCanvas(self.fig)

        # Добавляем виджет холста в окно
        self.setCentralWidget(self.canvas)

        # Инициализация данных
        self.cpu_data = []
        self.memory_data = []
        self.time_data = []

        # Инициализация графика
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('CPU Usage (%)')
        self.ax.set_zlabel('Time (s)')
        self.ax.set_ylabel('Memory Usage (%)')
        self.ax.set_facecolor((0, 0, 0, 0))
        self.ax.view_init(elev=30, azim=45)
        # Настройка анимации
        self.ani = FuncAnimation(self.fig, self.update_data, interval=100, cache_frame_data=False)

    def get_system_info(self):
        cpu_usage = psutil.cpu_percent(interval=0.1)
        memory_info = psutil.virtual_memory()
        memory_usage = memory_info.percent
        return cpu_usage, memory_usage

    def normalize_data(self, data):
        min_val = min(data)
        max_val = max(data)
        if max_val == min_val:
            return [0.5 for _ in data]
        return [(d - min_val) / (max_val - min_val) for d in data]

    def update_data(self, frame):
        cpu, memory = self.get_system_info()
        current_time = time.time()

        self.cpu_data.append(cpu)
        self.memory_data.append(memory)
        self.time_data.append(current_time)

        if len(self.time_data) > 20:
            self.cpu_data = self.cpu_data[-20:]
            self.memory_data = self.memory_data[-20:]
            self.time_data = self.time_data[-20:]

        normalized_memory_data = self.normalize_data(self.memory_data)

        self.ax.clear()
        self.ax.set_xlabel('CPU Usage (%)')
        self.ax.set_zlabel('Time (s)')
        self.ax.set_ylabel('Memory Usage (%)')
        relative_time = [t - self.time_data[0] for t in self.time_data]

        for i in range(1, len(self.cpu_data)):
            x = [0, 0, self.cpu_data[i], self.cpu_data[i - 1], 0]
            z = [relative_time[i - 1], relative_time[i], relative_time[i], relative_time[i - 1], relative_time[i - 1]]
            y = [0, normalized_memory_data[i - 1], normalized_memory_data[i - 1], 0, 0]
            color = (normalized_memory_data[i - 1] * self.cpu_data[i - 1]) / 50
            self.ax.plot(x, y, z, color=plt.cm.viridis(color + 5), linewidth=1, alpha=0.1)

            verts = [list(zip(x, y, z))]
            poly = Poly3DCollection(verts, color=plt.cm.viridis(color + 5), alpha=0.7)
            self.ax.add_collection3d(poly)

            if i > 1:
                prev_x = [0, 0, self.cpu_data[i - 1], self.cpu_data[i - 2], 0]
                prev_z = [relative_time[i - 2], relative_time[i - 1], relative_time[i - 1], relative_time[i - 2], relative_time[i - 2]]
                prev_y = [0, normalized_memory_data[i - 2], normalized_memory_data[i - 2], 0, 0]
                self.ax.plot_surface(np.array([prev_x, x]), np.array([prev_y, y]), np.array([prev_z, z]), color=plt.cm.viridis(color + 5), alpha=0.7)

        self.ax.set_xticks(np.linspace(0, 100, num=6))
        self.ax.set_xticklabels([f'{int(t)}%' for t in np.linspace(0, 100, num=6)], fontsize=8, rotation=45)
        self.ax.set_yticks(np.linspace(0, 1, num=6))
        self.ax.set_yticklabels([f'{round(float(t), 2)}%' for t in np.linspace(min(self.memory_data), max(self.memory_data), num=6)], fontsize=8, rotation=45)

def add_to_startup():
    # Получаем путь к текущему исполняемому файлу
    exe_path = os.path.abspath(sys.argv[0])
    # Имя ключа в реестре
    key_name = "CPU3Dmonitor"
    # Открываем ключ реестра для автозапуска
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                        r"Software\Microsoft\Windows\CurrentVersion\Run",
                        0, winreg.KEY_SET_VALUE)
    # Добавляем путь к исполняемому файлу
    winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, exe_path)
    key.Close()

if __name__ == '__main__':
    add_to_startup()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
