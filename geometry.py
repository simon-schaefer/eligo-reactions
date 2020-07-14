import typing

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QBrush, QColor, QPainter, QPen, QPolygon
from PyQt5.QtCore import Qt, QPoint


class Shape:

    forms = ["square", "circle", "triangle_up", "triangle_down", "triangle_left", "triangle_right",
             "corner_1", "corner_2", "corner_3", "corner_4", "tetraeder", "hexagon", "octagon", "plus",
             "arrow_right", "arrow_left"]
    colors = [Qt.red]

    def __init__(self, data: typing.Any = None, form: str = "square", color: QColor = Qt.red):
        assert color in self.colors
        self._color = color
        assert form in self.forms
        self._form = form
        self._data = data

    ################################################################################
    # Geometrical Properties #######################################################
    ################################################################################
    def draw(self, window: QWidget, position: typing.Tuple[int, int], size: typing.Union[int, typing.Tuple[int, int]]
             ) -> QPainter:
        assert len(position) == 2
        if type(size) == int:
            dx = dy = size
        else:
            assert len(size) == 2
            dx, dy = size

        painter = QPainter()
        painter.begin(window)
        painter.setPen(QPen(self.color, Qt.SolidPattern))
        painter.setBrush(QBrush(self.color, Qt.SolidPattern))

        if self.form == "circle":
            painter.drawEllipse(*position, dx, dy)
        elif self.form == "square":
            painter.drawRect(*position, dx, dy)
        elif self.form == "triangle_up":
            painter.drawPolygon(QPolygon([QPoint(position[0], position[1] + dy),
                                          QPoint(position[0] + dx, position[1] + dy),
                                          QPoint(position[0] + dx / 2, position[1])]))
        elif self.form == "triangle_down":
            painter.drawPolygon(QPolygon([QPoint(position[0], position[1]),
                                          QPoint(position[0] + dx, position[1]),
                                          QPoint(position[0] + dx / 2, position[1] + dy)]))
        elif self.form == "triangle_left":
            painter.drawPolygon(QPolygon([QPoint(position[0], position[1]),
                                          QPoint(position[0], position[1] + dy),
                                          QPoint(position[0] + dx, position[1] + dy / 2)]))
        elif self.form == "triangle_right":
            painter.drawPolygon(QPolygon([QPoint(position[0] + dx, position[1]),
                                          QPoint(position[0] + dx, position[1] + dy),
                                          QPoint(position[0], position[1] + dy / 2)]))
        elif self.form == "corner_1":
            painter.drawPolygon(QPolygon([QPoint(position[0], position[1]),
                                          QPoint(position[0] + dx, position[1]),
                                          QPoint(position[0], position[1] + dy)]))
        elif self.form == "corner_2":
            painter.drawPolygon(QPolygon([QPoint(position[0], position[1]),
                                          QPoint(position[0], position[1] + dy),
                                          QPoint(position[0] + dx, position[1] + dy)]))
        elif self.form == "corner_3":
            painter.drawPolygon(QPolygon([QPoint(position[0], position[1] + dy),
                                          QPoint(position[0] + dx, position[1] + dy),
                                          QPoint(position[0] + dx, position[1])]))
        elif self.form == "corner_4":
            painter.drawPolygon(QPolygon([QPoint(position[0], position[1]),
                                          QPoint(position[0] + dx, position[1]),
                                          QPoint(position[0] + dx, position[1] + dy)]))
        elif self.form == "tetraeder":
            painter.drawPolygon(QPolygon([QPoint(position[0] + dx/2, position[1]),
                                          QPoint(position[0], position[1] + dy/2),
                                          QPoint(position[0] + dx/2, position[1] + dy),
                                          QPoint(position[0] + dx, position[1] + dy/2)]))
        elif self.form == "hexagon":
            painter.drawPolygon(QPolygon([QPoint(position[0] + dx / 3 * 1, position[1]),
                                          QPoint(position[0] + dx / 3 * 2, position[1]),
                                          QPoint(position[0] + dx, position[1] + dy/2),
                                          QPoint(position[0] + dx / 3 * 2, position[1] + dy),
                                          QPoint(position[0] + dx / 3 * 1, position[1] + dy),
                                          QPoint(position[0], position[1] + dy/2)]))
        elif self.form == "octagon":
            painter.drawPolygon(QPolygon([QPoint(position[0] + dx / 3 * 1, position[1]),
                                          QPoint(position[0] + dx / 3 * 2, position[1]),
                                          QPoint(position[0] + dx, position[1] + dy / 3 * 1),
                                          QPoint(position[0] + dx, position[1] + dy / 3 * 2),
                                          QPoint(position[0] + dx / 3 * 2, position[1] + dy),
                                          QPoint(position[0] + dx / 3 * 1, position[1] + dy),
                                          QPoint(position[0], position[1] + dy / 3 * 2),
                                          QPoint(position[0], position[1] + dy / 3 * 1)]))
        elif self.form == "plus":
            painter.drawPolygon(QPolygon([QPoint(position[0] + dx / 3 * 1, position[1]),
                                          QPoint(position[0] + dx / 3 * 2, position[1]),
                                          QPoint(position[0] + dx / 3 * 2, position[1] + dy / 3 * 1),
                                          QPoint(position[0] + dx, position[1] + dy / 3 * 1),
                                          QPoint(position[0] + dx, position[1] + dy / 3 * 2),
                                          QPoint(position[0] + dx / 3 * 2, position[1] + dy / 3 * 2),
                                          QPoint(position[0] + dx / 3 * 2, position[1] + dy),
                                          QPoint(position[0] + dx / 3 * 1, position[1] + dy),
                                          QPoint(position[0] + dx / 3 * 1, position[1] + dy / 3 * 2),
                                          QPoint(position[0], position[1] + dy / 3 * 2),
                                          QPoint(position[0], position[1] + dy / 3 * 1),
                                          QPoint(position[0] + dx / 3 * 1, position[1] + dy / 3 * 1)]))
        elif self.form == "arrow_right":
            painter.drawPolygon(QPolygon([QPoint(position[0], position[1] + dy / 3 * 1),
                                          QPoint(position[0] + dx / 2, position[1] + dy / 3 * 1),
                                          QPoint(position[0] + dx / 2, position[1]),
                                          QPoint(position[0] + dx, position[1] + dy / 2),
                                          QPoint(position[0] + dx / 2, position[1] + dy),
                                          QPoint(position[0] + dx / 2, position[1] + dy / 3 * 2),
                                          QPoint(position[0], position[1] + dy / 3 * 2)]))
        elif self.form == "arrow_left":
            painter.drawPolygon(QPolygon([QPoint(position[0] + dx, position[1] + dy / 3 * 1),
                                          QPoint(position[0] + dx / 2, position[1] + dy / 3 * 1),
                                          QPoint(position[0] + dx / 2, position[1]),
                                          QPoint(position[0], position[1] + dy / 2),
                                          QPoint(position[0] + dx / 2, position[1] + dy),
                                          QPoint(position[0] + dx / 2, position[1] + dy / 3 * 2),
                                          QPoint(position[0] + dx, position[1] + dy / 3 * 2)]))
        else:
            raise ValueError(f"Invalid shape {self.form} !")
        painter.end()
        return painter

    ################################################################################
    # Operators ####################################################################
    ################################################################################
    def __add__(self, other):
        return Shape(data=self.data + other.data)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return Shape(data=self.data - other.data)

    def __mul__(self, other):
        return Shape(data=self.data * other.data)

    def __truediv__(self, other):
        return Shape(data=self.data / other.data)

    def __str__(self) -> str:
        return f"{self.form}({self.data}, {self.color})"

    def __repr__(self):
        return self.__str__()

    ################################################################################
    # Shape Properties #############################################################
    ################################################################################
    @property
    def color(self) -> str:
        return self._color

    @property
    def form(self) -> str:
        return self._form

    @property
    def data(self) -> typing.Any:
        return self._data
