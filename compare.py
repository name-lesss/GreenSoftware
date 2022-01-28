import pandas
import os
from scipy.stats import ks_2samp
from scipy.stats import pearsonr
from scipy.stats import kendalltau
import numpy
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

path = os.getcwd()
df2 = pandas.read_csv(path + "/newresults2.csv", engine='python')
df3 = pandas.read_csv(path + "/newresults3.csv", engine='python')
df_times = pandas.read_csv(path+"/program_info.csv", engine='python')
df2_outlier = pandas.read_csv(path + "/graphs2/outlier/port2.outliers.csv", engine='python')
df3_outlier = pandas.read_csv(path + "/graphs3/outlier/port3.outliers.csv", engine='python')
df2_diff = pandas.read_csv(path + "/graphs2/timediff.csv", engine='python')

problems = {"Binarytrees":"0", "Fannkuchredux":"1", "Fasta":"2",
    "Mandelbrot":"3", "Nbody":"4", "Revcomp":"5",
        "Spectralnorm":"6"}
language = ['java', 'javascript', 'python3', 'php', 'cs', 'yarv', 'c-flags', 'c-noflags', 'c++-flags', 'c++-noflags']

total = 0
same  = 0
ptotal = {'Binarytrees':{'Java':[[],[]], 'JavaScript':[[],[]], 'Python3':[[],[]], 'PHP':[[],[]], 'Cs':[[],[]], 'Yarv':[[],[]], 'C-flags':[[],[]], 'C-noflags':[[],[]], 'C++-flags':[[],[]], 'C++-noflags':[[],[]]}, 'Fannkuchredux':{'Java':[[],[]], 'JavaScript':[[],[]], 'Python3':[[],[]], 'PHP':[[],[]], 'Cs':[[],[]], 'Yarv':[[],[]], 'C-flags':[[],[]], 'C-noflags':[[],[]], 'C++-flags':[[],[]], 'C++-noflags':[[],[]]}, 'Fasta':{'Java':[[],[]], 'JavaScript':[[],[]], 'Python3':[[],[]], 'PHP':[[],[]], 'Cs':[[],[]], 'Yarv':[[],[]], 'C-flags':[[],[]], 'C-noflags':[[],[]], 'C++-flags':[[],[]], 'C++-noflags':[[],[]]}, 'Mandelbrot':{'Java':[[],[]], 'JavaScript':[[],[]], 'Python3':[[],[]], 'PHP':[[],[]], 'Cs':[[],[]], 'Yarv':[[],[]], 'C-flags':[[],[]], 'C-noflags':[[],[]], 'C++-flags':[[],[]], 'C++-noflags':[[],[]]}, 'Nbody':{'Java':[[],[]], 'JavaScript':[[],[]], 'Python3':[[],[]], 'PHP':[[],[]], 'Cs':[[],[]], 'Yarv':[[],[]], 'C-flags':[[],[]], 'C-noflags':[[],[]], 'C++-flags':[[],[]], 'C++-noflags':[[],[]]}, 'Revcomp':{'Java':[[],[]], 'JavaScript':[[],[]], 'Python3':[[],[]], 'PHP':[[],[]], 'Cs':[[],[]], 'Yarv':[[],[]], 'C-flags':[[],[]], 'C-noflags':[[],[]], 'C++-flags':[[],[]], 'C++-noflags':[[],[]]}, 'Spectralnorm':{'Java':[[],[]], 'JavaScript':[[],[]], 'Python3':[[],[]], 'PHP':[[],[]], 'Cs':[[],[]], 'Yarv':[[],[]], 'C-flags':[[],[]], 'C-noflags':[[],[]], 'C++-flags':[[],[]], 'C++-noflags':[[],[]]}}
xtotal = {'Binarytrees':[], 'Fannkuchredux':[], 'Fasta':[], 'Mandelbrot':[], 'Nbody':[], 'Revcomp':[], 'Spectralnorm':[]}
color = {'Binarytrees':[], 'Fannkuchredux':[], 'Fasta':[], 'Mandelbrot':[], 'Nbody':[], 'Revcomp':[], 'Spectralnorm':[]}
ptotalProgram = {'Binarytrees':[], 'Fannkuchredux':[], 'Fasta':[], 'Mandelbrot':[], 'Nbody':[], 'Revcomp':[], 'Spectralnorm':[]}
for i, row in df_times.iterrows():
    total += 1
    vals2, vals3 = [], []
    filename = row['Language'].lower() + "-" + str(row['ID']) + ".problem" + problems[row['Problem']]
    for i2, row2 in df2.iterrows():
        if filename not in df2_outlier.Name.values and filename in row2['Name']:
            vals2.append(row2['Joule(surface)'])
            if len(vals2) == 22:
                break
    for i3, row3 in df3.iterrows():
        if filename not in df3_outlier.Name.values and filename in row3['Name'] and int(row3['Name'].split(".")[-2]) > 5:
            vals3.append(row3['Joule(surface)'])
            if len(vals3) == 22:
                break

    #d, p = ks_2samp(vals2, vals3)
    u1, p1 = mannwhitneyu(vals2, vals3, alternative='less')
    u2, p2 = mannwhitneyu(vals2, vals3, alternative='greater')
    if p1 >= 0.05 and p2 >= 0.05:
        same += 1
        print("Same distribution name, p:", filename, p1, p2)

