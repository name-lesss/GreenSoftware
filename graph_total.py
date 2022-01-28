import pandas
import os
import matplotlib.pyplot as plt
import sys

port=sys.argv[1]
print('port is:', port)

path = os.getcwd()
df = pandas.read_csv(path+"/average_language" + port + ".csv", engine='python')

language = ['java-', 'javascript-', 'python3-', 'php-', 'cs-', 'yarv-', 'c-flags-', 'c-noflags-', 'c++-flags-', 'c++-noflags-']
problems = ['Binarytrees', 'Fannkuchredux', 'Fasta', 'Mandelbrot', 'Nbody', 'Revcomp', 'Spectralnorm']
color = {0:'blue', 1:'red', 2:'green', 3:'purple', 4:'yellow', 5:'cyan', 6:'magenta', 7:'black', 8:'brown', 9:'gray'}

for i, row in df.iterrows():
    problem = []#x-as
    energy = []#y-as
    error = []#yerr
    count = 0
    for x in language:
        if x in row['Language']:
            break
        count += 1
    for k in row.keys():
        if k != 'Language' and k != 'Unnamed: 0' and row[k] != "('NaN', 'NaN')":
            problem.append(problems.index(k))
            mean, median, std, min, max = row[k].strip("()").split(',', 4)
            energy.append(float(mean))
            error.append(float(std)*float(mean)/100)

    plt.errorbar(problem, energy, yerr=error, c=color[count], fmt='.')
plt.xlabel('Languages')
plt.ylabel('Energy consumption (Joule)')
plt.xticks([0,1,2,3,4,5,6], problems)
plt.legend(language, loc='best', fontsize='small')
plt.savefig("total_overview" + port)
plt.close()
