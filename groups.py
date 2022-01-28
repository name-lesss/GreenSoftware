import sys
import os
import pandas
import matplotlib.pyplot as plt

language = sys.argv[1]
problem = sys.argv[2]
port = sys.argv[3]

path = os.getcwd()
df = pandas.read_csv(path+"/newresults" + port + ".csv", engine='python')
df_outlier = pandas.read_csv(path + "/graphs" + port + "/outlier/port" + port + ".outliers.csv", engine='python')

values = {}
id = []
for i, row in df.iterrows():
    if (language + '-') in row['Name'] and problem in row['Name'] and ('port' + port) in row['Name'] and row['Name'] not in df_outlier.Name.values:
        name = ".".join(row['Name'].split(".", 3)[:3])
        if name in values.keys():
            values[name].append(row['Joule(surface)'])
        else:
            values[name] = [row['Joule(surface)']]
            id.append(name.split('.', 2)[1][-1])

data = []
for x in values.keys():
    plt.scatter([int(x.split('.', 2)[1][-1])] * len(values[x]), values[x], c='b', marker='.')
    data.append(values[x])
plt.xlabel('Programs')
plt.ylabel('Energy consumption (Joule)')
#plt.xticks(values.keys(), id)
plt.ylim(bottom=0)
plt.savefig(path + "/graphs" + port + "/Group." + language + "." + problem + "." + port + ".png")

plt.figure()
plt.boxplot(data)
plt.xlabel('Program ID')
plt.ylabel('Energy consumption (Joule)')
plt.ylim(bottom=0)
#print([i for i in range(1, len(data)+1)], id)
plt.xticks([i for i in range(1, len(data)+1)], id)
plt.savefig(path + "/graphs" + port + "/BOXGroup." + language + "." + problem + "." + port + ".png")
plt.close()
