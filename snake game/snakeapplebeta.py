import pygame
import random
from collections import deque
import heapq

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 631, 480
GRID_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE
UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

NORMAL = 50

class Wompwomp:
    def __init__(self):
        pygame.init()  # Initialize pygame
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("womp womp game")
        self.clock = pygame.time.Clock()
        self.speed = NORMAL  # Always use the NORMAL difficulty
        self.set_game_icon()  # Set the game icon here

        # Load snake head and apple images and resize them
        self.snake_head_img = pygame.image.load('snake_head.png')
        self.snake_head_img = pygame.transform.scale(self.snake_head_img, (GRID_SIZE, GRID_SIZE))

        self.snake_head_dead_img = pygame.image.load('snake_head_dead.png')
        self.snake_head_dead_img = pygame.transform.scale(self.snake_head_dead_img, (GRID_SIZE, GRID_SIZE))

        self.apple_img = pygame.image.load('apple.png')
        self.apple_img = pygame.transform.scale(self.apple_img, (GRID_SIZE, GRID_SIZE))

        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.apple = self.spawn_apple()
        self.game_over = False
        self.is_start_screen = True

        # Create the "Play Again" button
        self.play_again_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 30, 200, 50)

        # Create the "Start" button
        self.start_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50)
        self.start_button_color = (0, 255, 0)  # Green color for the button

        self.score = 0
        self.high_score = self.load_high_score()
        self.font = pygame.font.Font(None, 36)

    def set_game_icon(self):
        # Load the icon image and resize it (adjust the path as needed)
        icon_img = pygame.image.load('icon.png')  # Replace 'icon.png' with the path to your icon image
        icon_img = pygame.transform.scale(icon_img, (32, 32))  # Adjust the size as needed

        # Set the game icon
        pygame.display.set_icon(icon_img)

    def spawn_apple(self):
        while True:
            x, y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                return x, y

    def load_high_score(self):
        try:
            with open("highscore.txt", "r") as file:
                high_score = int(file.read())
        except FileNotFoundError:
            high_score = 0
        return high_score

    def save_high_score(self):
        with open("highscore.txt", "w") as file:
            file.write(str(self.high_score))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_over:
                    # Check if the "Play Again" button is clicked
                    if self.play_again_button.collidepoint(event.pos):
                        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
                        self.direction = RIGHT
                        self.apple = self.spawn_apple()
                        self.score = 0
                        self.game_over = False
                elif self.is_start_screen:
                    # Check if the "Start" button is clicked
                    if self.start_button.collidepoint(event.pos):
                        self.is_start_screen = False

    def move_snake(self):
        if self.game_over or self.is_start_screen:
            return

        head_x, head_y = self.snake[-1]
        if self.direction == UP:
            new_head = (head_x, head_y - 1)
        elif self.direction == DOWN:
            new_head = (head_x, head_y + 1)
        elif self.direction == LEFT:
            new_head = (head_x - 1, head_y)
        else:
            new_head = (head_x + 1, head_y)

        # Check if the new head position collides with any part of the snake's body
        if new_head in self.snake:
            self.game_over = True
            return

        # Wraparound if the new head position is outside the grid
        new_head_x = new_head[0] % GRID_WIDTH
        new_head_y = new_head[1] % GRID_HEIGHT
        new_head = (new_head_x, new_head_y)

        if new_head == self.apple:
            self.snake.append(new_head)
            self.apple = self.spawn_apple()
            self.score += 1
        else:
            self.snake.append(new_head)
            self.snake.pop(0)

    def draw(self):
        self.screen.fill((40, 40, 40))

        if not self.is_start_screen:
            # Draw the background grid lines
            for x in range(0, SCREEN_WIDTH, GRID_SIZE):
                pygame.draw.line(self.screen, (255, 255, 255), (x, 0), (x, SCREEN_HEIGHT))
            for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
                pygame.draw.line(self.screen, (255, 255, 255), (0, y), (SCREEN_WIDTH, y))

        if self.is_start_screen:
            # Draw "Start" button
            pygame.draw.rect(self.screen, self.start_button_color, self.start_button)
            start_text = self.font.render("Start", True, (0, 0, 0))
            self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
        elif self.game_over:
            # Draw the dead snake body
            for segment in self.snake[:-1]:
                pygame.draw.rect(self.screen, (128, 128, 128), (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            # Draw the snake head
            self.screen.blit(self.snake_head_dead_img, (self.snake[-1][0] * GRID_SIZE, self.snake[-1][1] * GRID_SIZE))

            game_over_text = self.font.render("Game Over", True, (255, 0, 0))
            self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))

            # Draw the "Play Again" button
            pygame.draw.rect(self.screen, (255, 0, 0), self.play_again_button)
            play_again_text = self.font.render("Play Again", True, (255, 255, 255))
            self.screen.blit(play_again_text, (SCREEN_WIDTH // 2 - play_again_text.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
        else:
            # Draw the snake body
            for segment in self.snake[:-1]:
                pygame.draw.rect(self.screen, (0, 255, 0), (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

            # Draw the snake head
            self.screen.blit(self.snake_head_img, (self.snake[-1][0] * GRID_SIZE, self.snake[-1][1] * GRID_SIZE))

            # Draw the apple
            self.screen.blit(self.apple_img, (self.apple[0] * GRID_SIZE, self.apple[1] * GRID_SIZE))

            # Draw the scoreboard
            score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_text, (10, 10))  # Display the score at the top-left corner

            # Draw the high score
            high_score_text = self.font.render(f"High Score: {self.high_score}", True, (255, 255, 255))
            self.screen.blit(high_score_text, (10, 40))  # Display the high score below the score

        pygame.display.update()

    def run(self):
        while True:
            self.handle_events()
            if not self.is_start_screen and not self.game_over:
                self.move_towards_apple()

            self.move_snake()
            self.draw()
            self.clock.tick(self.speed)  # Adjust speed based on the difficulty

            if self.game_over:
                self.check_high_score()  # Check and save high score if needed

    def heuristic(self, x, y):
        # A* heuristic function (Manhattan distance to the apple)
        apple_x, apple_y = self.apple
        return abs(x - apple_x) + abs(y - apple_y)

    def move_towards_apple(self):
        head_x, head_y = self.snake[-1]

        # Initialize the grid with the correct dimensions
        grid = [[1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        # Mark snake's body as unwalkable in the grid
        for segment in self.snake[:-1]:
            x, y = segment
            if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:  # Check if within valid grid bounds
                grid[y][x] = 0

        def is_valid_move(x, y):
            return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and grid[y][x] == 1

        # Perform A* to find the shortest path to the apple
        queue = [(self.heuristic(head_x, head_y), head_x, head_y, [])]
        heapq.heapify(queue)
        visited = set()

        while queue:
            _, x, y, path = heapq.heappop(queue)
            if (x, y) == self.apple:
                # Found the apple, set the direction towards it
                next_x, next_y = path[0]
                if next_x < head_x:
                    self.direction = LEFT
                elif next_x > head_x:
                    self.direction = RIGHT
                elif next_y < head_y:
                    self.direction = UP
                else:
                    self.direction = DOWN
                break

            if (x, y) not in visited:
                visited.add((x, y))
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_x, new_y = x + dx, y + dy
                    if is_valid_move(new_x, new_y):
                        new_path = path + [(new_x, new_y)]
                        heapq.heappush(queue, (len(new_path) + self.heuristic(new_x, new_y), new_x, new_y, new_path))

    def check_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

if __name__ == "__main__":
    game = Wompwomp()
    game.run()
