#!/usr/bin/env python
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "settings" # I Know What I Am Doing Is Wrong

from random import *
import settings

from django.contrib import auth
from django.core.files import File
from core.models import *
from cyber.models import *
from django.contrib.auth.models import Permission
from media.models import *
from mail.models import *
from pedia.models import *
from research.models import *

c = Character(username='gm', first_name="", last_name="GM",password='passwrd')
c.is_superuser = True
c.is_staff = True
c.set_password("passwrd")
f = open('profiles/alice.jpg', 'r')
c.image = File(f)
c.save()
c.playername = "Arcadia GMs"
c.type = "GM"
c.gender="Indeterminate"
c.race="?????"
c.sector="Unknown"
c.computron_income = 10
c.phone = ""
c.email = "arcadia-gms@mit.eduXXXCHANGEME"
c.visible = False
c.fame = 10
c.save()

assert(c.check_password("assbarn"))
u = auth.models.User.objects.all()[0]
assert(u.check_password("assbarn"))
assert(u.is_staff)
assert(u.is_superuser)
assert(u.is_active)

g = c

# c = Character(username='test', password='test')
# #f = open('templates/netimg/profiles/.jpg', 'r')
# #c.image = File(f)
# c.visible=False
# c.save()
# c.set_password('test')
# c.first_name = "Johnny"
# c.last_name = "Test-osterone"
# c.email = "test@test.test"
# c.fame = 20
# #c.user_permissions.add("is_hacker", "is_media")
# c.save()


#from char import chars

chars = []

for cd in chars:
    c = Character(username=cd, 
                  playername=chars[cd]["playername"],
                  gender=chars[cd]["gender"],
                  residence=chars[cd]["residence"],
                  phone=chars[cd]["phone"],
                  donotcall=chars[cd]["donotcall"],
                  email=chars[cd]["email"],
                  first_name=chars[cd]["firstname"],
                  last_name=chars[cd]["lastname"],
                  candidate=chars[cd]["famous"],
                  race=chars[cd]["race"],
                  nickname=chars[cd]["nickname"],
                  title=chars[cd]["title"],
                  computron_income=chars[cd]["computrons"])
    if chars[cd]["email"]:
        try:
            if chars[cd]["picfile"]:
                fakeemail = chars[cd]["picfile"]
            else:
                fakeemail = chars[cd]["email"].split('@')[0]+".jpg"
            f = open('profiles/'+fakeemail, 'r')
            c.image = File(f)
        except:
            print c.charname, fakeemail
            pass
    if "visible" in chars[cd].keys(): c.visible = chars[cd]["visible"]
    if "press" in chars[cd].keys(): c.press = chars[cd]["press"]
    if c.computron_income < 10: c.hacker = False
    c.computrons = c.computron_income
    c.set_password(chars[cd]["password"])
    c.save()
    a = Agent(name=c.charname,controller=c,direct=True,influence=chars[cd]["influence"])
    a.save()


from rumors import rumors

for rumor in rumors:
    try:
        r = Rumor(subject=Character.objects.get(username=rumor[0]).charname, text=rumor[1])
        r.save()
    except:
        print rumor


words = ['automata', 'Archer', 'Captain', 'Arcadia', 'Laconia', 'Birdie', 'research', 'station', 'Ark', 'pornstar', 'trance', 'drugs', 'Grooovytron', 'performance', 'ambassador', 'surface', 'virus', 'quarantine', 'Rauncher', 'Patsy', 'utopia', 'Communism', 'Calvin', 'Neptunians', 'Catholics', 'Mathison', 'ALICE', 'Cthulhu', 'dance', 'party', 'work', 'science', 'sex', 'Hamster', 'FirstGen']

for word in words:
    w = Word(word)
    w.save()
sciencewords = [
  "nanoparticle",
  "polymer",
  "aorta",
  "pandemonium",
  "allele",
  "barometer",
  "cell",
  "chromatography",
  "chromosome",
  "cornea",
  "crystal",
  "cytoplasm",
  "diaphragm",
  "diode",
  "distillation",
  "electromagnet",
  "electron",
  "embryo",
  "energy",
  "ethanol",
  "foetus",
  "foodchain",
  "fossil",
  "fuel",
  "fuse",
  "generator",
  "kidney",
  "liquid",
  "lung",
  "microscope",
  "microwave",
  "molecule",
  "motor",
  "neutron",
  "nucleus",
  "periodictable",
  "planet",
  "prism",
  "radiation",
  "retina",
  "satellite",
  "triceps",
  "uterus",
  "amoeba",
  "binary",
  "boiling",
  "carnivore",
  "circuit",
  "convection",
  "current",
  "DNA",
  "evolution",
  "extinction",
  "forest",
  "fossil",
  "fungus",
  "gem",
  "gravity",
  "helium",
  "inertia",
  "laser",
  "lever",
  "lightning",
  "longitude",
  "magma",
  "meteor",
  "molecule",
  "neuron",
  "onion",
  "opaque",
  "photosynthesis",
  "pollution",
  "predator",
  "redshift",
  "reflection",
  "refraction",
  "spore",
  "tornado",
  "ultraviolet",
  "uranium",
  "velociraptor",
  "cortex",
  "wavelength",
]

for word in sciencewords:
    w = Word(word)
    w.save()

