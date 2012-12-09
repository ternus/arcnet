#!/usr/bin/python
"""Word Search Generator"""
# Marianne Williams 31 AUG 2007 Toronto, Ontario

import sys
import re
import random

run_phase = 0
input_phase = 0
tab = chr(9)
pattern = "[A-Z]+|[0-9]+"
pat_obj = re.compile(pattern)
# Horizontal, Vertical, Diagonal, Forward, Backward, Up, Down
directions = ['HF','HB','VF','VB','DFU','DFD','DBU','DBD']
optimum_depth = 16
optimum_width = 45
max_depth = 32
max_width = 90

# keys to exit the program
quitseq = 'q,x,end,quit,stop,exit,halt,off' 
quitseq += quitseq.upper() # allow upper case versions
quitseq = quitseq.split(',') # change string to list

dflt_words = []


def gen_wordsearch(words,seed=0): 
    global run_phase
    user_input = {} # Stores results of all user_input
    run_phase = 0
    random.seed(seed)
    user_input[ "search_words" ] = words
    doProcess(user_input)
    s = doReportOutput(user_input)
    print s
    return s

# Processing Data
def doProcess(user_input):
    global run_phase

    search_words = user_input['search_words']    
    new_words = []
    max_len = 0
    act_len = 0
    dict_words = {}
    letter_list = [] # list of letters used to fill grid
    full_string = '' # all the words as one long string
    overlap = 1 # overlap is allowed
    user_input['max_len'] = max_len
    user_input['dict_words'] = dict_words
    user_input['letter_list'] = letter_list
    user_input['full_string'] = full_string
    user_input['overlap'] = overlap
    for line in search_words:
        comma_break = line.split(',')
        for c in comma_break:
            tab_break = c.split(tab)
            for t in tab_break:
                t = t.strip(' ')
                t = t.title()
                if t not in new_words and len(t) > 1:
                    user_input, good = WordList(t, user_input) # add Words to Word List
                    if good:
                        new_words.append(t)
                        if len(t) > act_len: act_len = len(t)
    new_words.sort()
    user_input['search_words'] = new_words    
    user_input['act_len'] = act_len
    return

def WordList(words, user_input):
    max_len = user_input['max_len']
    dict_words = user_input['dict_words']
    letter_list = user_input['letter_list']
    full_string = user_input['full_string']
    overlap = user_input['overlap']
    words = words.upper()
    word_list = re.findall(pat_obj, words)
    new_word = ''
    for word in word_list:
        new_word = new_word + word
    tlen = len(new_word)
    if tlen > max_len:
        max_len = tlen
    word_list = []
    if tlen in dict_words:
        word_list = dict_words[tlen]
    good = 0
    if new_word not in word_list:
        good = 1
        revword = ''
        for letter in new_word:
            revword = letter + revword
            if letter not in letter_list:
                letter_list.append(letter)
        test = full_string.find(new_word)
        if test > 0:
            overlap = 0 # Overlap will not be allowed
        else:
            test = full_string.find(revword)
            if test > 0: overlap = 0 # Overlap will not be allowed
        if revword not in word_list:
            word_list.append(new_word)
            full_string = full_string + new_word + ' '
    dict_words[tlen] = word_list
    user_input['max_len'] = max_len
    user_input['dict_words'] = dict_words
    user_input['letter_list'] = letter_list
    user_input['full_string'] = full_string
    user_input['overlap'] = overlap
    return user_input, good

# Output Results
def doReportOutput(user_input):
    # print program_title
    search_words = user_input['search_words']
    max_len = user_input['max_len']
    act_len = user_input['act_len']
    dict_words = user_input['dict_words']
    letter_list = user_input['letter_list']
    full_string = user_input['full_string']
    grid_width, grid_depth = GridSize(max_len, full_string) # set size
    line_len = grid_width * 2
    if act_len > line_len: line_len = act_len
    return BuildGrid(grid_width, grid_depth, user_input)
    

def GridSize(max_len, full_string):
    test = full_string
    test_len = len(test)
    grid_width = max_len + 1
    grid_depth = grid_width
    if grid_width < optimum_width and grid_depth < optimum_depth:
        mwidth = optimum_width
        mdepth = optimum_depth
    else:
        mwidth = max_width
        mdepth = max_depth
    if grid_depth < 10: grid_depth = 10
    if grid_width < 10: grid_width = 10
    if grid_depth > mdepth and grid_width < mwidth:
        diff = grid_depth - mdepth
        grid_width = grid_width + diff
        grid_depth = mdepth
    if grid_width > mwidth:
        grid_width, grid_depth = ReverseGrid(grid_width, grid_depth)
    elif grid_depth > grid_width and grid_width > mwidth:
        grid_width, grid_depth = ReverseGrid(grid_width, grid_depth)
    return grid_width, grid_depth

