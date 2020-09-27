import pygame
from random import random
from math import sqrt


class Vector:
    """Сlass of vectors"""

    def __init__(self, coordinates):
        """Initialization method"""
        self.coordinates = coordinates

    def __str__(self):
        """Method for string representation"""
        return str(self.coordinates)

    def __repr__(self):
        """Method for representation in lists"""
        return self.__str__()

    def __eq__(self, other):
        """Method for comparison"""
        if self.coordinates == other.coordinates:
            return True
        else:
            return False

    def __len__(self):
        """"Method for calculating length of vector"""
        return round(sqrt(self.coordinates[0] * self.coordinates[0] + self.coordinates[1]
                          * self.coordinates[1]))

    def __add__(self, other):
        """"Method for calculating the sum"""
        return Vector((self.coordinates[0] + other.coordinates[0], self.coordinates[1]
                       + other.coordinates[1]))

    def __sub__(self, other):
        """"Method for calculating the difference"""
        return Vector((self.coordinates[0] - other.coordinates[0], self.coordinates[1]
                       - other.coordinates[1]))

    def __truediv__(self, other):
        """"Method for calculating the division"""
        if isinstance(self, Vector):
            return self * (1 / other)

    def __mul__(self, other):
        """"Method for calculating the multiplication"""
        if isinstance(other, Vector) and isinstance(self, Vector):
            # dot product of vectors
            return self.coordinates[0] * other.coordinates[0] + self.coordinates[1] \
                   * other.coordinates[1]
        else:
            # vector-scalar multiplication
            return Vector((self.coordinates[0] * other, self.coordinates[1] * other))

    @staticmethod
    def vector(x, y):
        """Method for creating a vector at the start (x) and end (y) of the
         directed line"""
        x = Vector(x)
        y = Vector(y)
        return y - x

    @staticmethod
    def int_pair(x, y):
        """Method for getting a pair of integers as a tuple"""
        return x, y


class Line:
    """Class of closed polylines"""

    def __init__(self, points=None):
        """Initialization method"""
        self.points = points or []
        self.speeds = None

    def __str__(self):
        """Method for string representation"""
        return str(self.points)

    def __repr__(self):
        """Method for representation in lists"""
        return self.__str__()

    def add_point(self):
        """Method for adding a point(from class Vector) to a polyline with
         its speed"""
        self.points.append(Vector(event.pos))
        self.speeds.append(Vector((random() * 2, random() * 2)))

    def del_point(self):
        """Method for removing a point from a curve"""
        if len(self.points) != 0:
            self.points = self.points[:-1]

    def fast_line(self):
        """Method for accelerating the curve"""
        if self.speeds:
            for speed in range(len(self.speeds) - 1):
                self.speeds[speed] = self.speeds[speed] * 2

    def slow_line(self):
        """Method for decelerating the curve"""
        if self.speeds:
            for speed in range(len(self.speeds) - 1):
                self.speeds[speed] = self.speeds[speed] * 0.5

    def set_points(self, speeds):
        """Method for recalculation of coordinates of points"""
        for point in range(len(self.points)):
            self.points[point] = self.points[point] + speeds[point]
            if self.points[point].coordinates[0] > SCREEN_SIZE[0] or \
                    self.points[point].coordinates[0] < 0:
                speeds[point].coordinates = (- speeds[point].coordinates[0],
                                             speeds[point].coordinates[1])
            if self.points[point].coordinates[1] > SCREEN_SIZE[1] or \
                    self.points[point].coordinates[1] < 0:
                speeds[point].coordinates = (speeds[point].coordinates[0],
                                             -speeds[point].coordinates[1])

    def draw_points(self, style="points", width=4, color=(255, 255, 255)):
        """Method for drawing points and lines"""
        if style == "line":
            for point_number in range(-1, len(self.points) - 1):
                pygame.draw.line(gameDisplay, color,
                                 (int(self.points[point_number].coordinates[0]),
                                  int(self.points[point_number].coordinates[1])),
                                 (int(self.points[point_number + 1].coordinates[0]),
                                  int(self.points[point_number + 1].coordinates[1])),
                                 width)

        elif style == "points":
            for point in self.points:
                pygame.draw.circle(gameDisplay, color,
                                   (int(point.coordinates[0]),
                                    int(point.coordinates[1])), width)


