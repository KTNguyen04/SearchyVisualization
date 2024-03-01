

BLACK_C = (0, 0, 0)
WHITE_C = (255, 255, 255)
GRAY_C = (128, 128, 128)
GREEN_C = (0, 255, 0)
RED_C = (255, 0, 0)
YELLOW_C = (255, 255, 0)

BLOCKED_COLOR = BLACK_C
UNBLOCKED_COLOR = WHITE_C
START_COLOR = GREEN_C
GOAL_COLOR = RED_C
BACK_GR = WHITE_C
BUTTON_COLOR = (255, 102, 102)
BUTTON_DOWN_COLOR = (154, 15, 15)
SHADE_COLOR = BLACK_C

EXPAND_COLOR = YELLOW_C
REACHED_COLOR = (255, 153, 51)
SELECTED_COLOR = (102, 0, 204)
PATH_COLOR = (76, 0, 153)

FINISHED_COLOR = (255, 0, 127)


class Settings:
    def __init__(self):
        pass
    window_width = 800
    window_height = 800
    screen_width = 1200
    screen_height = 900

    top_bot_margin = int((screen_height - window_height)/2)
    left_margin = top_bot_margin

    window_topleft = (left_margin, top_bot_margin)
    n_rows = 50
    n_cols = n_rows

    cell_height = int(window_height/n_rows)
    cell_width = int(window_width/n_cols)

    button_width = 200
    button_height = 40
    button_shade = 5

    dashboard_width = screen_width - window_width - left_margin
    dashboard_height = window_height
    dashboard_topleft = (window_width + left_margin, top_bot_margin)
    spacing = 20
    max_goal = -1
    max_start = 1
    max_blocked = -1

    num_goal = 0
    num_start = 0
    num_blocked = 0