fameItems = [
    'Every member of a public group is present',
    'Picture takes place in a Waystation',
    'There is political or corporate negotiation in the picture',
    'picture is in the middle of a Shadowrun',
    'picture takes place during a religious service or speech',
    'at least one corpse in the picture',
    'at least three unconscious people are in the picture',
    'tense atmosphere: combat or an interrogation or similar are present',
    'at least six weapons are in the picture',
    'ten or more people are in the picture',
    '250 or more pan are visible in the picture',
    'a PI is investigating a crime in the picture',
    'a student is doing their homework in the picture',
    'shaking hands with the head of the current Government',
    'all four ReMade are in the picture',
    'at least two purple headbands are in the picture',
    'at least three blue headbands are in the picture',
    'eight or more automata are in the picture',
    'eight or more Laconians are in the picture',
    ]

for fame in fameItems:
    f = FameItem(name=fame, value=1)
    f.save()

subjects = [
    ['Independence', 
     'Laconian and Arcadian sectors should be independent.',
     'The government should run the entire station.','s'],
    ['Market',
     'The station should be a libertarian paradise.',
     'The station should be a socialist utopia.','s'],
    ['Automata',
     'Automata should have the rights of humans.',
     'Automata are tools and should be considered property.','s'],
    ['ReMade',
     'ReMade must be allowed to reproduce.',
     'ReMade reproduction must be disallowed for the good of all.','s'],
    ['Birth',
     'Natural childbirth should be encouraged.',
     'All births should be handled through the creches.','s'],
    ['Society',
     'A new world needs new social models.',
     'The old ways are the best ways.','s'],
    ['Trance',
     'Trance should be legal.',
     'Trance is dangerous and should be prohibited.','s'],

    ['ALICE', '','','e'],
    ['The New Darwinian Order', '','','e'],
    ['SWORD Conglomerates', '','','e'],
    ['SHIELD LLC', '','','e'],
    ['Elysium Medical Industries', '','','e'],
    ['The Neptunian Church', '','','e'],
    ['The Science Council', '','','e'],
    ['The Aquatic Defense Initiative', '','','e'],
    ['The Dockworkers\' Local 314', '','','e'],
    ['The Laconian High Command', '','','e'],
    ['G-Splice', '','','e'],
    ['Tangent Technologies', '','','e'],
    ['The Roman Catholic Church', '','','e'],
    ['Dockworkers\' Local 314', '','','e'],
    ['Colonization', '','','o']

]



for subject in subjects:
    s = Subject(name=subject[0],pro=subject[1],anti=subject[2],type=subject[3])
    s.save()
    

a = Agent(name="GM", controller=g, direct=True)
a.save()

agents = [
    ['ADI', 'catalan', 4],
    ['ARC Science Council', 'hal', 3],
    ['Dockworkers Local 314', 'rosseau', 5],
    ['Laconian High Command', 'mccaskill', 3],
    ['Catholic Church', 'demos', 3],
    ['Neptunian Church', 'lavender', 3],
    ['New Darwinian Order', 'kostelnik', 3],
    ['SWORD', 'lockhart', 3],
    ['SHIELD', 'gauntlet', 3],
    ['ACME', 'overton', 1],
    ['Elysium', 'walker', 1],
    ['G-Splice', 'meyer', 1],
    ['Tangent Technologies', 'mccaskill',1],
    ['social elite', 'calvin', 4],
    ['disaffected youth', 'grooovytron', 4],
    ['conservatives', 'byrd', 3],
    ['libertarians', 'mctaggert', 3],
    ['scientific community', 'grooovytron', 2],
    ['Darwinian followers', 'pieters', 3],
    ['Neptunian laity', 'rauncher', 3],
    ['Catholic laity', 'caesar', 3],
    ['Laconians on the street', 'vikki', 3],
    ['Arcadians on the street', 'archer', 4],
    ['automata on the street', 'freud', 2],
    ['ReMade on the street', 'lace', 2],
    ['lawyers', 'tirasa', 3],
    ['ravers', 'hatter', 3],
    ['nihilists', 'steadham', 3]]


for agent in agents:
    try:
        a = Agent(name=agent[0], controller=Character.objects.get(username=agent[1]), influence=agent[2])
        a.save()
    except:
        print agent


