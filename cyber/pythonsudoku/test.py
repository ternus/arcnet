import sudoku,board,image
from config import options

def set_options(opts):
    global options

    # 3rd param of SafeConfigParser.set() must be a string
    options.set("sudoku", "use_letters", str(opts.use_letters))

    options.set("image", "format", opts.format)
    options.set("image", "width", str(opts.width))
    options.set("image", "height", str(opts.height))
    if opts.no_background:
        options.set("image", "background", "")
    else:
        options.set("image", "background", opts.background)
    options.set("image", "lines_colour", opts.lines)
    options.set("image", "font", opts.font)
    options.set("image", "font_colour", opts.font_colour)
    options.set("image", "font_size", str(opts.font_size))

def gen_sudoku(seed):
    b = board.Board()
    s = sudoku.Sudoku(b, seed=seed)
    i = image.Image(s.to_board(), str(seed)+".png")
