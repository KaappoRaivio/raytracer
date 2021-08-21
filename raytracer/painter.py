import pygame

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

    def set(self, x, y, color):
        self.window.fill(color, pygame.Rect(x * self.scale, y * self.scale, self.scale, self.scale))

    def update(self):
        pygame.display.flip()


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__in_context_manager = False
        pygame.quit()


if __name__ == "__main__":
    with Painter(80, 60, 10) as painter:
        painter.set(1, 1, (255, 0, 0))
        painter.update()
        input()
