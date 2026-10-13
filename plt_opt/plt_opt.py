font1 = {'weight':'bold', 'size':9}
font2 = {'weight':'regular', 'size':9}

import argparse
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('File')
args = parser.parse_args()
file = args.File

#Data
Routes=[]
rx_id=0
with open(file, 'r') as sample:
    A=[]
    for line in sample:
        A.append(line.replace('\n','').split('	'))
        if A[-1][0]=='':
            rx_id+=1
            Routes.append('Route_{0:02}'.format(rx_id))

M=[]
for m in A[0]:
    M.append([m])
for a in A[1:]:
    for i in range(len(a)):
        M[i].append(a[i])

Energies=dict()
for r in Routes:
    Energies[r]=dict()
    for m in M:
        Energies[r][m[0]]=[]

for m in M:
    rx_id=1
    r_name='Route_{0:02}'.format(rx_id)
    ene=[]
    R=dict()
    for i in m[2:]:
        if i=='':
            Energies[r_name][m[0]]=ene
            rx_id+=1
            r_name='Route_{0:02}'.format(rx_id)
            ene=[]
        else:
            ene.append(float(i))
    Energies[r_name][m[0]]=ene

#Plot
x_init=0.5
lev_l=1
con_l=0.25
lev_w=1.5
con_w=1
#colors=['tab:blue','blue','tab:red','red','tab:green']
colors=plt.get_cmap('plasma', len(Energies[r])*2+1)
# font1 = {'family':'Sans','weight':'bold','size':15}
# plt.rcParams['font.family'] = 'Sans'
# plt.rcParams['font.size'] = 8
# plt.rcParams['font.weight'] = 'bold'
plt.rcParams['font.size'] = font2['size']
plt.rcParams['font.weight'] = font2['weight']

for r in Energies:
    color_id=0
    # fig, ax = plt.subplots(figsize=(17./2.54,7/2.54))
    fig, ax = plt.subplots(figsize=(14/2.54,7.88/2.54))
    

    for m in Energies[r]:
        data=Energies[r][m]
        #level
        x_0=x_init
        x_1=x_0+lev_l
        y_0=data[0]
        y_1=y_0
        ax.plot([x_0, x_1], [y_0, y_1], lw=lev_w, color=colors(color_id), label=m)
        for i in data[1:]:
            #connector
            x_0=x_1
            x_1+=con_l
            y_0=y_1
            y_1=i
            ax.plot([x_0, x_1], [y_0, y_1], lw=con_w, color=colors(color_id), linestyle='dotted')
            #level
            x_0=x_1
            x_1+=lev_l
            y_0=y_1
            ax.plot([x_0, x_1], [y_0, y_1], lw=lev_w, color=colors(color_id))
        color_id+=2
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    # ax.axes.get_xaxis().set_visible(False)
    # ax.spines['left'].set_visible(False)
    ax.set_ylabel('Energy [kJ mol$^{-1}$]', fontdict=font1)
    ax.set_xlabel('Reaction step', fontdict=font1)
    # rx_steps = [i for i in range(1, len(Energies[r][m])+1)]
    # ax.set_xticks(rx_steps)
    # ax.set_xticklabels(rx_steps)
    ax.set_xlim(0,12)
#######333
    n = len(next(iter(Energies[r].values())))
    tick_pos = [x_init + lev_l/2 + i*(lev_l + con_l) for i in range(n)]
    ax.set_xticks(tick_pos)
    ax.set_xticklabels(range(1, n + 1))
##########
    # print([range(1, len(Energies[r][m])+1)])
    # print(a)
    # exit()
    #ax.set_ylim()
    ax.legend()#loc='upper right')
    # ax.ticklabel_format(useOffset=False)
    plt.tight_layout()
    #plt.show()
    plt.savefig('{0}-{1}{2}'.format(file.replace('.txt',''),r,'.svg'), format='svg')