pedia = [

["ADI", "Aquatic Defense Initiative; occasionally referred to as the \"Arcadian military\", composed largely of ATCOL elements"],

["ALICE", "Autonomous Life-supporting Intelligent Control Entity; artificial intelligence in control of ARCADIA"],

["A-mail", "Electronic mail received via ARCNET."],

["ARC", "Atlantic Research Command; central research organization, administered by the Science Council."],

["ARCADIA", "Atlantic Research Command / Aquatic Defense Initiative; research and military station; last hope of humanity. The upper case version of the name is used to refer to the physical station. See also: Arcadia."],

["Arcadia", "the lower case version of the name is used to refer to the society or the de facto government formed by the ADI, the ARC and the Local. See also: ARCADIA."],

["Archer, Captain James (Sr.)", "a captain in the ADI during the Battle of Sector 5, and posthumous local hero."],

["ARCNET", "computer network spanning all of ARCADIA"],

["Ark", "(slang) see ARCADIA"],

["ATCOL", "the Atlantic Coalition; military alliance of the pre-Crisis nations; constructors of the Ark"],

["auto", "(slang) see Automata"],

["Automata", "humanoid constructs endowed with human-equivalent intelligence. Their brains are pandemonium cores."],

["Autorobotics Control Act", "old Earth legislation regulating the construction of automata"],

["Arcadian Civil War", "Civil war between Arcadia and Laconia."],

["deuce", "Slang terminology for a prostitute due to their common price of 2 pan."],


["Crisis", "term for Z1 pandemic; began in October 2142; led to the destruction of 99.99% of humanity"],

["FirstGen", "(slang) People who were adults when the Crisis hit."],

["Great Liberation", "October 8, 2142, the date of the Crisis."],

["Hamsters", "children born on the Ark (derogatory) (from Noah's disobedient son, Ham)"],

["Infected", "the official term for those who fell to Z1"],

["Laconia", "splinter nation residing in Sectors 8 and 9."],

["LHC", "Laconian High Command"],

["Lockdown", "ALICE's emergency security protocols enacted during the Crisis"],

["Mathison, Adam", "Legendary FirstGen scientist and mathematician; creator of autos, ARCNET, ALICE"],

["netspace", "collective computing environment formed by ARCNET"],

["node", "point of entry into netspace"],

["pandemonium", "rare and hard to produce type of strange matter with attractive quantum computing applications"],

["Pandora, Isaac", "Legendary pre-Crisis physicist and materials scientist. Discoverer of pandemonium matter."],

["Pan", "(slang) nickname for the Arcadian currency"],


["ReMade", "humans augmented through genetic and biological engineering. Forbidden to breed by ALICE, as a danger to the mainline human genome. Disparaged by the rest of Arcadia for their lack of children."],

["Sector", "a subunit of the station; there are 16 sector. All sectors except 5, 8 and 9 are administered by an ADI/ARC/Labor partnership."],

["Sector 5, Battle of", "prolonged firefight between ADI security forces and Infected on the station during the Crisis. Currently detached and at the bottom of the sea."],

["Shatter", "inevitable deterioration of human sanity resulting from life in a tin can at the bottom of the sea"],

["Starving Years", "the first decade or so after the Crisis, when the Ark was being converted to food and manufacturing for the people trapped aboard."],


["SWORD Brand Cola", "A delicious and refreshing synthetic drink, enjoyed by children and adults alike!"],

["trance", "Cybernetic programs that stimulate the cerebral cortex to achieve narcotic effects."],

["Z1", "A highly infectious virus, similar to rabies.  Caused the Crisis."],

["Zs, Zack, Zed", "(slang) see Infected."],

]

for entry in pedia:
    p = Entry(name=entry[0],text=entry[1])
    p.save()


comp = Computer(name="TestServer", security_level=3, address="111:111:111")
comp.save()

# ps = Permission.objects.filter(id__lt=41)
# for p in ps:
#     p.delete()


tech = {}

tech[ "A" ] = ["Basic Pandemonium Computer Processing", [], "P",
               "Skills: Materials, CS, CS, Particle, Particle",
               """
Observe an Auto play tic-tac-toe, hangman, and dots (see
http://superkids.com/aweb/tools/logic/dots/ if you don't know dots)
with a human.  Each game must be played at least once and they must
play for a total of five minutes.  The human and the auto cannot be
providing skills for the experiment.  Remember this must be done in a
Lab."""]
tech[ "B" ] = ["Basic Pandemonium Power Generation", [], "P",
               "Skills: Materials, Particle, Particle, Robotics, Robotics",
"""
Acquire a Plasmatic Condenser, a flashlight, and a roll of Duct tape.
Bring them to the lab.  You must expend a use of Basic Particle and a
use of Basic Materials to combine them into a Pandemonium Powered
Flashlight.  This device is identical to a regular flashlight for game
purposes, except that it counts as a Level 1 Commodity Device.  Rip up
the Plasmatic Condeser and the Duct tape.
"""               
]
tech[ "C" ] = ["Basic Pandemonium Material Engineering", [], "P",
               "Skills: Materials, Materials, Materials, Particle, Particle",
             """
Acquire a Magnetophobic Inductor and go to the lab.  Do a CR10 martial
attack on the wall of the lab, and observe it's reaction with the
Magnetophobic Inductor.
"""]

#Level 2:

tech[ "D" ] = ["Wireless Pandemonium Networking", ["A", "C"], "P"]
tech[ "E" ] = ["Intermediate Pandemonium Computer Processing", ["A"], "P"]
tech[ "F" ] = ["Subsystem Processing Core Location", ["A", "B"], "P"]
tech[ "G" ] = ["Intermediate Pandemonium Power Generation", ["B"], "P"]
tech[ "H" ] = ["Satellite Payload Design", ["B", "C"], "P"]
tech[ "I" ] = ["Intermediate Pandemonium Material Engineering", ["C"], "P"]

#Level 3:

tech[ "J" ] = ["Pandemonium Electromagnetics", ["E", "B"], "P"]
tech[ "K" ] = ["Pandemonium Expert Systems", ["E"], "P"]
tech[ "L" ] = ["Pandemonium Microprocessors", ["E", "C"], "P"]
tech[ "M" ] = ["Power Flow Regulation", ["G", "A"], "P"]
tech[ "N" ] = ["Radiation Safety Precautions", ["G"], "P"]
tech[ "O" ] = ["Wireless Power Transmission", ["G"], "P"]
tech[ "P" ] = ["Self-Modulating Construction Techniques", ["I"], "P"]
tech[ "Q" ] = ["Basic Pandemonium Mechanical Engineering", ["I"], "P"]
tech[ "R" ] = ["Room Temperature Superconductivity", ["I", "B"], "P"]

