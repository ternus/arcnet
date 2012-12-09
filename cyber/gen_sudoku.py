from pythonsudoku.config import *
from pythonsudoku.sudoku import *
from pythonsudoku.board import *
from pythonsudoku.image import *

seed = 200
s = Sudoku(Board(), seed=seed)
s.create()
i = Image(s.to_board(), str(seed)+".png")

