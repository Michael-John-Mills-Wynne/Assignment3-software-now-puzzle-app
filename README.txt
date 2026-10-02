Picture Puzzle - Assignment 03
Group: DAN/EXT 23
Members: Maximus Turner, Michael Mills-Wynne

How to run
    pip install -r requirements.txt
    python main.py

Controls
    Left click = select / swap, Right click = rotate, Shift + left click = flip

Files
    main.py, app.py      start the game, main window and mouse clicks
    views.py, widgets.py picture areas, buttons and score boxes
    board.py             game logic (moves, hints, solve)
    tile.py              one tile (turns and flip)
    transforms.py        Swap, Rotate, Flip classes
    image_processor.py   OpenCV work

Work split
    Michael Mills-Wynne (about 75%): app.py, views.py, widgets.py, board.py,
                                     image_processor.py, testing
    Maximus Turner (about 25%):      tile.py, transforms.py, main.py, README
