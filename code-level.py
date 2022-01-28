import pandas
import os
import math
import matplotlib.pyplot as plt
from scipy.stats import mannwhitneyu

path = os.getcwd() + '/results/results2'
files = []
dfs = []
for r, d, f in os.walk(path):
    for file in f:
        if 'idle' in file:
            df = pandas.read_csv(os.path.join(r, file), sep='\s*,\s*', engine='python')
            dfs.append(df)
        elif '.csv' in file:
            files.append(os.path.join(r, file))

concat = pandas.concat((dfs[0], dfs[1]))
idle = concat['Power(W)'].mean()
print(idle)

result = []
for name in files:
    data = pandas.read_csv(name, sep='\s*,\s*', engine='python')

    timeMs = data['TimeNODE(mS)'][data.index[-1]] - data['TimeNODE(mS)'][data.index[0]]
    if math.isnan(timeMs):
        print('NaN', name)
        break
    milli = timeMs % 1000
    sec = (int(timeMs / 1000) % 60)
    min = (int(timeMs / (1000*60)) % 60)
    hour = (int(timeMs / (1000*60*60)) % 60)
    timeString = str(hour) + " Hours, " + str(min) + " Minutes, " + \
        str(sec) + " Seconds, " + str(milli) + " Milliseconds"

    allsurface = 0
    surface = 0
    for i in range(data.index[-1]):
        allsurface += (data['Power(W)'][data.index[i]] +
                       data['Power(W)'][data.index[i+1]]) / 2 * (data['TimeNODE(mS)'][data.index[i+1]] - data['TimeNODE(mS)'][data.index[i]])
        surface += ((data['Power(W)'][data.index[i]] - idle) +
            (data['Power(W)'][data.index[i+1]] - idle)) / 2 * (data['TimeNODE(mS)'][data.index[i+1]] - data['TimeNODE(mS)'][data.index[i]])
    allsurfaceJ = allsurface/1000  # Make it in Joule
    allsurfacekWh = allsurfaceJ/3600000  # Make it in kWh
    surfaceJ = surface/1000  # Make it in Joule
    surfacekWh = surfaceJ/3600000  # Make it in kWh

    result.append((name, surfaceJ, surfacekWh, allsurfaceJ, allsurfacekWh, timeMs, timeString))

labels = ['Name', 'Joule(surface)', 'kWh(surface)', 'allJoule(surface)',
          'allkWh(surface)', 'time(ms)', 'time(string)']
df = pandas.DataFrame.from_records(result, columns=labels)
df.to_csv('results.code-level.csv')

rfor, rwhile, rsameline, rdiffline = [], [], [], []
for r in result:
    name = r[0].split(".")[1]
    if name == 'for':
        rfor.append(r[1])
    elif name == 'while':
        rwhile.append(r[1])
    elif name == 'sameline':
        rsameline.append(r[1])
    elif name == 'diffline':
        rdiffline.append(r[1])
    else:
        print("not in category")

plt.figure()
plt.boxplot([rfor, rwhile, rsameline, rdiffline])
plt.xlabel('Program')
plt.ylabel('Energy consumption (Joule)')
plt.ylim(bottom=0)
plt.xticks([i for i in range(1, 5)], ['for', 'while', 'sameline', 'diffline'])
plt.savefig(os.getcwd() + "/codelevel.png")
plt.close()

u1, p1 = mannwhitneyu(rfor, rwhile, alternative='less')
u2, p2 = mannwhitneyu(rfor, rwhile, alternative='greater')
print("For compared to While", p1, p2)

u1, p1 = mannwhitneyu(rsameline, rdiffline, alternative='less')
u2, p2 = mannwhitneyu(rsameline, rdiffline, alternative='greater')
print("Sameline compared to Diffline", p1, p2)