#    pvals = []
#    for j in range(500):
#        temp = [x for x in vals3]
#        for i in range(5):
#            index = numpy.random.randint(len(temp))
#            del temp[index]
#
#        r, p = pearsonr(vals2, temp)
#        pvals.append(p)
#    av = numpy.average(pvals)
#    ptotal.append(av)
    r, p = pearsonr(vals2, vals3)
    tau, p = kendalltau(vals2, vals3)

    ptotal[row['Problem']][row['Language']][0].append(vals2)
    ptotal[row['Problem']][row['Language']][1].append(vals3)

    ptotalProgram[row['Problem']].append(tau)
    if row['Language'] == 'Java':
        color[row['Problem']].append('blue')
        xtotal[row['Problem']].append(0)
    elif row['Language'] == 'JavaScript':
        color[row['Problem']].append('red')
        xtotal[row['Problem']].append(1)
    elif row['Language'] == 'Python3':
        color[row['Problem']].append('green')
        xtotal[row['Problem']].append(2)
    elif row['Language'] == 'PHP':
        color[row['Problem']].append('purple')
        xtotal[row['Problem']].append(3)
    elif row['Language'] == 'Cs':
        color[row['Problem']].append('yellow')
        xtotal[row['Problem']].append(4)
    elif row['Language'] == 'Yarv':
        color[row['Problem']].append('cyan')
        xtotal[row['Problem']].append(5)
    elif row['Language'] == 'C-flags':
        color[row['Problem']].append('magenta')
        xtotal[row['Problem']].append(6)
    elif row['Language'] == 'C-noflags':
        color[row['Problem']].append('black')
        xtotal[row['Problem']].append(7)
    elif row['Language'] == 'C++-flags':
        color[row['Problem']].append('brown')
        xtotal[row['Problem']].append(8)
    elif row['Language'] == 'C++-noflags':
        color[row['Problem']].append('gray')
        xtotal[row['Problem']].append(9)


print("Total files:", total)
print("Amount of same distribution:", same)

for key in ptotal.keys():
    x, y, c = [], [], []
    for key2 in ptotal[key].keys():
        tau, p = kendalltau(ptotal[key][key2][0], ptotal[key][key2][1])
        y.append(tau)
        if key2 == 'Java':
            c.append('blue')
            x.append(0)
        elif key2 == 'JavaScript':
            c.append('red')
            x.append(1)
        elif key2 == 'Python3':
            c.append('green')
            x.append(2)
        elif key2 == 'PHP':
            c.append('purple')
            x.append(3)
        elif key2 == 'Cs':
            c.append('yellow')
            x.append(4)
        elif key2 == 'Yarv':
            c.append('cyan')
            x.append(5)
        elif key2 == 'C-flags':
            c.append('magenta')
            x.append(6)
        elif key2 == 'C-noflags':
            c.append('black')
            x.append(7)
        elif key2 == 'C++-flags':
            c.append('brown')
            x.append(8)
        elif key2 == 'C++-noflags':
            c.append('gray')
            x.append(9)
    
    plt.figure()
    plt.scatter(x, y, c=c)
    plt.xlabel("Language")
    plt.ylabel("Correlation coefficient")
    plt.xticks([0,1,2,3,4,5,6,7,8,9], language)
    plt.ylim(bottom=-1, top=1)
    plt.savefig(path + '/kendall.lang_' + key + '.png')
    plt.close()

    plt.figure()
    plt.scatter(xtotal[key], ptotalProgram[key], c=color[key])
    plt.xlabel("Language")
    plt.ylabel("Correlation coefficient")
    plt.xticks([0,1,2,3,4,5,6,7,8,9], language)
    plt.ylim(bottom=-1, top=1)
    plt.savefig(path + '/kendall_' + key + '.png')
    plt.close()
