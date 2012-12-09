from random import *

LEVEL_WHITE  = 1
LEVEL_GREEN  = 2
LEVEL_BLUE   = 3
LEVEL_YELLOW = 4
LEVEL_ORANGE = 5
LEVEL_RED    = 6
LEVEL_BLACK  = 7
LEVEL_DIAMOND = 8

MIN_LEVEL = LEVEL_WHITE
MAX_LEVEL = LEVEL_BLACK

LEVEL_SIGMA = 1.0

AVERAGE_ICE_LAYERS = 4

levels = {
    LEVEL_WHITE : 'White',
    LEVEL_GREEN : 'Green',
    LEVEL_BLUE : 'Blue',
    LEVEL_YELLOW : 'Yellow',
    LEVEL_ORANGE : 'Orange',
    LEVEL_RED : 'Red',
    LEVEL_BLACK: 'Black',
    LEVEL_DIAMOND: 'Diamond'
}

DLEVEL_EASY   = 1
DLEVEL_MEDIUM = 2
DLEVEL_HARD   = 3

CONVERSION_FACTOR = 3.0/7.0

diff_levels = {
    DLEVEL_EASY : 'Easy',
    DLEVEL_MEDIUM : 'Medium',
    DLEVEL_HARD : 'Hard'
}

DLEVEL_CHOICES = ( ( dlevel, diff_levels[ dlevel ] ) for dlevel in diff_levels.keys() )

SECURITY_CHOICES = (
    ( LEVEL_WHITE, 'White' ),
    ( LEVEL_GREEN, 'Green' ),
    ( LEVEL_BLUE, 'Blue' ),
    ( LEVEL_YELLOW, 'Yellow' ),
    ( LEVEL_ORANGE, 'Orange' ),
    ( LEVEL_RED , 'Red' ),
    ( LEVEL_BLACK, 'Black' ),
    ( LEVEL_DIAMOND, 'Diamond' ),
)

BLOCK_CIPHER = 'B'
MEMORY_ANALYSIS = 'M'
LINK_HIJACK = 'L'
SOCIAL_ENGINEERING = 'S'
PHYSICAL_ACCESS = 'P'
#CHALLENGE_RESPONSE = 'C'

icetypes = {
    BLOCK_CIPHER : 'Block Cipher',
    MEMORY_ANALYSIS : 'Memory Analysis',
    LINK_HIJACK : 'Link Hijack',
    SOCIAL_ENGINEERING : 'Social Engineering',
    PHYSICAL_ACCESS : 'Physical Access',
#    CHALLENGE_RESPONSE : 'Challenge-Response',
}

CAN_PRINT = " You may print out this page to assist you; printouts are in-game and can be shown to others."

PRINTABLES = [ BLOCK_CIPHER, MEMORY_ANALYSIS, PHYSICAL_ACCESS ]

helptexts = {
    SOCIAL_ENGINEERING : "You must find one of the following people and, without speaking or writing any of the following words, get them to use each one in a sentence.",
    BLOCK_CIPHER : "You must solve this Sudoku puzzle.  You may print out this page to assist you; printouts are in-game.",
    MEMORY_ANALYSIS : "You must locate each of the following words in the grid below.  Words may be found in each of the cardinal directions and diagonally, both backwards and forwards.",
    LINK_HIJACK : "You must deal with the trance on this page -- either take its effect, or pay the computron cost to bypass.",
    PHYSICAL_ACCESS : "You must physically go to the place depicted in the following picture and tag it.",
}




# Each system has a max of one of these, to avoid overloading sudokus and the like.

ICE_MAX_ONE = [ BLOCK_CIPHER, LINK_HIJACK, MEMORY_ANALYSIS ]

ICE_TYPES = ( ( ice, icetypes[ice] ) for ice in icetypes )

ICE_CHOICES = (
    (BLOCK_CIPHER, 'Block Cipher'),
)


FILE_CODE_LENGTH= 5

def get_seed():
    return randint(0,32768)

def gen_random_code():
    str = ""
    for i in range(FILE_CODE_LENGTH):
        str += chr(randint(65,90))
    return str


def genRandomIP():
    # Does not enforce uniqueness constraints.  2.36x10^-10 chance of overlap.  Whatever.
    ip = []
    for i in range(3):
        ip += [str(randint(0,255))]
    ipstr = ip[0] + ":" + ip[1] + ":" + ip[2] 
    return ipstr