def ReverseGrid(grid_width, grid_depth):
    temp = grid_depth
    grid_depth = grid_width
    grid_width = temp
    return grid_width, grid_depth

def BuildGrid(grid_width, grid_depth, user_input):
    max_len = user_input['max_len']
    dict_words = user_input['dict_words']
    letter_list = user_input['letter_list']
    grid_settings = {}
    grid_settings['grid_width'] = grid_width
    grid_settings['grid_depth'] = grid_depth
    dict_keys = dict_words.keys()
    dict_keys.sort(reverse=1) # highest to lowest index    
    cnt = 0
    grid = {}
    agrid = {}
    grid_settings['grid'] = grid
    grid_settings['agrid'] = agrid
    for wlen in dict_keys:
        words = dict_words[wlen]
        for word in words:
            cnt += 1
            if cnt == 1:
                best_directions = directions[:] # HF,HB,VF,VB,DFU,DFD,DBU,DBD
                orientation, best_directions = GetOrientation(grid_settings, max_len,best_directions)
                # setup grid
                x,y = GridPosition(grid_settings, max_len, orientation)
                xstep,ystep = GridStep(orientation)
                grid_settings = FillGrid(x,y,xstep,ystep,word,grid_settings) # put word in the grid
            else:
                grid_settings = AddWord(word,grid_settings,user_input) # add word
    overlap = user_input['overlap']
    overlap_title = ''
    if not overlap:
        overlap_title = '(none of the words overlap)'
        overlap_title = overlap_title.center(grid_width*2)
    return PrintGrid(user_input,grid_settings)

def GetOrientation(grid_settings, len_word, best_directions):
    grid_width = grid_settings['grid_width']
    grid_depth = grid_settings['grid_depth']
    if len_word > grid_width and best_directions == directions:
        best_directions = ['VF','VB']
    elif len_word > grid_depth and best_directions == directions:
        best_directions = ['HF','HB']
    test = random.sample(best_directions,1)
    orientation = test[0]
    cnt = 0
    for test in best_directions:
        if test == orientation:
            del best_directions[cnt]
        cnt += 1
    return orientation, best_directions

def GridPosition(grid_settings, len_word, orientation):
    grid_width = grid_settings['grid_width']
    grid_depth = grid_settings['grid_depth']
    x = 1
    y = 1
    if orientation == 'DFD': # Diagonal Forward Down
        x = GridPos(len_word,grid_width)
        y = GridPos(len_word,grid_depth)
    elif orientation == 'DBD': # Diagonal Backward Down
        x = GridPos(len_word,grid_width)        
        x = (grid_width + 1) - x
        y = GridPos(len_word,grid_depth)
    elif orientation == 'DFU': # Diagonal Forward Up
        x = GridPos(len_word,grid_width)
        y = GridPos(len_word,grid_depth)
        y = (grid_depth + 1) - y
    elif orientation == 'DBU': # Diagonal Backward Up
        x = GridPos(len_word,grid_width)        
        x = (grid_width + 1) - x
        y = GridPos(len_word,grid_depth)
        y = (grid_depth + 1) - y
    elif orientation == 'HF': # Horizontal Forward
        x = GridPos(len_word,grid_width)
        y = random.randint(1,grid_depth)
    elif orientation == 'HB': # Horizontal Backward
        x = GridPos(len_word,grid_width)        
        x = (grid_width + 1) - x
        y = random.randint(1,grid_depth)
    elif orientation == 'VF': # Vertical Forward
        x = random.randint(1,grid_width)
        y = GridPos(len_word,grid_depth)
    elif orientation == 'VB': # Vertical Backward
        x = random.randint(1,grid_width)
        y = GridPos(len_word,grid_depth)
        y = (grid_depth + 1) - y
    if x > grid_width: x = grid_width
    if y > grid_depth: y = grid_depth
    if x < 1: x = 1
    if y < 1: y = 1
    return x,y

def GridStep(orientation):
    xstep = 1
    ystep = 1
    if orientation == 'DBD': # Diagonal Backward Down
        xstep = 0-1
    elif orientation == 'DFU': # Diagonal Forward Up
        ystep = 0-1
    elif orientation == 'DBU': # Diagonal Backward Up
        xstep = 0-1
        ystep = 0-1
    elif orientation == 'HF': # Horizontal Forward
        ystep = 0
    elif orientation == 'HB': # Horizontal Backward
        xstep = 0-1
        ystep = 0
    elif orientation == 'VF': # Vertical Forward
        xstep = 0
    elif orientation == 'VB': # Vertical Backward
        xstep = 0
        ystep = 0-1
    return xstep,ystep

