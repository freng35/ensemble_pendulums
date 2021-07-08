from math import sqrt, cos, pi

g = 9.80665


class Pendulums:

    def __init__(self, canvas, params):
        self.CANVAS = canvas
        self.CANVAS_WIDTH = canvas.winfo_reqwidth()
        self.CANVAS_HEIGHT = canvas.winfo_reqheight()

        self.number_of_pendulums = None
        self.amplitude = None
        self.start_nu = None
        self.delta_nu = None
        self.size = None

        self.delta_type_nu = 1

        # time cannot be updated in params_update
        self.time = params['time']
        self.array_of_circles = []

        self.set_params(params)

        self.is_running = False
        self.__draw__()
        self.__loop__()

    def set_params(self, params):
        updated_nu = sqrt(g / float(params['length']))

        self.number_of_pendulums = int(params['number_of_pendulums'])
        self.amplitude = float(params['amplitude'])
        self.start_nu = float(updated_nu)
        self.delta_nu = float(params['delta_nu'])
        self.size = int(params['size'])
        self.time = float(params['time'])
        self.start_lenght = float(params['length'])

        # as number of pendulums may change, first - delete all existing, then create new
        for circle in self.array_of_circles:
            self.CANVAS.delete(circle)
        self.array_of_circles.clear()

        for i in range(self.number_of_pendulums):
            pend_coords = self.__get_coords__(i)
            pend = self.CANVAS.create_oval(pend_coords[0] + self.size, pend_coords[1] + self.size,
                                           pend_coords[0] - self.size, pend_coords[1] - self.size, fill="#fff")
            self.array_of_circles.append(pend)

        self.start_loop()

    def __draw__(self):
        for i, circle in enumerate(self.array_of_circles):
            coords = self.__get_coords__(i)
            self.CANVAS.coords(circle, coords[0] + self.size, coords[1] + self.size,
                               coords[0] - self.size, coords[1] - self.size)

    def __get_coords__(self, i):
        # current_length = g / (4 * (pi ** 2) * ((self.start_nu + i * self.delta_nu) ** 2))
        # current_omega = sqrt(g / current_length)

        current_omega = self.start_nu + i * self.delta_nu

        if not self.delta_type_nu:
            current_len = self.start_lenght + i * self.delta_nu
            current_omega = sqrt(g / current_len)

        x = self.CANVAS_WIDTH / (self.number_of_pendulums + 1) * (i + 1)
        y = self.CANVAS_HEIGHT / 2 + self.amplitude * cos(current_omega * self.time)

        coords = (x, y)
        return coords

    def __loop__(self):
        self.CANVAS.after(30, self.__loop__)
        self.__draw__()
        if self.is_running:
            self.time += 0.03

    def start_loop(self):
        self.is_running = True

    def stop_loop(self):
        self.is_running = False