#Level 4:

tech[ "S" ] = ["Basic AI Creation", ["J", "K"], "P"]
tech[ "T" ] = ["Advanced Pandemonium Computer Processing", ["K", "L"], "P"]
tech[ "U" ] = ["Micro Power Generation", ["L", "M"], "P"]
tech[ "V" ] = ["Advanced Pandemonium Power Generation", ["M", "N"], "P"]
tech[ "W" ] = ["Area Broadcast Power Supplies", ["N", "O"], "P"]
tech[ "X" ] = ["Remote Auto Operations", ["O", "P"], "P"]
tech[ "Y" ] = ["Advanced Pandemonium Mechanical Engineering", ["P", "Q"], "P"]
tech[ "Z" ] = ["Advanced Pandemonium Material Engineering", ["Q", "R"], "P"]
tech[ "AA" ] = ["Nanosecond Magnetic Field Manipulation ", ["R", "J"], "P"]

#Level 5:

tech[ "BB" ] = ["Advanced AI Creation", ["S"], "P"]
tech[ "CC" ] = ["Auto Power Cores", ["T", "U"], "P"]
tech[ "DD" ] = ["Distributed Power Production and Control", ["V"], "P"]
tech[ "EE" ] = ["Power Non-interference Protocols", ["W", "X"], "P"]
tech[ "FF" ] = ["Hardened Pandemonium", ["Y"], "P"]
tech[ "GG" ] = ["Basic Pandemonium Creation", ["Z", "AA"], "P"]

#Level 6:
tech[ "HH" ] = ["Expert Pandemonium Programming", ["BB", "T21"], "P"]# (And Trance Level 4) (Auto Psychlims)], "P"]
tech[ "II" ] = ["Multibody Coordination and Control", ["BB", "Z30"], "P"]# (and Z1 Level 4) (Roboslavers)], "P"]
tech[ "JJ" ] = ["Self-Constructing Infrastructures", ["CC", "DD"], "P"]
tech[ "KK" ] = ["Expert Pandemonium Power Control", ["EE", "FF"], "P"]
tech[ "LL" ] = ["Expert Pandemonium Material Engineering", ["GG"], "P"]

#Level 7:

tech[ "MM" ] = ["Pandemonium Deconstruction", ["LL", "W"], "P"]
tech[ "NN" ] = ["Advanced Pandemonium Creation", ["LL", "V"], "P"]
tech[ "OO" ] = ["Expert Pandemonium Mechanical Engineering", ["JJ", "FF"], "P"]

tech[ "D1" ] = ["Basic Brain Chemistry", [], "D",
                "Skills: Neurobio x2, BioChem x2, Genetics",
                """Experiment:
Prepare two minutes worth of questions to ask someone.  In a Lab,
converse with a human for 2 minutes, asking those questions, then have the same
conversation with them after they have had an alcoholic drink.
"""]
tech[ "D2" ] = ["Basic Body Chemistry", [], "D",
                "Skills: BioChem x3, Neurobio x1, Genetics x1",
"""
Acquire a Genetic Decoupler and a Bioinformatics Matrix.  Get a
volunteer (not remade or autos) who is not providing skills for the
experiment, and bring them to the Lab with you.  Spend two minutes
using the devices to take readings from the volunteer.
"""
]
tech[ "D3" ] = ["Basic Anatomy", [], "D",
                "Skills: Mechanics, Robotics, BioChem, Genetics, Neurobio",
"""
Gather five non-autos who are *not* providing skills for the
experiment and take them to the Lab with you.  Use a tape measure
(freely available) to measure the distance from their fingertip to
wrist, wrist to elbow, elbow to shoulder, hip to knee, knee to ankle.
"""
]
tech[ "D4" ] = ["Natural Uppers", ["D1"], "D"]
tech[ "D5" ] = ["Intermediate Brain Chemistry", ["D1"], "D"]
tech[ "D6" ] = ["Artificial Adrenal Response", ["D2"], "D"]
tech[ "D7" ] = ["Intermediate Body Chemistry", ["D2"], "D"]
tech[ "D8" ] = ["Basic Environmental Effects", ["D3"], "D"]
tech[ "D9" ] = ["Underwater Functionality", ["D3"], "D"]
tech[ "D10" ] = ["Natural Downers", ["D4"], "D"]
tech[ "D11" ] = ["Designing Uppers", ["D4"], "D"]
tech[ "D12" ] = ["Advanced Brain Chemistry", ["D5"], "D"]
tech[ "D13" ] = ["Accelerated Repair", ["D6"], "D"]
tech[ "D14" ] = ["Global Hormonal Rebalancing", ["D6"], "D"]
tech[ "D15" ] = ["Advanced Body Chemistry", ["D7"], "D"]
tech[ "D16" ] = ["Biochemical Environments", ["D8"], "D"]
tech[ "D17" ] = ["Intermediate Environmental Effects", ["D8"], "D"]
tech[ "D18" ] = ["Aquatic Lifeforms", ["D9"], "D"]
tech[ "D19" ] = ["Natural Responses", ["D10"], "D"]
tech[ "D20" ] = ["Interrupted Neural Pathways", ["D10"], "D"]
tech[ "D21" ] = ["Human Pheremone Design", ["D11"], "D"]
tech[ "D22" ] = ["Neuron Regrowth", ["D12", "D13"], "D"]
tech[ "D23" ] = ["Deliberate Hormone Imbalances", ["D14"], "D"]
tech[ "D24" ] = ["Hormone Replacement", ["D14"], "D"]
tech[ "D25" ] = ["Expert Body Chemistry", ["D15"], "D"]
tech[ "D26" ] = ["Advanced Biochemicals", ["D15", "D16"], "D"]
tech[ "D27" ] = ["Healthy Environments", ["D17"], "D"]
tech[ "D28" ] = ["Advanced Environmental Effects", ["D17"], "D"]
tech[ "D29" ] = ["Underwater Maneuverability", ["D18"], "D"]
tech[ "D30" ] = ["Regenerative Creatures", ["D18"], "D"]
tech[ "D31" ] = ["Patterns of Neuron Disintegration", ["D20"], "D"]
tech[ "D32" ] = ["Brain Cancer", ["D20", "D22"], "D"]
tech[ "D33" ] = ["Cellular Rejuvenation", ["D22", "D24"], "D"]
tech[ "D34" ] = ["Artificial Hormone Control", ["D24", "D26"], "D"]
tech[ "D35" ] = ["Expert Environmental Effects", ["D26", "D28"], "D"]
tech[ "D36" ] = ["Survivability Increasers", ["D28", "D30"], "D"]
tech[ "D37" ] = ["Regeneration Interference", ["D30"], "D"]
tech[ "D38" ] = ["Chemical Trance Induction ", ["D34", "T19"], "D"]
tech[ "D39" ] = ["Fertility Biochem", ["D36", "G30"], "D"]
tech[ "D40" ] = ["Increased Bodily Disfunction", ["D32", "D37"], "D"]
tech[ "D41" ] = ["Genomic Purity Restoration ", ["D40", "G34"], "D"]