def GridPos(len_word,size):
    if len_word == size:
        pos = 1
    else:
        end_pos = (size - len_word) + 1
        if end_pos < 2:
            pos = 1
        else:
            pos = random.randint(1,end_pos)
    return pos

def FillGrid(x,y,xstep,ystep,word,grid_settings): # put word into the grid
    grid = grid_settings['grid']
    agrid = grid_settings['agrid']
    wlen = len(word)
    for w in word:
        grid[x,y] = w
        if w in agrid:
            old = agrid[w]
        else:
            old = []
        old.append([x,y])
        agrid[w] = old
        x += xstep
        y += ystep
    grid_settings['grid'] = grid
    grid_settings['agrid'] = agrid
    return grid_settings

def AddWord(word,grid_settings,user_input):
    grid_width = grid_settings['grid_width']
    grid_depth = grid_settings['grid_depth']
    grid = grid_settings['grid']
    agrid = grid_settings['agrid']
    overlap = user_input['overlap']
    wlen = len(word)
    acnt = len(word) # after number of letters
    good_add = 0
    bcnt = 0 # before number of letters
    orientation = ''
    do_overlap = random.randint(0,1)
    if overlap and do_overlap:
        test = word
        while test and not good_add:
            t_len = len(test)
            choice = random.randint(0,t_len-1)
            w = test[choice:choice+1]
            test = test.replace(w,'',1)
            if not good_add:
                acnt -= 1
                good_add,grid_settings = OverlapAdd(word,wlen,w,acnt,bcnt,good_add,grid_settings,user_input)
                bcnt += 1
            else:
                break
        if good_add:
            x = grid_settings['x']
            y = grid_settings['y']
            xstep = grid_settings['xstep']
            ystep = grid_settings['ystep']
    if good_add:
        grid_settings = FillGrid(x,y,xstep,ystep,word,grid_settings) # put word in the grid
        grid = grid_settings['grid']
        agrid = grid_settings['agrid']
    while not good_add:
        x = random.randint(1,grid_width)
        startx = 0 + x
        endx = 0 + grid_width
        y = random.randint(1,grid_depth)
        starty = 0 + y
        endy = 0 + grid_depth
        while not good_add and x <= endx:
            while not good_add and y <= endy:
                best_directions = BestDirections(x,y,wlen,grid_settings)
                while not good_add and best_directions:
                    orientation, best_directions = GetOrientation(grid_settings, wlen, best_directions)
                    if orientation:
                        good_add = 1
                        xstep,ystep = GridStep(orientation)
                        pos = 1
                        grid_settings['x'] = x
                        grid_settings['y'] = y
                        grid_settings['xstep'] = xstep
                        grid_settings['ystep'] = ystep
                        good_add = TestGrid(word,pos,grid_settings,user_input)
                        if good_add:
                            grid_settings = FillGrid(x,y,xstep,ystep,word,grid_settings)
                            grid = grid_settings['grid']
                            agrid = grid_settings['agrid']
                y = y + 1
                if y > grid_depth and starty <> 1:
                    y = 1
                    endy = 0 + starty
                    starty = 1
            x = x + 1
            if x > grid_width and startx <> 1:
                x = 1
                endx = 0 + startx
                startx = 1
        if not good_add:
            # make the grid larger
            if grid_width > max_width:
                grid_depth += 1
            else:
                grid_width += 1
            grid_settings['grid_width'] = grid_width
            grid_settings['grid_depth'] = grid_depth
    return grid_settings

