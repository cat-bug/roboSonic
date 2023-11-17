import pygame
import random

class RoboSonic:
    def __init__(self):
        pygame.init()
        
        self.load_images()
        self.new_game()
        self.game_over = False
        self.points_done = 5
        
        self.height = len(self.map)
        self.width = len(self.map[0])
        self.scale = self.images[0].get_width()

        window_height = self.scale * self.height
        window_width = self.scale * self.width
        self.window = pygame.display.set_mode((window_width, window_height + self.scale))
        
        self.game_font = pygame.font.SysFont("Arial", 24)
        self.set_rings_and_holes()
        pygame.display.set_caption("RoboSonic")

        self.main_loop()

    def load_images(self):
        self.images = []
        for name in ["floor", "wall", "target", "box", "robot", "done", "target_robot"]:
            self.images.append(pygame.image.load(name + ".png"))

    def set_rings_and_holes(self):
            for _ in range(self.points_done):
                roboty, robotx = self.find_robot()
                x = random.randint(0, self.width-1)
                y = random.randint(0, self.height-1)
                if x == robotx and y == roboty:
                    y -= 1
                self.map[y][x] = 2
                xh = random.randint(0, self.width-1)
                yh = random.randint(0, self.height-1)
                if (xh == x and yh == y) or (xh == robotx and yh == roboty):
                    continue
                self.map[yh][xh] = 1
                
                
    def new_game(self):
        

        self.map = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        self.points = 0

    def main_loop(self):
        #keep adding executions going next level 
        while True:
            self.check_events()
            self.draw_window()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move(0, -1)
                if event.key == pygame.K_RIGHT:
                    self.move(0, 1)
                if event.key == pygame.K_UP:
                    self.move(-1, 0)
                if event.key == pygame.K_DOWN:
                    self.move(1, 0)
                if event.key == pygame.K_F2:
                    self.new_game()
                    self.game_over = False
                    self.set_rings_and_holes()
                if event.key == pygame.K_ESCAPE:
                    exit()

            if event.type == pygame.QUIT:
                exit()

    def move(self, move_y, move_x):
        if self.game_over or self.game_solved():
            return
        robot_old_y, robot_old_x = self.find_robot() 
        robot_new_y = robot_old_y + move_y
        robot_new_x = robot_old_x + move_x
        if robot_new_y > self.height-1 or robot_new_x > self.width-1 or robot_new_y < 0 or robot_new_x < 0:
            return
        if self.map[robot_new_y][robot_new_x] == 2:
            self.points += 1
            self.map[robot_old_y][robot_old_x] = 0
            self.map[robot_new_y][robot_new_x] = 4
            return
        if self.map[robot_new_y][robot_new_x] == 1:
            self.game_over = True 

        self.map[robot_old_y][robot_old_x] -= 4
        self.map[robot_new_y][robot_new_x] += 4


        
   
    def find_robot(self ):
        for y in range(self.height):
            for x in range(self.width):
                if self.map[y][x] == 4:
                    return (y, x)

    def draw_window(self):
        self.window.fill((0, 0, 0))

        for y in range(self.height):
            for x in range(self.width):
                square = self.map[y][x]
                self.window.blit(self.images[square], (x * self.scale, y * self.scale))

        game_text = self.game_font.render("Points: " + str(self.points), True, (255, 0, 0))
        self.window.blit(game_text, (25, self.height * self.scale + 10))

        game_text = self.game_font.render("F2 = new game", True, (255, 0, 0))
        self.window.blit(game_text, (200, self.height * self.scale + 10))

        game_text = self.game_font.render("Esc = exit game", True, (255, 0, 0))
        self.window.blit(game_text, (400, self.height * self.scale + 10))

        if self.game_solved():
            game_text = self.game_font.render("Congratulations, you solved the game!", True, (255, 0, 0))
            game_text_x = self.scale * self.width / 2 - game_text.get_width() / 2
            game_text_y = self.scale * self.height / 2 - game_text.get_height() / 2
            pygame.draw.rect(self.window, (0, 0, 0), (game_text_x, game_text_y, game_text.get_width(), game_text.get_height()))
            self.window.blit(game_text, (game_text_x, game_text_y))
        if self.game_over:
            game_text = self.game_font.render("It is over, you fall in the hooooleee :(", True, (255, 0, 0))
            game_text_x = self.scale * self.width / 2 - game_text.get_width() / 2
            game_text_y = self.scale * self.height / 2 - game_text.get_height() / 2
            pygame.draw.rect(self.window, (0, 0, 0), (game_text_x, game_text_y, game_text.get_width(), game_text.get_height()))
            self.window.blit(game_text, (game_text_x, game_text_y))

        pygame.display.flip()

    def game_solved(self):
        if self.points < self.points_done:
            return False
        return True

if __name__ == "__main__":
    RoboSonic()