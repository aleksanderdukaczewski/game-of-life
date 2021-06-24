import pygame as pg
from grid import Grid
pg.init()

# Global colors
BACKGROUND_COLOR = (30, 30, 30)
WHITE = (255,255,255)
BLACK = (0,0,0)

# Fonts
inputfield_font = pg.font.Font(None, 32)
button_font = pg.font.Font(None, 60)

# Clock
clock = pg.time.Clock()
FPS = 60

def welcome_menu():
    WIDTH, HEIGHT = 640, 480
    WIN = pg.display.set_mode((WIDTH, HEIGHT)) # Create a surface for the window.
    
    # Local colors for the input fields.
    color_inactive = pg.Color('lightskyblue3')
    color_active = pg.Color('dodgerblue2')

    # Define the input field for the number of horizontal cells.
    cellsx_label = inputfield_font.render("HORIZONTAL CELLS", True, WHITE)
    cellsx_box = pg.Rect((WIDTH - 100)//2, (HEIGHT - 42)//2 - 90, 100 ,32)
    cellsx_color = color_inactive
    cellsx_text = "20"
    cellsx_active = False

    # Define the input field for the number of vertical cells.
    cellsy_label = inputfield_font.render("VERTICAL CELLS", True, WHITE)
    cellsy_box = pg.Rect(cellsx_box.x, cellsx_box.y + 90, 100 ,32)
    cellsy_color = color_inactive
    cellsy_text = "20"
    cellsy_active = False

    # Define the input field for the size of the cell.
    cellsize_label = inputfield_font.render("CELLSIZE", True, WHITE)
    cellsize_box = pg.Rect(cellsy_box.x, cellsy_box.y + 90, 100 ,32)
    cellsize_color = color_inactive
    cellsize_text = "15"
    cellsize_active = False

    # Define the "NEXT" button.
    nextbutton_label = button_font.render("NEXT", True, WHITE)
    nextbutton_box = pg.Rect(cellsize_box.x - 45, cellsize_box.y + 55, nextbutton_label.get_width() + 10, nextbutton_label.get_height() + 10)

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                done = True
                pg.quit()
            if event.type == pg.MOUSEBUTTONDOWN: # Check for mouse clicks on the fields.
                if cellsx_box.collidepoint(event.pos):
                    cellsx_active = not cellsx_active
                    cellsy_active, cellsize_active = False, False
                elif cellsy_box.collidepoint(event.pos):
                    cellsy_active = not cellsy_active
                    cellsx_active, cellsize_active = False, False
                elif cellsize_box.collidepoint(event.pos):
                    cellsize_active = not cellsize_active
                    cellsx_active, cellsy_active = False, False
                elif nextbutton_box.collidepoint(event.pos):
                    try:
                        return (int(cellsx_text), int(cellsy_text), int(cellsize_text))
                    except ValueError:
                        print("MUST ENTER VALID INTEGER VALUES IN ALL FIELDS")
                        quit()
                else:
                    cellsx_active, cellsy_active, cellsize_active = False, False, False

            cellsx_color = color_active if cellsx_active else color_inactive
            cellsy_color = color_active if cellsy_active else color_inactive
            cellsize_color = color_active if cellsize_active else color_inactive

            if event.type == pg.KEYDOWN:
                if cellsx_active:
                    if event.key == pg.K_BACKSPACE:
                        cellsx_text = cellsx_text[:-1]
                    else:
                        cellsx_text += event.unicode
                elif cellsy_active:
                    if event.key == pg.K_BACKSPACE:
                        cellsy_text = cellsy_text[:-1]
                    else:
                        cellsy_text += event.unicode
                elif cellsize_active:
                    if event.key == pg.K_BACKSPACE:
                        cellsize_text = cellsize_text[:-1]
                    else:
                        cellsize_text += event.unicode

        WIN.fill(BACKGROUND_COLOR)

        # Render the current text.
        cellsx_surface = inputfield_font.render(cellsx_text, True, cellsx_color)
        cellsy_surface = inputfield_font.render(cellsy_text, True, cellsy_color)
        cellsize_surface = inputfield_font.render(cellsize_text, True, cellsize_color)

        # Resize the box if the text is too long.
        cellsx_width = max(32, cellsx_surface.get_width()+10)
        cellsx_box.w = cellsx_width
        cellsy_width = max(32, cellsy_surface.get_width()+10)
        cellsy_box.w = cellsy_width
        cellsize_width = max(32, cellsize_surface.get_width()+10)
        cellsize_box.w = cellsize_width

        # Blit the text.
        WIN.blit(cellsx_label, (cellsx_box.x - cellsx_label.get_width()//2 + 30, cellsx_box.y - 40))
        WIN.blit(cellsx_surface, (cellsx_box.x+5, cellsx_box.y+5))
        WIN.blit(cellsy_label, (cellsy_box.x - cellsy_label.get_width()//2 + 25, cellsx_box.y + cellsx_box.height//2 + 40))
        WIN.blit(cellsy_surface, (cellsy_box.x+5, cellsy_box.y + 5))
        WIN.blit(cellsize_label, (cellsx_box.x+5 - cellsize_label.get_width()//2 + 20, cellsy_box.y + cellsy_box.height//2 + 40))
        WIN.blit(cellsize_surface, (cellsx_box.x+5, cellsize_box.y + 5))
        WIN.blit(nextbutton_label, (nextbutton_box.x+5, nextbutton_box.y+5))

        # Blit the input box rect.
        pg.draw.rect(WIN, cellsx_color, cellsx_box, 2)
        pg.draw.rect(WIN, cellsy_color, cellsy_box, 2)
        pg.draw.rect(WIN, cellsize_color, cellsize_box, 2)
        pg.draw.rect(WIN, WHITE, nextbutton_box, 4)

        pg.display.flip() # Update the display window.
        clock.tick(FPS) # Limit the framerate

def select_fields_menu(cellsx, cellsy, cellsize):
    # Define the display window.
    BUTTON_WIDTH, BUTTON_HEIGHT = 80, 50
    WIDTH = cellsx * cellsize
    HEIGHT = cellsy * cellsize + BUTTON_HEIGHT
    WIN = pg.display.set_mode((WIDTH, HEIGHT))

    # Define the start button.
    startbutton_label = button_font.render("START", True, BLACK)
    startbutton_box = pg.Rect(WIDTH // 2 - startbutton_label.get_width() // 2, cellsx * cellsize, startbutton_label.get_width() + 10, BUTTON_HEIGHT)

    # Generate an empty grid.
    g = Grid(cellsize, cellsx, cellsy)
    done = False

    while not done:
        # Retrieve the position of the mouse.
        pos = pg.mouse.get_pos()
        x, y = pos[0] // cellsize, pos[1] // cellsize

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                pg.quit()
            elif event.type == pg.MOUSEBUTTONDOWN: # Check for mouse clicks on the fields.
                if x >= 0 and x < cellsx and y >= 0 and y < cellsy: # Click on a field on the grid.
                    g.toggle_alive(x, y)
                elif startbutton_box.collidepoint(event.pos): # Click on the start button
                    done = True
                    run(g)
        

        WIN.fill(WHITE) # Fill the window with white.
        WIN.blit(startbutton_label, (startbutton_box.x + 5, startbutton_box.y + 5)) # Blit the start button label.
        pg.draw.rect(WIN, BLACK, startbutton_box, 2) # Draw the start button
        g.draw(WIN, BLACK) # Draw the grid
        pg.display.update() # Update the display
        clock.tick(FPS) # Limit the framerate

    return g # Grid with the selected fields

# Run the game, creating new generations of the given grid.
def run(grid):
    # Define the display window.
    CELLS_X = grid.CELLS_X
    CELLS_Y = grid.CELLS_Y
    CELL_SIZE = grid.CELL_SIZE
    WIDTH, HEIGHT = CELLS_X * CELL_SIZE, CELLS_Y * CELL_SIZE
    WIN = pg.display.set_mode((WIDTH, HEIGHT))

    done = False

    while not done:
        new_grid = grid.next_generation() # Create a new generation of the current grid.
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                pg.quit()
        WIN.fill(WHITE) # Fill the background
        grid.draw(WIN, BLACK) # Draw a new grid
        grid = new_grid # Move the grid to a new generation.
        clock.tick(5) # Limit the framerate significantly so that new generations would be easily observable.
        pg.display.update() # Update the display


def main():
    # grid = select_fields_menu(20,20,15)

    (cellsx, cellsy, cellsize) = welcome_menu()
    select_fields_menu(cellsx, cellsy, cellsize)

if __name__ == '__main__':
    main()