import pandas
import os
import matplotlib.pyplot as plt
import sys

port=sys.argv[1]
print('port is:', port)

path = os.getcwd()
df = pandas.read_csv(path+"/average_file" + port + ".csv", engine='python')

language = ['java-', 'javascript-', 'python3-', 'php-', 'cs-', 'yarv-', 'c-flags-', 'c-noflags-', 'c++-flags-', 'c++-noflags-']
problems = ['problem0', 'problem1', 'problem2', 'problem3', 'problem4', 'problem5', 'problem6']

for p in problems:
    plt.figure()
    lang = []#language
    energy = []#energy
    error = []
    for i, row in df.iterrows():
        if p in row['Name']:
            count = 0
            for x in language:
                if x in row['Name']:
                    lang.append(count)
                    energy.append(row['Average(joule)'])
                    error.append(row['Standart deviation(J)'])
                count += 1
    plt.errorbar(lang, energy, yerr=error, ecolor='k', c='b', fmt='.')
    plt.xlabel('Languages')
    plt.ylabel('Energy consumption (Joule)')
    plt.xticks([0,1,2,3,4,5,6,7,8,9], language)
    if p == 'problem0':
        plt.savefig(path + "/graphs" + port + "/binarytrees_file" + port)
    elif p == 'problem1':
            plt.savefig(path + "/graphs" + port + "/fannkuchredux_file" + port)
    elif p == 'problem2':
        plt.savefig(path + "/graphs" + port + "/fasta_file" + port)
    elif p == 'problem3':
            plt.savefig(path + "/graphs" + port + "/mandelbrot_file" + port)
    elif p == 'problem4':
        plt.savefig(path + "/graphs" + port + "/nbody_file" + port)
    elif p == 'problem5':
            plt.savefig(path + "/graphs" + port + "/revcomp_file" + port)
    elif p == 'problem6':
        plt.savefig(path + "/graphs" + port + "/spectralnorm_file" + port)
    plt.close()