tech[ "T1" ] = ["Hacking 101", [], "T",
                "Skills: CSx3, Robotics x2",
"""
Acquire a Subatomic Hyperslicer and a Neophasic Nullifier.  Also
acquire a medium sudoku puzzle from www.sudokuslam.net. Go to the Lab
with the experimenters and the equipment and solve the sudoku.  
"""
]
tech[ "T2" ] = ["Basic Computronics ", [], "T",
                "Skills: CS x 2, Robotics x2, Particle",
"""
Find someone with a Computron income of 15 or 20.  Take them to the
lab with you and interview them for five minutes on their opinions
about computers.
"""]
tech[ "T3" ] = ["Building Your Own Jack ", [], "T",
                "Skills: Robotics, CS, Mechanics x3",
"""
Get a Neophasic Nullifier, a Positron Carbonizer, and a roll of Duct
Tape.  Take them to a lab, where you must use up one charge of basic
robotics and one charge of basic Mechanics to turn them into a Jack.
This is a level 1 Cyber Sector Device, but does not produce any RTIs of
its own.  Rip up the original item cards and write yourself one for
the device.
"""
]
tech[ "T4" ] = ["Basic ICE", ["T1"], "T"]
tech[ "T5" ] = ["The Importance of Hardware Access", ["T1"], "T"]
tech[ "T6" ] = ["The IP Address", ["T2"], "T"]
tech[ "T7" ] = ["Data Smashing and Crashing", ["T2"], "T"]
tech[ "T8" ] = ["Touring the Cloud", ["T3"], "T"]
tech[ "T9" ] = ["Avoiding Burnout", ["T3"], "T"]
tech[ "T10" ] = ["Turning Walls Into Doors", ["T4"], "T"]
tech[ "T11" ] = ["Trance Traps", ["T4"], "T"]
tech[ "T12" ] = ["Personal Computing", ["T5"], "T"]
tech[ "T13" ] = ["Internet Protocols A History", ["T6"], "T"]
tech[ "T14" ] = ["Other People's Machines", ["T6"], "T"]
tech[ "T15" ] = ["Advanced Computronics", ["T7"], "T"]
tech[ "T16" ] = ["Forgotten Places in Cyberspace", ["T8"], "T"]
tech[ "T17" ] = ["Flying High", ["T8"], "T"]
tech[ "T18" ] = ["Fixing Burnout", ["T9"], "T"]
tech[ "T19" ] = ["Keeping Walls on Your Brain", ["T10"], "T"]
tech[ "T20" ] = ["Encryption Protocols", ["T10"], "T"]
tech[ "T21" ] = ["Trance and Psychosis", ["T11"], "T"]
tech[ "T22" ] = ["Your Brain as an IP Address", ["T12", "T13"], "T"]
tech[ "T23" ] = ["Distributed Computing", ["T14"], "T"]
tech[ "T24" ] = ["Denial of Service Attacks", ["T14"], "T"]
tech[ "T25" ] = ["Computrons/Brain Interfaces", ["T15"], "T"]
tech[ "T26" ] = ["Forging New Territory", ["T15", "T16"], "T"]
tech[ "T27" ] = ["Operating on Auto Pilot", ["T17"], "T"]
tech[ "T28" ] = ["A View from Above", ["T17"], "T"]
tech[ "T29" ] = ["Programming Biology", ["T18"], "T"]
tech[ "T30" ] = ["Burnout Attacks", ["T18"], "T"]
tech[ "T31" ] = ["Encrypting Consciousness", ["T20"], "T"]
tech[ "T32" ] = ["Subliminal Trance", ["T20", "T22"], "T"]
tech[ "T33" ] = ["Hypno Trance", ["T22", "T24"], "T"]
tech[ "T34" ] = ["Fast Cloud Creation", ["T24", "T26"], "T"]
tech[ "T35" ] = ["Detail Trance", ["T26", "T28"], "T"]
tech[ "T36" ] = ["Burning Out While Flying", ["T28", "T30"], "T"]
tech[ "T37" ] = ["Brainstem Redirection", ["T30"], "T"]
tech[ "T38" ] = ["Trance Based Education", ["T34", "G19"], "T"]
tech[ "T39" ] = ["Chemical Trance Integration", ["T32", "Z22"], "T"]
tech[ "T40" ] = ["Trance Dissociation", ["T35", "G27"], "T"]
tech[ "T41" ] = ["Using the Burn", ["T36", "D19"], "T"]
tech[ "T42" ] = ["Expert Trance Creation", ["T41", "D30"], "T"]
tech[ "T43" ] = ["Burning through the Brain", ["T31"], "T"]
tech[ "T44" ] = ["Destructive Trance", ["T43"], "T"]
tech[ "T45" ] = ["Tranced Out", ["T33", "Z33"], "T"]
tech[ "T46" ] = ["Test Pattern Trance", ["T45"], "T"]