def OverlapAdd(word,wlen,w,acnt,bcnt,good_add,grid_settings,user_input):
    grid_width = grid_settings['grid_width']
    grid_depth = grid_settings['grid_depth']
    grid = grid_settings['grid']
    agrid = grid_settings['agrid']
    overlap = user_input['overlap']
    if w in agrid and not good_add:
        test = agrid[w]
        while test and not good_add:
            len_test = len(test)
            choice = random.randint(0,len_test-1)
            t = test[choice]
            del test[choice]
            best_directions = directions[:] # HF,HB,VF,VB,DFU,DFD,DBU,DBD
            orientation = 'HF'
            while not good_add and best_directions and orientation:
                x = t[0]
                y = t[1]
                orientation = ''
                if best_directions == directions:
                    best_directions = []
                    if x > acnt and (x+bcnt) < grid_width:
                        best_directions.append('HB')
                        if y > acnt and (y+bcnt) < grid_depth:
                            best_directions.append('VB')
                            best_directions.append('DBU')
                        elif y > bcnt and (y+acnt) < grid_depth:
                            best_directions.append('DBD')
                    elif x > bcnt and (x+acnt) < grid_width:
                        best_directions.append('HF')
                        if y > bcnt and (y+acnt) < grid_depth:
                            best_directions.append('VF')
                            best_directions.append('DFD')
                        elif y > acnt and (y+bcnt) < grid_depth:
                            best_directions.append('DFU')
                    elif y > acnt and (y+bcnt) < grid_depth:
                        best_directions.append('VB')
                    elif y > bcnt and (y+acnt) < grid_depth:
                        best_directions.append('VF')
                if best_directions:
                    orientation, best_directions = GetOrientation(grid_settings,wlen, best_directions)
                if orientation:
                    good_add = 1
                    xstep,ystep = GridStep(orientation)
                    if xstep == 1:
                        x = x - bcnt
                    if ystep == 1:
                        y = y - bcnt
                    if xstep < 0:
                        x = x + bcnt
                    if ystep < 0:
                        y = y + bcnt
                    grid_settings['x'] = x
                    grid_settings['y'] = y
                    grid_settings['xstep'] = xstep
                    grid_settings['ystep'] = ystep
                    pos = bcnt + 1
                    good_add = TestGrid(word,pos,grid_settings,user_input)
                grid_settings['x'] = x
                grid_settings['y'] = y                
    return good_add, grid_settings

def BestDirections(x,y,wlen,grid_settings):
    grid_width = grid_settings['grid_width']
    grid_depth = grid_settings['grid_depth']
    best_directions = []
    if (x+wlen) <= grid_width:
        best_directions.append('HF')
        if (y+wlen) <= grid_depth:
            best_directions.append('DFD')
        elif (y-wlen) >= 0:
            best_directions.append('DFU')
    if (y+wlen) <= grid_depth:
        best_directions.append('VF')
    if (x-wlen) >= 0:
        best_directions.append('HB')
        if (y+wlen) <= grid_depth:
            best_directions.append('DBD')
        elif (y-wlen) >= 0:
            best_directions.append('DBU')
    if (y-wlen) >= 0:
        best_directions.append('VB')
    return best_directions

def TestGrid(word,pos,grid_settings,user_input): # test put word into the grid
    grid_width = grid_settings['grid_width']
    grid_depth = grid_settings['grid_depth']
    grid = grid_settings['grid']
    overlap = user_input['overlap']
    x = grid_settings['x']
    y = grid_settings['y']
    xstep = grid_settings['xstep']
    ystep = grid_settings['ystep']
    good = 1 # yes it is a good fill
    # test if within grid range
    wlen = len(word)
    if (x+xstep) < 1 or (x+xstep) > grid_width:
        good = 0
    elif (x+(wlen*xstep)) < 1 or (x+(wlen*xstep)) > grid_width:
        good = 0
    if (y+ystep) < 1 or (y+ystep) > grid_depth:
        good = 0
    elif (y+(wlen*ystep)) < 1 or (y+(wlen*ystep)) > grid_depth:
        good = 0
    if good:
        cnt = 0
        # test for overlapping letters
        for w in word:
            cnt += 1
            test = ''
            if (x,y) in grid:
                test = grid[x,y]
                if test <> ' ' and not overlap:
                    good = 0 # we shouldn't overlap
                    break
                elif test <> w and test <> ' ':
                    good = 0 # not good to use
                    break
            if good and cnt <> pos:
                good = Test_Letter(w,x,y,grid_settings,user_input)
            if not good: break
            x += xstep
            y += ystep
    return good

def Test_Letter(w,x,y,grid_settings,user_input):
    # horizontal check
    xtest = 1
    ytest = 0
    good = TestWord(w,x,y,xtest,ytest,grid_settings,user_input)
    # vertical
    xtest = 0
    ytest = 1
    if good: good = TestWord(w,x,y,xtest,ytest,grid_settings,user_input)
    # diagonal check 1
    xtest = 1
    ytest = 1
    if good: good = TestWord(w,x,y,xtest,ytest,grid_settings,user_input)
    # diagonal reversed
    xtest = -1
    ytest = -1
    if good: good = TestWord(w,x,y,xtest,ytest,grid_settings,user_input)
    return good

