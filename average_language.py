import pandas
import os
import numpy
import matplotlib.pyplot as plt
import sys
from scipy.stats import mannwhitneyu
from scipy.stats import ks_2samp

port=sys.argv[1]
print('port is:', port)

path = os.getcwd()
df = pandas.read_csv(path+"/newresults" + port + ".csv", engine='python')
df_outlier = pandas.read_csv(path + "/graphs" + port + "/outlier/port" + port + ".outliers.csv", engine='python')

result = []
labels = ['Language', 'Binarytrees', 'Fannkuchredux', 'Fasta', 'Mandelbrot', 'Nbody', 'Revcomp', 'Spectralnorm']
language = ['java-', 'javascript-', 'python3-', 'php-', 'cs-', 'yarv-', 'c-flags-', 'c-noflags-', 'c++-flags-', 'c++-noflags-']
problems = ['problem0', 'problem1', 'problem2', 'problem3', 'problem4', 'problem5', 'problem6']

for x in language:
    values = []
    for y in problems:
        rows = []
        for i, row in df.iterrows():
            if x in row['Name'] and y in row['Name'] and row['Name'] not in df_outlier.Name.values:
                rows.append(row['Joule(surface)'])
        if len(rows) == 0:
            values.append(("NaN", "NaN"))
        else:
            mean = '%.3g' % numpy.mean(rows)
            median = '%.3g' % numpy.median(rows)
            std = '%.3g' % ((numpy.std(rows)/numpy.mean(rows))*100)
            values.append([mean, median, std, '%.3g' % (min(rows)), '%.3g' % (max(rows))])
    result.append([x] + values)

df_al = pandas.DataFrame.from_records(result, columns=labels)
df_al.to_csv('average_language' + port + '.csv')

#graph per problem, on x-as the languages on y the energy
for y in problems:
    plt.figure()
    lang = []#languages
    energy = []#energy
    for i, row in df.iterrows():
        if y in row['Name']:
            count = 0
            for x in language:
                if x in row['Name']:
                    if row['Name'] not in df_outlier.Name.values:
                        lang.append(count)
                        energy.append(float('%.3g' % row['Joule(surface)']))
                count += 1
    plt.scatter(lang, energy, c='b', marker='.')
    plt.xlabel('Languages')
    plt.ylabel('Energy consumption (Joule)')
    plt.xticks([0,1,2,3,4,5,6,7,8,9], language)
    if y == 'problem0':
        plt.savefig(path + "/graphs" + port + "/problem/binarytrees_overview" + port)
    elif y == 'problem1':
        plt.savefig(path + "/graphs" + port + "/problem/fannkuchredux_overview" + port)
    elif y == 'problem2':
        plt.savefig(path + "/graphs" + port + "/problem/fasta_overview" + port)
    elif y == 'problem3':
        plt.savefig(path + "/graphs" + port + "/problem/mandelbrot_overview" + port)
    elif y == 'problem4':
        plt.savefig(path + "/graphs" + port + "/problem/nbody_overview" + port)
    elif y == 'problem5':
        plt.savefig(path + "/graphs" + port + "/problem/revcomp_overview" + port)
    elif y == 'problem6':
        plt.savefig(path + "/graphs" + port + "/problem/spectralnorm_overview" + port)
    plt.close()

    plt.figure()
    data = []
    for i in range(len(language)):
        col = []
        for j in range(len(lang)):
            if lang[j] == i:
                col.append(energy[j])
        data.append(col)
    plt.figure()
    plt.boxplot(data)
    plt.xlabel('Languages')
    plt.ylabel('Energy consumption (Joule)')
    plt.ylim(bottom=0)
    plt.xticks([i for i in range(1, len(data)+1)], language)
    if y == 'problem0':
        plt.savefig(path + "/graphs" + port + "/problem/binarytrees_BOXoverview" + port)
    elif y == 'problem1':
        plt.savefig(path + "/graphs" + port + "/problem/fannkuchredux_BOXoverview" + port)
    elif y == 'problem2':
        plt.savefig(path + "/graphs" + port + "/problem/fasta_BOXoverview" + port)
    elif y == 'problem3':
        plt.savefig(path + "/graphs" + port + "/problem/mandelbrot_BOXoverview" + port)
    elif y == 'problem4':
        plt.savefig(path + "/graphs" + port + "/problem/nbody_BOXoverview" + port)
    elif y == 'problem5':
        plt.savefig(path + "/graphs" + port + "/problem/revcomp_BOXoverview" + port)
    elif y == 'problem6':
        plt.savefig(path + "/graphs" + port + "/problem/spectralnorm_BOXoverview" + port)
    plt.close()

    order = []
    index = 0
    for l in data:
        meanCompare = []
        for l2 in data:
            if len(l2) == 0 or len(l) == 0:
                meanCompare.append('NaN')
            elif l == l2:
                meanCompare.append(0)
            else:
                u1, p1 = mannwhitneyu(l, l2, alternative='less')
                u2, p2 = mannwhitneyu(l, l2, alternative='greater')
                if p1 < 0.05 and p2 < 0.05:
                    meanCompare.append("Error")
                elif p1 < 0.05:
                    meanCompare.append(1)
                elif p2 < 0.05:
                    meanCompare.append(-1)
                else:
                    u3, p3 = mannwhitneyu(l, l2, alternative='two-sided')
                    if p3 < 0:
                        meanCompare.append("Undifined")
                    else:
                        meanCompare.append("?")
        print(y, index, meanCompare)
        index += 1
        order.append(meanCompare.count(-1) + 1)
    print("Order for:", y, "is", order)