tech[ "G1" ] = ["ReMade Analysis", [], "G",
                "Skills: Genetics x2, BioChem, Neurobio, Mechanics",
"""
Acquire a Bioinformatics Matrix.  Bring any ReMade to the Lab with
you, and scan them.  This takes two minutes.
"""]
tech[ "G2" ] = ["Basic Genomics", [], "G",
                "Skills: Genetics x 3, BioChem, Neurobio",
"""
Gather five volunteers (non-auto) of clearly distinct phenotypes
(either in player or in character, up to you).  Bring them to the Lab
with you and interview them as a group about their family histories
for five minutes.  The volunteers cannot be providing skills for the
experiment.
"""
]
tech[ "G3" ] = ["Retroviral Recombinates", [], "G",
                "Skills: CS, Genetics x2, Biochem, Materials",
"""
Acquire a Plasmatic Condenser and a Nanowave Projector, and a roll of
duct tape.  Take these to the Lab, where you must expend a use of
Genetics and of Biochem to turn them into a Retroviral Shield.  This
device has no use in game other than to be a Level 1 Military Device.
Tear up the item cards you started with and write a new one.
"""
]
tech[ "G4" ] = ["Human/Animal Interspeciation", ["G1"], "G"]
tech[ "G5" ] = ["Individual Design", ["G1"], "G"]
tech[ "G6" ] = ["Gamete Operations", ["G2"], "G"]
tech[ "G7" ] = ["Intermediate Genomics", ["G2"], "G"]
tech[ "G8" ] = ["Embryo Interactions", ["G3"], "G"]
tech[ "G9" ] = ["Creche Operations", ["G3"], "G"]
tech[ "G10" ] = ["Maintaining Brain Integrity", ["G4"], "G"]
tech[ "G11" ] = ["Specific Animal Traits", ["G4", "G5"], "G"]
tech[ "G12" ] = ["Basic Genome Creation", ["G5", "G2"], "G"]
tech[ "G13" ] = ["ReMade Fertility", ["G6", "G1"], "G"]
tech[ "G14" ] = ["Species Maintenance", ["G6", "G7"], "G"]
tech[ "G15" ] = ["Adult Alterations", ["G7", "G3"], "G"]
tech[ "G16" ] = ["Early Error Detection", ["G8", "G2"], "G"]
tech[ "G17" ] = ["Rapid Growth", ["G8", "G9"], "G"]
tech[ "G18" ] = ["Chemical Balance Maintenance", ["G9"], "G"]
tech[ "G19" ] = ["Brain Design", ["G10"], "G"]
tech[ "G20" ] = ["Intermediate Interspeciation", ["G11", "G12"], "G"]
tech[ "G21" ] = ["Advanced Genome Creation", ["G12"], "G"]
tech[ "G22" ] = ["Basic ReMade Design", ["G12", "G13"], "G"]
tech[ "G23" ] = ["Genomic Domination", ["G14"], "G"]
tech[ "G24" ] = ["Embryonic Corrections", ["G15", "G16"], "G"]
tech[ "G25" ] = ["Genetic Disease Analysis", ["G16"], "G"]
tech[ "G26" ] = ["Replication Error Removal", ["G16", "G17"], "G"]
tech[ "G27" ] = ["Contamination Removal", ["G18"], "G"]
tech[ "G28" ] = ["Interspecies Immunoresponses", ["G20"], "G"]
tech[ "G29" ] = ["Blended Genetics", ["G20", "G21"], "G"]
tech[ "G30" ] = ["Genetic Disease Removal", ["G21", "G22"], "G"]
tech[ "G31" ] = ["Advanced ReMade Design", ["G21", "G22", "G23"], "G"]
tech[ "G32" ] = ["Advanced Genomics", ["G22", "G23", "G24"], "G"]
tech[ "G33" ] = ["Stabilizing Heritability", ["G23", "G24"], "G"]
tech[ "G34" ] = ["Adult Disease Correction", ["G24", "G25"], "G"]
tech[ "G35" ] = ["Genetic Disease Creation", ["G26"], "G"]
tech[ "G36" ] = ["Animal Cybernetic Training", ["G19", "T15"], "G"]
tech[ "G37" ] = ["Mutagenic Trance Induction", ["G34", "T18"], "G"]
tech[ "G38" ] = ["Advanced Interspecies Genetics", ["G29", "G33"], "G"]
tech[ "G39" ] = ["Male-Female Genetic Recombination", ["G32", "D11"], "G"]
tech[ "G40" ] = ["Fertility Genetics", ["G39", "Z24"], "G"]
tech[ "G41" ] = ["Biologically Encoded Fixations", ["G33", "T35"], "G"]
tech[ "G42" ] = ["Pair Bonding Genotype", ["G41", "D11"], "G"]
tech[ "G43" ] = ["Z1 Regenerative Genetic Modifications", ["G25", "Z26", "D27"], "G"]

