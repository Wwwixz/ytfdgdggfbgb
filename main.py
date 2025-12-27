import arcade
import random

ok
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Epic Chess"

class Epic_Chess(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.player_x = 400
        self.player_y = 300
        self.player_size = 30
        self.player_hp = 100
        self.player_max_hp = 100

        self.monsters = [
            {"x": 200, "y": 300, "alive": True, "size": 25, "hp": 30, "attack_timer": 0},
            {"x": 600, "y": 300, "alive": True, "size": 25, "hp": 30, "attack_timer": 0},
            {"x": 400, "y": 100, "alive": True, "size": 25, "hp": 30, "attack_timer": 0},
            {"x": 400, "y": 500, "alive": True, "size": 25, "hp": 30, "attack_timer": 0},
        ]

        self.kills = 0
        self.frame_count = 0

        arcade.set_background_color(arcade.color.LIGHT_GRAY)

    def on_draw(self):
        self.clear()

        half = self.player_size / 2
        points = [
            (self.player_x - half, self.player_y - half),
            (self.player_x + half, self.player_y - half),
            (self.player_x + half, self.player_y + half),
            (self.player_x - half, self.player_y + half),
        ]
        arcade.draw_polygon_filled(points, arcade.color.GREEN)

        for monster in self.monsters:
            if monster["alive"]:
                half_size = monster["size"] / 2
                monster_points = [
                    (monster["x"] - half_size, monster["y"] - half_size),
                    (monster["x"] + half_size, monster["y"] - half_size),
                    (monster["x"] + half_size, monster["y"] + half_size),
                    (monster["x"] - half_size, monster["y"] + half_size),
                ]

                color = arcade.color.ORANGE if monster["attack_timer"] > 50 else arcade.color.RED
                arcade.draw_polygon_filled(monster_points, color)

                if monster["hp"] < 30:
                    hp_width = monster["size"] * (monster["hp"] / 30)
                    hp_points = [
                        (monster["x"] - monster["size"] / 2, monster["y"] + monster["size"] / 2 + 5),
                        (monster["x"] - monster["size"] / 2 + hp_width, monster["y"] + monster["size"] / 2 + 5),
                        (monster["x"] - monster["size"] / 2 + hp_width, monster["y"] + monster["size"] / 2 + 10),
                        (monster["x"] - monster["size"] / 2, monster["y"] + monster["size"] / 2 + 10),
                    ]
                    arcade.draw_polygon_filled(hp_points, arcade.color.GREEN)

        hp_width = 200 * (self.player_hp / self.player_max_hp)
        hp_points = [
            (20, SCREEN_HEIGHT - 40),
            (20 + hp_width, SCREEN_HEIGHT - 40),
            (20 + hp_width, SCREEN_HEIGHT - 20),
            (20, SCREEN_HEIGHT - 20),
        ]
        arcade.draw_polygon_filled(hp_points, arcade.color.RED)
        arcade.draw_polygon_outline(hp_points, arcade.color.BLACK, 2)

        arcade.draw_text(f"HP: {int(self.player_hp)}/{self.player_max_hp}", 20, SCREEN_HEIGHT - 60,
                         arcade.color.BLACK, 18)
        arcade.draw_text(f"Убито: {self.kills}/4", 20, SCREEN_HEIGHT - 90,
                         arcade.color.BLACK, 18)
        arcade.draw_text("Стрелки - двигаться", 20, SCREEN_HEIGHT - 120,
                         arcade.color.BLACK, 16)
        arcade.draw_text("Пробел - атаковать", 20, SCREEN_HEIGHT - 145,
                         arcade.color.BLACK, 16)
        arcade.draw_text("R - рестарт", 20, SCREEN_HEIGHT - 170,
                         arcade.color.BLACK, 16)

        if self.player_hp <= 0:
            text_bg_points = [
                (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 60),
                (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 - 60),
                (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 60),
                (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 + 60),
            ]
            arcade.draw_polygon_filled(text_bg_points, arcade.color.BLACK)
            arcade.draw_text("ВЫ ПРОИГРАЛИ!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20,
                             arcade.color.RED, 36, anchor_x="center")
            arcade.draw_text(f"Убито монстров: {self.kills}", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20,
                             arcade.color.WHITE, 24, anchor_x="center")
            arcade.draw_text("R - начать заново", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                             arcade.color.YELLOW, 20, anchor_x="center")

        elif self.kills == 4:
            text_bg_points = [
                (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50),
                (SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2 - 50),
                (SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2 + 50),
                (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 50),
            ]
            arcade.draw_polygon_filled(text_bg_points, arcade.color.BLACK)
            arcade.draw_text("ПОБЕДА!", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                             arcade.color.GOLD, 36, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if self.player_hp <= 0:
            if key == arcade.key.R:
                self.restart_game()
            return

        speed = 8

        if key == arcade.key.UP:
            self.player_y += speed
        elif key == arcade.key.DOWN:
            self.player_y -= speed
        elif key == arcade.key.LEFT:
            self.player_x -= speed
        elif key == arcade.key.RIGHT:
            self.player_x += speed

        elif key == arcade.key.SPACE:
            self.player_attack()

        elif key == arcade.key.R:
            self.restart_game()

        elif key == arcade.key.ESCAPE:
            arcade.close_window()

        self.player_x = max(self.player_size, min(SCREEN_WIDTH - self.player_size, self.player_x))
        self.player_y = max(self.player_size, min(SCREEN_HEIGHT - self.player_size, self.player_y))

    def player_attack(self):
        attack_range = 60

        for monster in self.monsters:
            if not monster["alive"]:
                continue

            distance_x = abs(self.player_x - monster["x"])
            distance_y = abs(self.player_y - monster["y"])

            if distance_x < attack_range and distance_y < attack_range:
                monster["hp"] -= 15
                if monster["hp"] <= 0:
                    monster["alive"] = False
                    self.kills += 1

    def update_monsters(self):
        for monster in self.monsters:
            if not monster["alive"]:
                continue

            if self.frame_count % random.randint(30, 60) == 0:
                if random.random() < 0.7:
                    dx = random.choice([-4, -3, -2, 2, 3, 4])
                    dy = random.choice([-4, -3, -2, 2, 3, 4])

                    monster["x"] += dx
                    monster["y"] += dy

            monster["x"] = max(monster["size"], min(SCREEN_WIDTH - monster["size"], monster["x"]))
            monster["y"] = max(monster["size"], min(SCREEN_HEIGHT - monster["size"], monster["y"]))

            if monster["attack_timer"] <= 0 and self.player_hp > 0:
                distance_x = abs(self.player_x - monster["x"])
                distance_y = abs(self.player_y - monster["y"])

                if distance_x < 50 and distance_y < 50:
                    self.player_hp -= 5
                    monster["attack_timer"] = 90

            if monster["attack_timer"] > 0:
                monster["attack_timer"] -= 1

    def on_update(self, delta_time):
        self.frame_count += 1

        if self.player_hp <= 0 or self.kills == 4:
            return

        self.update_monsters()


    def restart_game(self):
        self.player_x = 400
        self.player_y = 300
        self.player_hp = 100
        self.kills = 0
        self.frame_count = 0

        self.monsters = [
            {"x": 200, "y": 300, "alive": True, "size": 25, "hp": 30, "attack_timer": 0},
            {"x": 600, "y": 300, "alive": True, "size": 25, "hp": 30, "attack_timer": 0},
            {"x": 400, "y": 100, "alive": True, "size": 25, "hp": 30, "attack_timer": 0},
            {"x": 400, "y": 500, "alive": True, "size": 25, "hp": 30, "attack_timer": 0},
        ]

def main():
    game = Epic_Chess()
    arcade.run()

if __name__ == "__main__":

    main()