class Joint(Line):
    """"""

    def __init__(self, points=None):
        """Initialization method"""
        super().__init__(points)

    def __str__(self):
        """Method for string representation"""
        return super().__str__()

    def __repr__(self):
        """Method for representation in lists"""
        return self.__str__()

    def get_point(self, alpha, deg=None):
        if deg is None:
            deg = len(self.points) - 1
        if deg == 0:
            return self.points[0]
        return self.points[deg] * alpha + self.get_point(alpha, deg - 1) * \
               (1 - alpha)

    def get_points(self, count):
        alpha = 1 / count
        result = []
        for i in range(count):
            result.append(self.get_point(i * alpha))
        return result

    def get_joint(self, count):
        """Method for calculating curve points by added points"""
        if len(self.points) < 3:
            return Joint()
        result = []
        for i in range(-2, len(self.points) - 2):
            pnt = []
            pnt.append((self.points[i] + self.points[i + 1]) * 0.5)
            pnt.append(self.points[i + 1])
            pnt.append((self.points[i + 1] + self.points[i + 2]) * 0.5)
            pnt = Joint(pnt)
            result.extend(pnt.get_points(count))
        return Joint(result)


class Game:
    """Class of game"""

    @staticmethod
    def display_help():
        """Method for showing display with instruction"""
        gameDisplay.fill((50, 50, 50))
        font1 = pygame.font.SysFont("arial", 30)
        font2 = pygame.font.SysFont("serif", 30)
        data = []
        data.append(["F1", "Помощь"])
        data.append(["R", "Перезапуск"])
        data.append(["P", "Воспроизвести / Пауза"])
        data.append(["Num+", "Добавить точку"])
        data.append(["Num-", "Удалить точку"])
        data.append(["D", "Удалить точку из кривой"])
        data.append(["F", "Ускорение движения кривой"])
        data.append(["L", "Замедление движения кривой"])
        data.append(["", ""])
        data.append([str(steps), "текущих точек"])

        pygame.draw.lines(gameDisplay, (255, 50, 50, 255), True, [
            (0, 0), (800, 0), (800, 600), (0, 600)], 5)
        for item, text in enumerate(data):
            gameDisplay.blit(font1.render(
                text[0], True, (128, 128, 255)), (100, 100 + 30 * item))
            gameDisplay.blit(font2.render(
                text[1], True, (128, 128, 255)), (200, 100 + 30 * item))


if __name__ == "__main__":
    SCREEN_SIZE = (1280, 720)
    pygame.init()
    gameDisplay = pygame.display.set_mode(SCREEN_SIZE)
    pygame.display.set_caption("Screen Saver")

    steps = 20
    working = True
    line = Joint()
    line.speeds = []
    show_help = False
    pause = False

    color_param = 0
    color = pygame.Color(0)

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    working = False
                if event.key == pygame.K_r:
                    line.points = []
                    line.speeds = []
                if event.key == pygame.K_p:
                    pause = not pause
                if event.key == pygame.K_KP_PLUS:
                    steps += 1
                if event.key == pygame.K_F1:
                    show_help = not show_help
                if event.key == pygame.K_KP_MINUS:
                    steps -= 1 if steps > 1 else 0
                if event.key == pygame.K_d:
                    line.del_point()
                if event.key == pygame.K_s:
                    line.slow_line()
                if event.key == pygame.K_f:
                    line.fast_line()

            if event.type == pygame.MOUSEBUTTONDOWN:
                line.add_point()

        gameDisplay.fill((0, 0, 0))
        color_param = (color_param + 1) % 360
        color.hsla = (color_param, 100, 50, 100)
        line.draw_points()
        line.get_joint(steps).draw_points("line", 4, color)
        if not pause:
            line.set_points(line.speeds)
        if show_help:
            Game.display_help()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
    exit(0)
