# Picture Puzzle - Assignment 03

**Group:** DAN/EXT 23
**Members:** Maximus Turner, Michael Mills-Wynne

## How to run

```bash
pip install -r requirements.txt
python main.py
```

## Controls

| Action | What it does |
|---|---|
| Left click | Select a tile, click another tile to swap |
| Right click | Rotate tile 90° clockwise |
| Shift + left click | Flip tile horizontally |

## Files

| File | Purpose |
|---|---|
| `main.py`, `app.py` | Start the game, main window and mouse clicks |
| `views.py`, `widgets.py` | Picture areas, buttons and score boxes |
| `board.py` | Game logic (moves, hints, solve) |
| `tile.py` | One tile (turns and flip) |
| `transforms.py` | Swap, Rotate, Flip classes |
| `image_processor.py` | OpenCV work |

## Work split

| Member | Share | Files / tasks |
|---|---|---|
| Michael Mills-Wynne | about 75% | `app.py`, `views.py`, `widgets.py`, `board.py`, `image_processor.py`, testing |
| Maximus Turner | about 25% | `tile.py`, `transforms.py`, `main.py`, README |
