[🇫🇷 Français](README.fr.md) | [🇬🇧 English](README.md)

# Chess for NumWorks

A two-player chess game written in MicroPython for the [NumWorks](https://www.numworks.com/) graphing calculator. The whole game fits in a single script (`chess.py`, about 20 KB): board, pieces, move validation and game-over detection are all drawn and computed on the calculator itself.

Script page: <https://my.numworks.com/python/leandre-hiron-latourte/chess>

## Features

- Full 8×8 board with hand-drawn 20×20 pixel sprites for all twelve pieces
- Legal move generation for every piece, with moves that would leave your own king in check filtered out
- Special moves: **castling**, **en passant** and **pawn promotion** (with a selection menu)
- Highlighting of the legal destination squares of the selected piece
- **Checkmate** and **stalemate** detection, with the result displayed on screen
- Smooth, cooldown-based cursor movement

## Installation

1. Open the [script page](https://my.numworks.com/python/leandre-hiron-latourte/chess).
2. Send the script to your calculator from your NumWorks account (USB connection), or copy it into the Python app of the [online simulator](https://www.numworks.com/emulator/graphing/) (the kewstrokes won't work on the simulator).
3. On the calculator, open the **Python** app, select `chess.py` and run it.

The script only uses the modules available on the NumWorks: `kandinsky` (drawing), `ion` (keyboard) and `time`.

## How to play

White plays first, then the players take turns on the same calculator.

| Key | Action |
|-----|--------|
| Arrow keys | Move the green cursor |
| OK | Select one of your pieces, then OK again on a highlighted square to move it |
| OK on another square | Deselect the current piece |
| ↑ / ↓ then OK | Choose a piece in the promotion menu |

Once a piece is selected, its legal destination squares are outlined in pink. After each move, the cursor goes back to the middle of the board for the next player.

When a pawn reaches the last rank, a menu appears on the left of the screen: pick a queen, rook, bishop or knight with the up and down arrows, and confirm with OK.

When the game ends, the screen shows either `WHITE WON` / `BLACK WON` by checkmate, or `DRAW` by stalemate. To play again, run the script again.

## How it works

- **Sprites:** each piece is a list of 20 integers, one per pixel row. Each integer is a 20-digit number in base 3 (`0` transparent, `1` black, `2` white) that is decoded when the piece is drawn. This keeps the sprites compact in the calculator's limited memory.
- **Board:** a flat list of 64 strings (`""` for an empty square, otherwise colour + piece such as `"WK"` or `"BP"`). Squares are indexed `col + row * 8`.
- **Move generation:** one `gen_*_moves` function per piece type. All candidate moves are then tested on a copy of the board with `is_king_in_check`, and the ones that expose the king are removed.
- **Rendering:** the board is drawn with `kandinsky` on 22×22 pixel squares. The `angle` variable (0 to 3) controls the board orientation, and is set to 0 by default.
- **Main loop:** `input_engine` handles the keys and the turn logic, and `game_ends` displays the final result.

## Known limitations

- Local two-player only: there is no computer opponent, undo, or clock.
- Only stalemate is detected as a draw. Threefold repetition, the fifty-move rule and insufficient material are not handled.
- There is no restart option: run the script again to start a new game.

## Project structure

```
chess.py    The whole game (sprites, rendering, rules, input handling)
```