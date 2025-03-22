import pyxel


SCREEN_WIDTH = 160
SCREEN_HEIGHT = 120
STONE_INTERVAL = 15
STONE_INTERVAL_GRADE = 1
STONE_NUMS = 1

POWER_STAR_INTERVAL = 75
POWER_STAR_TIME = 75

GAME_OVER_DISPLAY_TIMER = 60
START_SCENE = "start"
PLAY_SCENE = "play"

SCORE_RATE = 30
LEVEL_UP_RATE = 150
GRADE_UP_RATE = 300


class Stone:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        if self.y < SCREEN_HEIGHT:
            self.y += 1

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 8, pyxel.COLOR_BLACK)


class PowerStar:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        if self.y < SCREEN_HEIGHT:
            self.y += 1

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 8, 8, 8, pyxel.COLOR_BLACK)


class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="レトロゲーム")
        pyxel.mouse(True)
        pyxel.load("my_resource.pyxres")
        self.jp_font = pyxel.Font("umplus_j10r.bdf")
        pyxel.playm(1, loop=True)
        self.current_scene = START_SCENE
        pyxel.run(self.update, self.draw)

    def reset_play_scene(self):
        pyxel.playm(0, loop=True)
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT // 5 * 4
        self.stones = []
        self.power_stars = []
        self.score = 0
        self.current_frame = 1
        self.stone_nums = STONE_NUMS
        self.stone_interval_grade = STONE_INTERVAL_GRADE
        self.is_collision = False
        self.is_power_star = False
        self.game_over_display_timer = GAME_OVER_DISPLAY_TIMER

    def update_start_scene(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.reset_play_scene()
            self.current_scene = PLAY_SCENE

    def update_play_scene(self):
        # ゲームオーバー時の処理
        if self.is_collision:
            if self.game_over_display_timer > 0:
                self.game_over_display_timer -= 1
            else:
                pyxel.playm(1, loop=True)
                self.current_scene = START_SCENE
            return
        else:
            # スコア更新
            if self.current_frame % SCORE_RATE == 0:
                self.score += 1

        # パワーアップ時の処理
        if self.is_power_star:
            if self.power_star_timer > 0:
                self.power_star_timer -= 1
            else:
                self.is_power_star = False

        # プレイヤの移動
        if (pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT)) and self.player_x < SCREEN_WIDTH - 14:
            self.player_x += 1
        elif (pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT)) and self.player_x > -2:
            self.player_x -= 1

        # 石を追加
        if self.current_frame % STONE_INTERVAL == 0:
            for _ in range(self.stone_nums):
                self.stones.append(Stone(pyxel.rndi(0, SCREEN_WIDTH - 8), 0))
            if self.current_frame % GRADE_UP_RATE == 0:
                self.stone_nums += 1
                self.stone_interval_grade += 1

        # パワーアップアイテムを追加
        if self.current_frame % POWER_STAR_INTERVAL == 0:
            self.power_stars.append(PowerStar(pyxel.rndi(0, SCREEN_WIDTH - 16), 0))

        # 石の落下
        for stone in self.stones.copy():
            stone.update()

            # 石とプレイヤの衝突判定
            if (self.player_x <= stone.x <= self.player_x + 8 and
                self.player_y <= stone.y <= self.player_y + 8) and not self.is_power_star:
                self.is_collision = True

            # 画面外に出たら石を削除
            if stone.y > SCREEN_HEIGHT:
                self.stones.remove(stone)

        # パワーアップアイテムの落下
        for power_star in self.power_stars.copy():
            power_star.update()

            # パワーアップアイテムとプレイヤの衝突判定
            if (self.player_x <= power_star.x <= self.player_x + 16 and
                self.player_y <= power_star.y <= self.player_y + 16):
                self.power_stars.remove(power_star)
                self.is_power_star = True
                self.power_star_timer = POWER_STAR_TIME

            # 画面外に出たらパワーアップアイテムを削除
            if power_star.y > SCREEN_HEIGHT:
                self.power_stars.remove(power_star)

        self.current_frame += 1

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if self.current_scene == PLAY_SCENE:
            self.update_play_scene()
        elif self.current_scene == START_SCENE:
            self.update_start_scene()

    def draw_start_scene(self):
        pyxel.blt(0, 0, 0, 32, 0, 160, 120)
        pyxel.text(SCREEN_WIDTH // 12, SCREEN_HEIGHT // 12, "ver.0.0.3", pyxel.COLOR_WHITE, self.jp_font)
        pyxel.text(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, "おちる岩をよけろ！", pyxel.COLOR_RED, self.jp_font)
        pyxel.text(SCREEN_WIDTH // 12, SCREEN_HEIGHT // 5 * 3, "クリック/タッチ してスタート", pyxel.COLOR_RED, self.jp_font)

    def draw_play_scene(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE)

        # 石
        for stone in self.stones:
            stone.draw()

        # パワーアップアイテム
        for power_star in self.power_stars:
            power_star.draw()

        # プレイヤ
        if not self.is_power_star:
            pyxel.blt(self.player_x, self.player_y, 0, 16, 0, 16, 16, pyxel.COLOR_BLACK)
        else:
            pyxel.blt(self.player_x, self.player_y, 0, 16, 16, 16, 16, pyxel.COLOR_BLACK)

        # 石とプレイヤの衝突判定
        if self.is_collision:
            pyxel.text(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2, "GAME OVER", pyxel.COLOR_YELLOW)

        # スコア表示
        pyxel.text(0, SCREEN_HEIGHT // 12, f"スコア: {self.score}(グレード: {self.stone_interval_grade})", pyxel.COLOR_WHITE, self.jp_font)

    def draw(self):
        if self.current_scene == START_SCENE:
            self.draw_start_scene()
        elif self.current_scene == PLAY_SCENE:
            self.draw_play_scene()

App()