tech[ "Z1" ] = ["Basic Zed Thought Patterns", [], "Z"]
tech[ "Z2" ] = ["Basic Zed Animation Process", [], "Z", 
                "Skills: Mechanics x2, Robotics x2, Biochem",
"""
Acquire a pressure suit and someone who can lift more than two dots of
bulkiness.  Put on the suit and let the person who can lift extra dots
of bulkiness move you around the Lab for 2 minutes, while you attempt
to match the slow and awkward gait of a standard Zed.
"""]
tech[ "Z3" ] = ["Basic Zed Recovery Process", [], "Z"]
tech[ "Z4" ] = ["Basic Zed Digestion Process", [], "Z",
                "Skills: Biochem, Materials x2, Genetics, Neurobio",
"""
Acquire a Genetic Decoupler, a Nanowave Projector, and a roll of Duct
tape.  Take them to the Lab.  You (as a group) must use up one basic
Biochem Skill and one Basic Materials Skill to turn them into a Model
Zed Digestive Track.  Rip up the original item cards.  The new Item is
a Level 1 Biological Device, but does not produce any items itself.
"""

]
tech[ "Z5" ] = ["Basic Zed Infection Process", [], "Z"]
tech[ "Z6" ] = ["Basic Zed Behavior Patterns", [], "Z",
                "Skills: CSx2, Neurobio x3",
"""
Bring any member of the Military who has been in a fight with a Zed
(either in-game or during the crisis) to the Lab with you, and
interview them for five minutes about their recollections of fighting
Zed.
"""
]
tech[ "Z7" ] = ["Intermediate Zed Thought Patterns", ["Z1"], "Z"]
tech[ "Z8" ] = ["Intermediate Zed Animation Process", ["Z1", "Z2"], "Z"]
tech[ "Z9" ] = ["Intermediate Zed Recovery Process", ["Z2", "Z3"], "Z"]
tech[ "Z10" ] = ["Basic Zed Immortality", ["Z3", "Z4"], "Z"]
tech[ "Z11" ] = ["Intermediate Zed Digestion Process", ["Z4", "Z5"], "Z"]
tech[ "Z12" ] = ["Intermediate Zed Infection Patterns", ["Z5", "Z6"], "Z"]
tech[ "Z13" ] = ["Intermediate Zed BEHAVIOR Patterns", ["Z6"], "Z"]
tech[ "Z14" ] = ["Advanced Zed Thought Patterns", ["Z7"], "Z"]
tech[ "Z15" ] = ["Advanced Zed Animation Process", ["Z7", "Z8"], "Z"]
tech[ "Z16" ] = ["Advanced Zed Recovery Process", ["Z8", "Z9"], "Z"]
tech[ "Z17" ] = ["Intermediate Zed Immortality", ["Z9", "Z10"], "Z"]
tech[ "Z18" ] = ["Advanced Zed Digestion Process", ["Z10", "Z11"], "Z"]
tech[ "Z19" ] = ["Advanced Zed Infection Patterns", ["Z11", "Z12"], "Z"]
tech[ "Z20" ] = ["Basic Z1 Transmission Vectors", ["Z12", "Z13"], "Z"]
tech[ "Z21" ] = ["Advanced Zed Behavior Patterns", ["Z13"], "Z"]
tech[ "Z22" ] = ["Expert Zed Thought Patterns", ["Z14"], "Z"]
tech[ "Z23" ] = ["Expert Zed Animation Process", ["Z14", "Z16"], "Z"]
tech[ "Z24" ] = ["Expert Zed Recovery Process", ["Z15", "Z16"], "Z"]
tech[ "Z25" ] = ["Advanced Zed Immortality", ["Z15", "Z17"], "Z"]
tech[ "Z26" ] = ["Expert Zed Digestion Process", ["Z17", "Z19"], "Z"]
tech[ "Z27" ] = ["Expert Zed Infection Patterns", ["Z18", "Z19"], "Z"]
tech[ "Z28" ] = ["Intermediate Z1 Transmission Vectors", ["Z18", "Z21"], "Z"]
tech[ "Z29" ] = ["Expert Zed Behavior Patterns", ["Z20", "Z21"], "Z"]
tech[ "Z30" ] = ["Zed Mob Behavior", ["Z20"], "Z"]
tech[ "Z31" ] = ["Z1 Neurochemistry", ["Z22", "Z24"], "Z"]
tech[ "Z32" ] = ["Human Adaptation of Zed Characteristics", ["Z23", "Z25"], "Z"]
tech[ "Z33" ] = ["Zed Treats", ["Z24", "Z26"], "Z"]
tech[ "Z34" ] = ["Persistence of the Ongoing Zed Hordes", ["Z25", "Z27"], "Z"]
tech[ "Z35" ] = ["Salival Carrier Pathways", ["Z26", "Z28"], "Z"]
tech[ "Z36" ] = ["Host Cooperation as Survival Trait", ["Z27", "Z29"], "Z"]
tech[ "Z37" ] = ["Zed Destruction Patterns", ["Z28", "Z30"], "Z"]
tech[ "Z38" ] = ["Z1 Biodegradation", ["Z34", "D31"], "Z"]
tech[ "Z39" ] = ["Z1 Reversal Procedures", ["Z38", "T37"], "Z"]
tech[ "Z40" ] = ["OMNI-VACCINE", ["Z32", "G28"], "Z"]
tech[ "Z41" ] = ["Z1 Origins", ["Z37", "G35"], "Z"]
tech[ "Z42" ] = ["Z1 Creation History", ["Z41"], "Z"]
tech[ "Z43" ] = ["Z1 Organism Survival", ["Z36", "D37"], "Z"]
tech[ "Z44" ] = ["Advanced Z1 Creation", ["Z43", "G14"], "Z"]
tech[ "Z45" ] = ["Pavlovian Zed Conditioning", ["Z33", "T23"], "Z"]
tech[ "Z46" ] = ["Z1 Training", ["Z45", "G22"], "Z"]
tech[ "Z47" ] = ["Nonmutagenic Z1 Creation", ["Z35", "G31"], "Z"]