def TestWord(w,x,y,xtest,ytest,grid_settings,user_input):
    grid_width = grid_settings['grid_width']
    grid_depth = grid_settings['grid_depth']
    grid = grid_settings['grid']
    good = 1
    check = w # check string
    checkf = w # check string
    if xtest > 0 and ytest > 0:
        xb = x - xtest
        yb = y - ytest
        while xb >= 1 and yb >= 1 and (xb,yb) in grid and good:
            check = grid[xb,yb] + check
            good = CheckForWord(check,user_input)
            yb -= ytest
            xb -= xtest
        xf = x + xtest
        yf = y + ytest
        while xf <= grid_width and yf <= grid_depth and (xf,yf) in grid and good:
            check = check + grid[xf,yf]
            good = CheckForWord(check,user_input)
            if good:
                checkf = checkf + grid[xf,yf]
                good = CheckForWord(check,user_input)
            yf += ytest
            xf += xtest
    elif xtest > 0:
        xb = x - xtest
        while xb >= 1 and (xb,y) in grid and good:
            check = grid[xb,y] + check
            good = CheckForWord(check,user_input)
            xb -= xtest
        xf = x + xtest
        while xf <= grid_width and (xf,y) in grid and good:
            check = check + grid[xf,y]
            good = CheckForWord(check,user_input)
            if good:
                checkf = checkf + grid[xf,y]
                good = CheckForWord(check,user_input)
            xf += xtest
    elif ytest > 0:
        yb = y - ytest
        while yb >= 1 and (x,yb) in grid and good:
            check = grid[x,yb] + check
            good = CheckForWord(check,user_input)
            yb -= ytest
        yf = y + ytest
        while yf <= grid_depth and (x,yf) in grid and good:
            check = check + grid[x,yf]
            if good:
                checkf = checkf + grid[x,yf]
                good = CheckForWord(check,user_input)
            yf += ytest
    else:
        xb = x - 1
        yb = y + 1
        while xb >= 1 and yb <= grid_depth and (xb,yb) in grid and good:
            check = grid[xb,yb] + check
            good = CheckForWord(check,user_input)
            yb += 1
            xb -= 1
        xf = x + 1
        yf = y - 1
        while xf <= grid_width and yf >= 1 and (xf,yf) in grid and good:
            check = check + grid[xf,yf]
            good = CheckForWord(check,user_input)
            if good:
                checkf = checkf + grid[xf,yf]
                good = CheckForWord(check,user_input)
            yf -= ytest
            xf += xtest
    return good

def CheckForWord(check,user_input):
    good = 1
    dict_words = user_input['dict_words']
    tlen = len(check)
    if tlen in dict_words:
        word_list = dict_words[tlen]
        if check in word_list: good = 0 # makes a word, not a good choice
        if good:
            rword = ''
            for w in check:
                rword = w + rword
            if rword in word_list: good = 0 # reverse makes a word, not a good choice
    return good

def PrintGrid(user_input,grid_settings):
    grid_width = grid_settings['grid_width']
    grid_depth = grid_settings['grid_depth']
    grid = grid_settings['grid']
    letter_list = user_input['letter_list']
    xstart = 1
    xend = grid_width + 1
    ystart = 1
    yend = grid_depth + 1
# eliminate blank beginning and ending rows and columns
    xstart = grid_width+1
    xend = 1
    ystart = grid_depth+1
    yend = 1
    for x in range(1,grid_width+1):
        for y in range(1,grid_depth+1):
            grid_pos = x,y
            if grid_pos in grid:
                if x < xstart: xstart = x
                if y < ystart: ystart = y
                if x > xend: xend = x
                if y > yend: yend = y
    grid_width = xend - xstart + 1
# now we can print it
    use_letters = letter_list[:]
    str = ""
    str += '-' * ((grid_width * 2) + 1)
    str += '\n'
    for y in range(ystart,yend+1):
        line = ''
        if grid_width <= optimum_width and grid_depth <= optimum_depth:
            line = '|'
        for x in range(xstart,xend+1):
            grid_pos = x,y
            if grid_pos in grid:
                letter = grid[x,y]
            else:
                good = 0
                while not good:
                    use_len = len(use_letters)
                    choice = random.randint(0,use_len-1)
                    letter = use_letters[choice]
                    good = Test_Letter(letter,x,y,grid_settings,user_input)
                    del use_letters[choice]
                    if not use_letters: use_letters = letter_list[:]
                grid[x,y] = letter
                grid_settings['grid'] = grid
            line += letter
            if grid_width <= optimum_width and grid_depth <= optimum_depth: line += '|'
        str += line + '\n'
        if grid_width <= optimum_width and grid_depth <= optimum_depth:
            str += '-' * ((grid_width * 2) + 1)
            str += '\n'
    return str


