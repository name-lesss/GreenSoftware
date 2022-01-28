import pandas
import os
import math
#import matplotlib.pyplot as plt

# data = pandas.read_csv('results/primes_300000.csv', sep='\s*,\s*',
#                        engine='python')

result2 = []
result3 = []
labels = ['Name', 'Joule(surface)', 'kWh(surface)', 'allJoule(surface)',
          'allkWh(surface)', 'time(ms)', 'time(string)']
#labels = ['Name', 'time(ms)', 'time(string)']

path = os.getcwd() + '/results/results'
files = []
idle2 = {}
idle3 = {}
for r, d, f in os.walk(path):
    for file in f:
        if 'start'in file or 'end' in file:
            if 'port2' in file:
                df1 = pandas.read_csv(os.path.join(r, file), sep='\s*,\s*', engine='python')
                name = file.split("count")[1].split(".")[0]
                if name in idle2.keys():
                    concat = pandas.concat((idle2[name], df1))
                    idle2[name] = concat['Power(W)'].mean()
                else:
                    idle2[name] = df1
            else:
                df1 = pandas.read_csv(os.path.join(r, file), sep='\s*,\s*', engine='python')
                name = file.split("count")[1].split(".")[0]
                if name in idle3.keys():
                    concat = pandas.concat((idle3[name], df1))
                    idle3[name] = concat['Power(W)'].mean()
                else:
                    idle3[name] = df1
        elif '.csv' in file:
            files.append(os.path.join(r, file))

print("Idle mean 2:", idle2)
print("Idle mean 3:", idle3)

for name in files:
    count = name.split(".")[-2]

    data = pandas.read_csv(name, sep='\s*,\s*', engine='python')

#    if (name == 'primes.csv'):
#        plt.scatter(data['Time(mS)'], data['Power(W)'])
#        plt.xlabel('Time (ms)')
#        plt.ylabel('Power (Watt)')
#        plt.show()

    # Calculate Duration in Milliesecond, but also nicely formated (caution
    # days/weeks/months not implemented because we know that the programs
    # are not running that long)
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

    # Calculate Energy Consumption in Joule and kWh by taking the
    # average between two points, calculating the surface and then
    # adding all the surfaces together
    allsurface = 0
    surface = 0
    for i in range(data.index[-1]):
        allsurface += (data['Power(W)'][data.index[i]] +
                    data['Power(W)'][data.index[i+1]]) / 2 * (
            data['TimeNODE(mS)'][data.index[i+1]] -
            data['TimeNODE(mS)'][data.index[i]])
        if 'port2' in name:
            surface += ((data['Power(W)'][data.index[i]] - idle2[count]) +
                    (data['Power(W)'][data.index[i+1]] - idle2[count])) / 2 * (data['TimeNODE(mS)'][data.index[i+1]] - data['TimeNODE(mS)'][data.index[i]])
        else:
            surface += ((data['Power(W)'][data.index[i]] - idle3[count]) +
                        (data['Power(W)'][data.index[i+1]] - idle3[count])) / 2 * (data['TimeNODE(mS)'][data.index[i+1]] - data['TimeNODE(mS)'][data.index[i]])
    allsurfaceJ = allsurface/1000  # Make it in Joule
    allsurfacekWh = allsurfaceJ/3600000  # Make it in kWh
    surfaceJ = surface/1000  # Make it in Joule
    surfacekWh = surfaceJ/3600000  # Make it in kWh

    # Calculate Energy Consumption in kWh by using meter
#    energyMeter = (data['Energy(kWH)'][data.index[-1]] -
#                   data['Energy(kWH)'][data.index[0]])
    # remove weird trailing numbers
#    energyMeter = round(energyMeter * 1000)/1000


    # Calculate average and median of power
#    mean = data['Power(W)'].mean()
#    median = data['Power(W)'].median()
#    stddev = data['Power(W)'].std()
    name = os.path.split(name)[1]

    if 'port2' in name:
        result2.append((name, surfaceJ, surfacekWh, allsurfaceJ, allsurfacekWh, timeMs, timeString))
    else:
        result3.append((name, surfaceJ, surfacekWh, allsurfaceJ, allsurfacekWh, timeMs, timeString))
#    if "port3" in name:#name.startswith( 'port3' ):
#        result.append((name, timeMs, timeString))
                   #result.append((name, timeMs, timeString))

    if timeMs < 7000:
        print(name, timeString)

df2 = pandas.DataFrame.from_records(result2, columns=labels)
df2.to_csv('results2.csv')
df3 = pandas.DataFrame.from_records(result3, columns=labels)
df3.to_csv('results3.csv')
#totaltime = df['time(ms)'].sum()
#print(totaltime)
#totaltimeSec = (int(totaltime / 1000) % 60)
#totaltimeMin = (int(totaltime / (1000*60)) % 60)
#totaltimeHour = (int(totaltime / (1000*60*60)) % 60)
#print(totaltimeHour, totaltimeMin, totaltimeSec)