for t in tech:
    try:
        nt = Tech(name=tech[t][0],
                  tree=tech[t][2])
        if len(tech[t]) > 3:

            nt.design = tech[t][3]
            nt.experiment = tech[t][4]
        nt.save()
    except Exception,e:
        print t, e

for t in tech:
    nt = Tech.objects.filter(name=tech[t][0])[0]
    for p in tech[t][1]:
        np = Tech.objects.filter(name=tech[p][0])[0]
        nt.prereqs.add(np)
    nt.save()


for c in Character.objects.all():
    m = Mail(subject="Welcome to Arcadia",
             sender=g,
             recipient = c,
             text = """
Welcome to Arcadia!  We hope you have a great time. 

If you have any concerns or questions, you can use A-mail to contact
the GMs through this interface, or email arcadia-gms@mit.edu.  Please
do let us know if there are any problems.

Good luck with game

- The GMs
""")
    m.save()


trance = [
    ["Accent", "Talk in a foreign accent of your choice for the next hour."],
    ["Diet", "For the next hour, whenever you decline any offer, claim that you're \"trying to cut back.\"."],
    ["Morse", "For the next hour, speak in telegrams. End every sentence with \"stop\" and use the shortest phrasing possible."],
    ["Joke", "For the next hour, use the phrase \"that's what she said!\" at least every 5 minutes in conversation." ],
    ["Sinister", "For the next hour, you're vaguely afraid that your left hand is out to get you. View it with extreme suspicion, and try not to enlist its help unless absolutely necessary." ],
    ["Blues", "For the next hour, you do not notice anything blue unless it is explicitly pointed out to you. Except weapons."],
    ["Mirror", "The next 30 minutes is opposite day! You must always say the exact opposite of what you mean, or as close as possible."],
    ["Bond", "For the next 30 minutes, you are a secret agent. Walk around corners with extreme suspicion and hold your hands in a fake gun position. Hum theme music when appropriate."],
    ["Broadway", "For the next 30 minutes, you live in Arcadia! The Musical! Roleplay accordingly."],
    ["Owly", "For the next hour, every conversation is a staring contest. Deny that you're doing anything strange if asked."],
    ["Mapper", "For the next hour, you may only move in straight lines. Whenever you switch direction, say your new direction out loud. (\"Left! Forward!\")"],
    ["", "For the next hour, you must attempt to imitate the mannerisms of anyone you're conversing with. Switch mannerisms only when you start talking to a new person."],
    ["Delicious!", 'For the next hour, if someone says \"drink" or "thirsty", or if you see a drink, say "I could sure go for a refreshing SWORD brand cola right now!" (Feel free to wait a little while between stimuli before repeating the phrase so it doesn\'t get irritating.)'],
    ["Refreshing!", 'For the next hour, whenever someone uses a positive adjective  that could plausibly be used to describe cola, say "Almost as (adjective) as SWORD-brand cola!" (Feel free to wait a little while between stimuli before repeating the phrase so it doesn\'t get irritating.)']
]

for t in trance:
    r = Trance(name=t[0], level=1, effects=t[1])
    r.save()


from tomorrow import tomorrow
#tomorrow()
