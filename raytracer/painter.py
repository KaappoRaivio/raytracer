import pygame

from visual import Color


def clamp(value, minimum, maximum):
    return max(min(value, maximum), minimum)

class Painter:
    def __init__(self, width, height, scale):
        self.width = width
        self.height = height
        self.scale = scale

        self.__in_context_manager = False


    def __enter__(self):
        self.__in_context_manager = True
        self.window = pygame.display.set_mode((self.width * self.scale, self.height * self.scale))
        self.window.fill((255, 255, 255))
        return self

    def set(self, x, y, color: Color):
        result = self.to_24_bit_rgb(color)

        #
        # color = color.inv_gamma(2)
        # luma = abs(color)
        # saturation = 1.0
        # for channel in color:
        #     divisor = max((luma - channel), 0.0001)
        #     if channel > 1:
        #         saturation = min(saturation, (luma - 1) / divisor)
        #     elif channel < 0:
        #         saturation = min(saturation, luma / divisor)
        # saturation = clamp(saturation, 0, 1)
        # result = color.map(lambda n: clamp((n - luma) * saturation + luma, 0, 1) * (256 - 1e-5))


        self.window.fill((*result,), pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale))

    def to_24_bit_rgb(self, color):
        result = map(lambda x: int(min(x * 256, 255)), color.inv_gamma(2))
        return list(result)

    def fill(self, pixels, width):
        for index, pixel in enumerate(pixels):
            x = index % width
            y = index // width
            self.set(x, y, pixel)
        # for y, row in enumerate(pixels):
        #     for x, pixel in enumerate(row):
        #         self.set(x, y, pixel)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        pygame.display.flip()

    def wait(self, callback=lambda x: x):
        while True:
            # print("waiting")
            try:
                event = pygame.event.wait(1000)
            except KeyboardInterrupt:
                pygame.quit()
                exit()
            # for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            else:
                if callback(event):
                    # self.update()
                    return



    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__in_context_manager = False
        pygame.quit()


if __name__ == "__main__":
    with Painter(80, 60, 10) as painter:
        painter.set(1, 1, (255, 0, 0))
        painter.update()
        input()
