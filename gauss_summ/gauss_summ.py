import argparse
from sys import stdout
parser=argparse.ArgumentParser()
parser.add_argument("filenames", nargs='+', help="Lista de archivos a procesar")
parser.add_argument("-e", "--energy", action='store_true', help="Display only energy")
parser.add_argument("-c", "--coordinates", action='store_true', help="Write file with optimized coordinates")
args=parser.parse_args()
filenames=args.filenames

atoms=[
    'H',  'He', 'Li', 'Be', 'B',  'C',  'N',  'O',  'F',  'Ne',
    'Na', 'Mg', 'Al', 'Si', 'P',  'S',  'Cl', 'Ar', 'K',  'Ca',
    'Sc', 'Ti', 'V',  'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
    'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y',  'Zr',
    'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn',
    'Sb', 'Te', 'I',  'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd',
    'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',
    'Lu', 'Hf', 'Ta', 'W',  'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
    'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th',
    'Pa', 'U',  'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm',
    'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds',
    'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'
]

namelen=0
for filename in filenames:
    namelen=max(namelen,len(filename))

for filename in filenames:
    starter=False
    ender=False
    logsumm=""
    with open(filename, 'r') as logfile:
        for logline in logfile:
            if not starter and (len(logline)==72) and ('\\' in logline):
                starter=True
            if starter and not ender:
                logsumm+=logline.strip()
                if '@' in logline:
                    ender=True
    if logsumm=='':
#        print(f'{filename.ljust(namelen," ")}  No information found')
        print(f'{filename} No information found')
        continue
    loglist=logsumm.split("\\")
    if not args.energy:    #1. prints complete summary
        print ('\n'+filename)
        for i in loglist[:-2]:
            print (i.replace('=','= '))
    elif args.energy:
#        outtxt=filename.ljust(namelen+1," ")  #2. prints only energy
        outtxt=filename.replace('.log','').replace('/',' ')
        for i in loglist:
            if ("HF" in i) and ("=" in i):
#                outtxt+=" "+i.ljust(18," ")
                outtxt+=" "+i
        print (outtxt.replace('=','= '))
    if args.coordinates:
        coords=[]
        for i in loglist:
            coormap=i.split(",")
            if len(coormap)==4 and coormap[0] in atoms:
                coords.append(coormap)
        with open(filename.replace(".log",".xyz"), 'w') as trajfile:
            trajfile.write(str(len(coords))+'\n')
            trajfile.write('\n')
            for i in coords:
                trajfile.write('  '+i[0].ljust(4,' ')+i[1].rjust(16,' ')+i[2].rjust(16,' ')+i[3].rjust(16,' ')+'\n')
    stdout.flush()

