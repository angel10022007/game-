import random
import tkinter as tk

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="black")
        self.canvas.pack()

        self.snake = [(200, 200), (180, 200), (160, 200)]  # 初始蛇段落在中央位置
        self.food = None
        self.bosses = []
        self.direction = 'Right'
        self.running = False
        self.score = 0
        self.level = 1
        self.speed = 200
        self.max_length = 20  # 設定一個蛇的最大長度以通關遊戲

        self.name = None  # 儲存玩家的名字
        self.entry = tk.Entry(self.root)
        self.entry.pack()
        self.entry.bind("<Return>", self.get_name)  # 綁定Enter鍵來獲取玩家名字

        self.bind_keys()
        self.show_intro()  # 顯示劇情介紹

    def bind_keys(self):
        self.root.bind("<Up>", lambda event: self.change_direction('Up'))
        self.root.bind("<Down>", lambda event: self.change_direction('Down'))
        self.root.bind("<Left>", lambda event: self.change_direction('Left'))
        self.root.bind("<Right>", lambda event: self.change_direction('Right'))

    def change_direction(self, new_direction):
        all_directions = {'Up': 'Down', 'Down': 'Up', 'Left': 'Right', 'Right': 'Left'}
        if new_direction != all_directions.get(self.direction):
            self.direction = new_direction

    def get_name(self, event):
        self.name = self.entry.get()
        self.entry.pack_forget()  # 隱藏輸入框
        self.show_story()

    def show_intro(self):
        intro_text = "請輸入你的名字並按Enter鍵開始"
        self.canvas.create_text(200, 200, text=intro_text, fill="white", font=("Arial", 16), tag="intro")

    def show_story(self):
        self.canvas.delete("intro")
        story_text = (
            f"很久以前，\n"
            f"在一個遙遠的森林裡，有一隻神奇的小蛇 {self.name}。\n"
            f"它個性勇敢，充滿冒險精神，總是勇於挑戰自己。\n\n"
            f"{self.name} 擁有敏捷的身手和冷靜的頭腦，\n"
            f"善於在危險中保持鎮定。\n"
            f"它的夢想是成為森林中的霸主，為此一直努力著。\n\n"
            f"{self.name} 的成長背景是如此的特別，\n"
            f"它在一個充滿挑戰的環境中長大，\n"
            f"每天都在學習如何躲避敵人，尋找食物。\n\n"
            f"遊戲目標：吃掉紅色食物，使自己變得更長。\n\n"
            f"操作方法：使用方向鍵移動。\n\n"
            f"第3關會出現1個Boss，\n"
            f"第5關會出現2個Boss，\n"
            f"避開它們！\n\n"
            f"按Enter鍵開始遊戲。\n"
        )
        # 將分行的文字分別顯示
        y_position = 50
        for line in story_text.split('\n'):
            self.canvas.create_text(200, y_position, text=line, fill="white", font=("Arial", 14), tag="story")
            y_position += 20

        self.root.bind("<Return>", self.start_game)  # 綁定Enter鍵開始遊戲

    def start_game(self, event=None):
        self.running = True
        self.canvas.delete("story")
        self.create_snake()
        self.create_food()
        self.move_snake()

    def create_snake(self):
        for segment in self.snake:
            self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="green", tag="snake")

    def move_snake(self):
        if self.running:
            head_x, head_y = self.snake[0]
            if self.direction == 'Up':
                head_y -= 20
            elif self.direction == 'Down':
                head_y += 20
            elif self.direction == 'Left':
                head_x -= 20
            elif self.direction == 'Right':
                head_x += 20

            new_head = (head_x, head_y)

            # Check for collisions with wall, itself, or bosses
            if (new_head in self.snake or
                not (0 <= head_x < 400 and 0 <= head_y < 400) or
                any(new_head in boss for boss in self.bosses)):
                self.game_over()
                return

            # Move the snake
            self.snake = [new_head] + self.snake[:-1]

            # Check if food is eaten
            if self.snake[0] == self.food:
                self.snake.append(self.snake[-1])
                self.canvas.delete("food")
                self.create_food()
                self.score += 10

                if len(self.snake) >= self.max_length:
                    self.you_win()
                    return

                if self.score % 50 == 0:
                    self.level_up()

            self.redraw_snake()
            self.move_bosses()  # 移動Boss
            self.root.after(self.speed, self.move_snake)

    def create_food(self):
        while True:
            x = random.randint(0, 19) * 20
            y = random.randint(0, 19) * 20
            if (x, y) not in self.snake and not any((x, y) in boss for boss in self.bosses):
                break
        self.food = (x, y)
        self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="red", tag="food")

    def create_boss(self, number_of_bosses):
        self.bosses = []
        for _ in range(number_of_bosses):
            while True:
                x = random.randint(0, 19) * 20
                y = random.randint(0, 19) * 20
                if (x, y) not in self.snake and (x, y) != self.food:
                    boss_position = [(x, y)]
                    self.bosses.append(boss_position)
                    break
        self.redraw_bosses()

    def move_bosses(self):
        if self.bosses:
            self.canvas.delete("boss")
            for boss in self.bosses:
                direction = random.choice(['Up', 'Down', 'Left', 'Right'])
                head_x, head_y = boss[0]
                if direction == 'Up':
                    head_y -= 20
                elif direction == 'Down':
                    head_y += 20
                elif direction == 'Left':
                    head_x -= 20
                elif direction == 'Right':
                    head_x += 20

                if 0 <= head_x < 400 and 0 <= head_y < 400:
                    boss[0] = (head_x, head_y)
            self.redraw_bosses()

    def redraw_bosses(self):
        for boss in self.bosses:
            for segment in boss:
                self.canvas.create_rectangle(segment[0], segment[1], segment[0] + 20, segment[1] + 20, fill="blue", tag="boss")

    def redraw_snake(self):
        self.canvas.delete("snake")
        self.create_snake()

    def level_up(self):
        self.level += 1
        self.speed = max(50, self.speed - 20)  # 每次提升一級速度增快，但最低為50ms
        self.canvas.delete("levelup")
        self.canvas.create_text(200, 20, text=f"Level {self.level}", fill="white", font=("Arial", 16), tag="levelup")

        if self.level == 3:
            self.create_boss(1)
        elif self.level == 5:
            self.create_boss(2)
        elif self.level == 10:
            self.you_win()

    def game_over(self):
        self.running = False
        self.canvas.create_text(200, 200, text="Game Over", fill="white", font=("Arial", 24))
        self.canvas.create_text(200, 230, text=f"Score: {self.score}", fill="white", font=("Arial", 16))
        self.root.unbind("<Return>")  # 避免重新開始遊戲

    def you_win(self):
        self.running = False
        self.canvas.create_text(200, 200, text="You Win!", fill="white", font=("Arial", 24))
        self.canvas.create_text(200, 230, text=f"Final Score: {self.score}", fill="white", font=("Arial", 16))
        self.root.unbind("<Return>")  # 避免重新開始遊戲

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
