
import pygame
import sys
from grid import Grid
from settings import BACK_GR, BUTTON_DOWN_COLOR, Settings
from button import Button
from algo import Algo


class SearchingVisualization:
    def __init__(self):
        self.screen = pygame.display.set_mode(
            (Settings.screen_width, Settings.screen_height))
        self.screen_rect = self.screen.get_rect()
        pygame.init()
        self.window = pygame.Rect(
            Settings.left_margin,  Settings.top_bot_margin, Settings.window_width, Settings.window_height)

        self.dashboard_rect = pygame.Rect(
            Settings.dashboard_topleft, (Settings.dashboard_width, Settings.dashboard_height))

        self.clock = pygame.time.Clock()
        self.grid = Grid(self)

        self.block_button = Button(self, "Block")
        self.start_button = Button(self, "Start")
        self.goal_button = Button(self, "Goal")

        self.buttons = [self.block_button, self.start_button, self.goal_button]
        self.align_buttons()

        self.cell_flags = [
            False,
            False,
            False,

        ]  # block, start,end
        self.start = None
        self.goals = []

        self.algo = Algo()

    def run(self):
        while True:
            self.check_events()
            self.update_data()
            self.update_buttons()
            self.update_screen()

    def update_screen(self):
        self.screen.fill(BACK_GR)
        self.grid.draw()
        for button in self.buttons:
            button.draw()
        pygame.display.flip()
        self.clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.algo.run(lambda: self.grid.draw())
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.check_buttons(pos)
            if event.type == pygame.MOUSEBUTTONUP:
                pass
            if pygame.mouse.get_pressed()[0]:
                self.check_left_press(pos)
            if pygame.mouse.get_pressed()[2]:
                self.check_right_press(pos)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def check_mouse_down(self):
        pass

    def check_left_press(self, pos):
        for row in self.grid.cells:
            for cell in row:
                if not self.grid.check_barrier(cell.pos):
                    if cell.get_rect().collidepoint(pos):
                        for i, flag in enumerate(self.cell_flags):
                            if flag == True:
                                if i == 0:
                                    cell.blocked()
                                    Settings.num_blocked += 1
                                elif i == 1:
                                    if Settings.num_start < 1:
                                        cell.make_start()
                                        Settings.num_start += 1

                                elif i == 2:
                                    cell.make_goal()
                                    Settings.num_goal += 1

    def check_right_press(self, pos):
        for row in self.grid.cells:
            for cell in row:
                if not self.grid.check_barrier(cell.pos):
                    if cell.get_rect().collidepoint(pos):
                        if cell.is_start():
                            Settings.num_start -= 1
                        elif cell.is_goal():
                            Settings().num_goal -= 1
                        elif cell.is_blocked():
                            Settings().num_blocked -= 1
                        cell.unblocked()

    def align_buttons(self):
        for i, button in enumerate(self.buttons):
            button.top_rect.midtop = (self.dashboard_rect.midtop[0], self.dashboard_rect.midtop[1] +
                                      i * (button.height + Settings.spacing))

            button.bot_rect.midtop = (self.dashboard_rect.midtop[0], self.dashboard_rect.midtop[1] +
                                      i * (button.height + Settings.spacing))

            button.text_rect.center = button.top_rect.center

    def check_buttons(self, pos):
        for i, button in enumerate(self.buttons):
            if button.top_rect.collidepoint(pos):
                if all(flag == False for flag in self.cell_flags):
                    self.cell_flags[i] ^= True
                    break
                else:
                    if self.cell_flags[i]:
                        self.cell_flags[i] = False
                        break
                    else:
                        self.cell_flags = [False]*len(self.cell_flags)
                        self.cell_flags[i] = True
                        break

    def update_buttons(self):
        for i, button in enumerate(self.buttons):
            if self.cell_flags[i]:
                button.clicked()
            else:
                button.unclicked()

    def detect_cells(self):
        for row in self.grid.cells:
            for cell in row:
                if cell.is_start():
                    self.start = cell
                elif cell.is_goal():
                    if cell not in self.goals:
                        self.goals.append(cell)

    def update_search_data(self):
        self.algo.start = self.start
        self.algo.goals = self.goals
        self.algo.matrix = self.grid.cells

    def update_data(self):
        self.detect_cells()
        self.update_search_data()


if __name__ == "__main__":
    sv = SearchingVisualization()
    sv.run()
