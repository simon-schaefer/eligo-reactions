import argparse
import logging
import sys
import typing

import pandas as pd
from PyQt5.QtWidgets import QWidget, QApplication, QDesktopWidget
from PyQt5.QtGui import QFont, QPainter, QKeyEvent, QCloseEvent
from PyQt5.QtCore import QRect, Qt

from exercise import Exercise
from geometry import Shape


class Window(QWidget):

    def __init__(self):
        super().__init__()

        # Create window at center of the display.
        display_geometry = QDesktopWidget().availableGeometry()
        window_size = display_geometry.size() / 2
        dx, dy = window_size.width(), window_size.height()

        display_geometry = QDesktopWidget().availableGeometry()
        display_center = display_geometry.center()
        x = display_center.x() - dx / 2
        y = display_center.y() - dy / 2
        self.setGeometry(int(x), int(y), dx, dy)
        self.setFixedSize(dx, dy)

        # Initialize statistic and exercise result variable.
        self.exercise = Exercise(num_shapes=2)
        self.statistics = pd.DataFrame(columns=["time", "correct"])

        # Set window properties.
        self.setWindowTitle('eligo_reactions')
        self.show()

    def paintEvent(self, e) -> None:
        super(Window, self).paintEvent(e)

        # If the time is running the previous task has not been solved, so do not update
        # the window's content. Only if the timer is None
        if self.exercise.task is None:
            self.exercise.new_task()
            logging.debug(self.exercise)

        shapes_dict, shapes_task, task_description, operation = self.exercise.task
        self.draw_legend(shapes_dict)
        self.draw_exercise(task_description)
        self.draw_task(shapes_task, operation)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        time_needed = self.exercise.time_needed()
        key_pressed = "left" if a0.key() == Qt.Key_Left else "right"
        is_correct = (key_pressed == self.exercise.solution)
        statistic = {"time": time_needed, "correct": is_correct}
        self.statistics = self.statistics.append(statistic, ignore_index=True)

        self.exercise.reset_task()
        self.update()

    def closeEvent(self, a0: QCloseEvent) -> None:
        logging.info("--- Statistics ---")
        logging.debug(self.statistics)
        logging.info(self.statistics.mean())

    ################################################################################
    # Drawing ######################################################################
    ################################################################################
    def draw_exercise(self, task_description: str):
        window_size = self.get_size()
        text = f"Which side is {task_description} (or equal) ?"

        painter = QPainter()
        painter.begin(self)
        painter.setFont(QFont('Times', 35))
        painter.drawText(QRect(0, 0, window_size[0], window_size[1] / 8), Qt.AlignCenter | Qt.AlignCenter, text)
        painter.end()

    def draw_task(self, task: typing.List[typing.List[Shape]], operation: str, size: int = 30):
        window_size = self.get_size()
        num_sides = len(task)

        for s, shapes_s in enumerate(task):
            x0 = window_size[0] / num_sides / 2 * (1 + 2 * s)
            num_shapes = len(shapes_s)

            for n, shape in enumerate(shapes_s):
                x = int(x0 + size * 2 * (n - num_shapes + 1))
                y = int(window_size[1] / 3)
                painter = shape.draw(window=self, position=(x, y), size=size)

                if n < num_shapes - 1:
                    painter.begin(self)
                    painter.setFont(QFont('Times', 35))
                    painter.drawText(QRect(x + size, y, size, size), Qt.AlignLeft | Qt.AlignCenter, operation)
                    painter.end()

    def draw_legend(self, shape_dict: typing.List[Shape]):
        window_size = self.get_size()
        size = int(window_size[0] / (len(shape_dict) * 2 + 2))

        for n, shape in enumerate(shape_dict):
            x = int(size * (1 + n * 2))
            y = int(window_size[1] / 4 * 3)
            painter = shape.draw(window=self, position=(x, y), size=size)

            painter.begin(self)
            painter.drawText(QRect(x + size, y, size, size), Qt.AlignLeft | Qt.AlignCenter, f" = {shape.data}")
            painter.end()

    ################################################################################
    # Window Geometry ##############################################################
    ################################################################################
    def get_size(self) -> typing.Tuple[int, int]:
        return self.geometry().width(), self.geometry().height()

    def get_position(self) -> typing.Tuple[int, int]:
        return self.geometry().x(), self.geometry().y()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="log debugging mode")
    args = parser.parse_args()

    log_level = logging.INFO if not args.debug else logging.DEBUG
    logging.basicConfig(level=log_level, format="%(message)s")

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
