import pandas
import os
import numpy
import sys
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.stats import shapiro
from scipy.stats import ks_2samp
from scipy.stats import mannwhitneyu
from scipy.stats import ttest_ind

port=sys.argv[1]
test=sys.argv[2]
print('port is:', port)
print('test is:', test)
#Test 1 is comparing two distributions (ks 2 sample test)
#Test 2 is finding outliers (dbscan)
#Test 3 is checking if normally distributed (shapiro wilkens test)
#Test 4 is clustering (kmeans)
#Test 5 is comparing two means (mann whitney u test)

path = os.getcwd()
df = pandas.read_csv(path + "/newresults" + port + ".csv", engine='python')
df_times = pandas.read_csv(path+"/program_info.csv", engine='python')
df_outlier = pandas.read_csv(path + "/graphs" + port + "/outlier/port" + port + ".outliers.csv", engine='python')

if port == "2":
    count = 22
else:
    count = 27#to make it stop searching if have found all
problems = {"Binarytrees":"0", "Fannkuchredux":"1", "Fasta":"2",
    "Mandelbrot":"3", "Nbody":"4", "Revcomp":"5",
        "Spectralnorm":"6"}

total = []
totalnames = []
allnames = []
for i, row in df_times.iterrows():
    rows = []
    filename = row['Language'].lower() + "-" + str(row['ID']) + ".problem" + problems[row['Problem']]
    for i2, row2 in df.iterrows():
        if filename in row2['Name']:
            rows.append(row2)
            if len(rows) == count:
                break

    data = []
    names = []
    for r in rows:
        data.append([r['time(ms)'], float('%.3g' % r['Joule(surface)'])])
        names.append(r['Name'])
    total.append(data)
    totalnames.append(filename)
    allnames.append(names)

#test if two programs energy consumption come from the same distribution
#using Kolmogorov–Smirnov test
if test == '1':
    samedist = []
    count = 0
    for d1 in total:
        for i2 in range(total.index(d1)+1, len(total)):
            name1 = totalnames[total.index(d1)]
            name2 = totalnames[i2]
            if name1.split(".")[1] == name2.split(".")[1] and (name1.split(".")[0]).split("-", 2)[:-1] == (name2.split(".")[0]).split("-", 2)[:-1]:
                value1 = []
                for point in range(len(d1)):
                    if allnames[total.index(d1)][point] not in df_outlier.Name.values:
                        value1.append(d1[point][1])
                value2 = []
                for point in range(len(total[i2])):
                    if allnames[i2][point] not in df_outlier.Name.values:
                        value2.append(total[i2][point][1])
                d, p = ks_2samp(value1, value2)
                if p >= 0.05:
                    print("Same distribution:", name1, name2, d, p)
                    count += 1
                    plt.figure()
                    plt.subplot(211)
                    y1 = [y[1] for y in d1]
                    y2 = [y[1] for y in total[i2]]
                    y1.sort()
                    y2.sort()
                    plt.scatter([x for x in range(len(d1))], y1, c='b', marker='.')
                    plt.scatter([x for x in range(len(total[i2]))], y2, c='r', marker='.')
                    plt.xlabel('ID')
                    plt.ylabel('Energy consumption (Joule)')
                    plt.ylim(bottom=0)
                    
                    plt.subplot(212)
                    plt.scatter([x[0] for x in d1], [y[1] for y in d1], c='b', marker='.')
                    plt.scatter([x[0] for x in total[i2]], [y[1] for y in total[i2]], c='r', marker='.')
                    plt.xlabel('Run-time (Seconds)')
                    plt.ylabel('Energy consumption (Joule)')
                    plt.ylim(bottom=0)
                    plt.xlim(left=0)
                    plt.savefig(path + '/graphs' + port + '/samedist/port' + port + '.' + name1 + '-' + name2 + '.png')
                    plt.close()
                    
                    samedist.append([name1, name2, d, p])
    print("The amount of programs that have the same distribution:", count)

    df = pandas.DataFrame.from_records(samedist, columns=['Program1', 'Program2', 'd', 'p'])
    df.to_csv(path + '/graphs' + port + '/samedist/port' + port + 'same_distribution.csv')
    

        #1d outlier/anomaly check
#        for r in rows:
#            zscore = abs(numpy.mean(data) - r['Joule(surface)']) / numpy.std(data)
#            if zscore >= 2.5:
#                print("Outlier:", r['Name'], zscore)
#
#        #1d normal dist check
#        data.sort()
#        stat, p = shapiro(data)
#        if p <= 0.05:
#            pass
                #print(filename, stat, p)

elif test == '2':
    count1clust = 0
    count2clust = 0
    countMulticlust = 0
    countTime = 0
    countSame = 0
    Same = 0
    diff = []
    results = []
    minPts = 4
    
    for d in total:
        data = StandardScaler().fit_transform(d)
        data = [[x[0],x[1]] for x in data]
        kdist = []
        for p in data:
            dist = []
            for p2 in data:
                if p != p2:
                    dist.append(numpy.sqrt((p[0]-p2[0])**2 + (p[1]-p2[1])**2))
            dist.sort()
            kdist.append(dist[minPts-1])

        #calc eps for outlier check
        slopes = []
        kdist.sort(reverse=True)
        for k in range(1, len(kdist)):
            slopes.append(abs(kdist[k]-kdist[k-1]))
        div = 0.15
        eps = 1
        index = -1
        for l in range(len(slopes)-1):
            if abs(slopes[l] - slopes[l+1]) >= div:
                div = abs(slopes[l] - slopes[l+1])
                eps = kdist[l+1]
                index = l
        if index == -1:
            color = ['b' for i in range(len(kdist))]
            shape = ['.' for i in range(len(kdist))]
        else:
            color = ['b' for i in range(index+1)] + ['r'] + ['b' for i in range(len(slopes)-1-index)]
            shape = ['.' for i in range(index+1)] + ['x'] + ['.' for i in range(len(slopes)-1-index)]
    
        plt.figure()
        plt.subplot(212)
        for i in range(len(kdist)):
            plt.scatter(i, kdist[i], c=color[i], marker=shape[i])
        plt.xlabel("ID")
        plt.ylabel("eps")

        #2d outlier/anomaly check
        cluster = DBSCAN(eps=eps, min_samples=minPts, metric='euclidean').fit(data)
        label = cluster.labels_
        color = []
        shape = []
        for q in range(len(data)):
            if label[q] == -1:
                color.append('r')
                shape.append('x')
                results.append([allnames[total.index(d)][q], eps, d[q][0], d[q][1]])
            elif label[q] == 0:
                color.append('b')
                shape.append('.')
            elif label[q] == 1:
                color.append('g')
                shape.append('.')
            elif label[q] == 2:
                color.append('y')
                shape.append('.')
            elif label[q] == 3:
                color.append('c')
                shape.append('.')
            else:
                color.append('b')
                shape.append('.')
    
        plt.subplot(211)
        for i in range(len(d)):
            plt.scatter(d[i][0], d[i][1], c=color[i], marker=shape[i])
        plt.xlabel('time(s)')
        plt.ylabel('Joule(surface)')
        plt.ylim(bottom=0)
        plt.xlim(left=0)
        plt.savefig(path + "/graphs" + port + "/outlier/port" + port + ".bdscan." + totalnames[total.index(d)] + ".eps" + str(int(eps*100)/100) + ".png")
        plt.close()
        
        
        val1, val2 = [], []
        for j in range(len(d)):
            #20 for node28, 13 for node29
            if  int(allnames[total.index(d)][j].split(".")[-2]) >= 13:
                val1.append(d[j][1])
            else:
                val2.append(d[j][1])
        #d2, p2 = ks_2samp(val1, val2)
        u1, p1 = mannwhitneyu(val1, val2, alternative='less')
        u2, p2 = mannwhitneyu(val1, val2, alternative='greater')
        if p1 >= 0.05 and p2 >= 0.05:
            Same += 1

        if 0 in label and 1 in label and 2 not in label:
            count2clust += 1
            group1, value1 = [], []
            group2, value2 = [], []
            for i in range(len(label)):
                if label[i] == 0:
                    group1.append(int(allnames[total.index(d)][i].split(".")[-2]))
                    value1.append(d[i][1])
                if label[i] == 1:
                    group2.append(int(allnames[total.index(d)][i].split(".")[-2]))
                    value2.append(d[i][1])
        
            #20 for node28, 13 for node29
            if (max(group1) < 13 and min(group2) >= 13) or (max(group2) < 13 and min(group1) >= 13):
                countTime += 1
                diff.append([totalnames[total.index(d)]])
                #d, p = ks_2samp(value1, value2)
                u1, p1 = mannwhitneyu(value1, value2, alternative='less')
                u2, p2 = mannwhitneyu(value1, value2, alternative='greater')
                if p1 >= 0.05 and p2 >= 0.05:
                    countSame += 1
            else:
                print(group1, group2)
        elif 1 not in label:
            count1clust += 1
        else:
            countMulticlust += 1
                
    df_outliers = pandas.DataFrame.from_records(results, columns=['Name', 'Eps', 'Time', 'Energy'])
    df_outliers.to_csv(path + "/graphs" + port + "/outlier/port" + port + ".outliers.csv")
    df_diff = pandas.DataFrame.from_records(diff, columns=['Name'])
    df_diff.to_csv(path + "/graphs" + port + "/timediff.csv")

    print('1 cluster:', count1clust)
    print('2 clusters:', count2clust)
    print('The amount of 2 clusters that follow date:', countTime)
    print('The amount of 2 clusters that follow date and have the same distribution:', countSame)
    print('The that have same distribution for different date:', Same)
    print('multiple clusters:', countMulticlust)

elif test == '3':
    notNormalE = 0
    notNormalT = 0
    for d in total:
        dataE = []
        dataT = []
        for point in range(len(d)):
            if allnames[total.index(d)][point] not in df_outlier.Name.values:
                dataE.append(d[point][1])
                dataT.append(d[point][0])

        dataE.sort()
        dataT.sort()
        statE, pE = shapiro(dataE)
        statT, pT = shapiro(dataT)
        if pE < 0.01:
            #print(pE, statE)
            notNormalE += 1
        if pT < 0.01:
            notNormalT += 1
            #print(filename, stat, p)

    print("notNormal energy:", notNormalE)
    print("notNormal time:", notNormalT)
    print("Total:", len(total))

elif test == '4':
    groupTime = 0
    countSame = 0
    diff = []
    
    for d in total:
        data = []
        for point in range(len(d)):
            if allnames[total.index(d)][point] not in df_outlier.Name.values:
                data.append(d[point])

        kmeans = KMeans(n_clusters=2).fit(data)
        labelK = list(kmeans.labels_)
        color = []
        group1 = []
        group2 = []
        value1 = []
        value2 = []
        for i in range(len(labelK)):
            if labelK[i] == 1:
                color.append('b')
                group1.append(int(allnames[total.index(d)][i].split(".")[-2]))
                value1.append(d[i][1])
            else:
                color.append('r')
                group2.append(int(allnames[total.index(d)][i].split(".")[-2]))
                value2.append(d[i][1])

        plt.figure()
        plt.scatter([x[0] for x in data], [y[1] for y in data], c=color, marker='.')
        plt.xlabel('time(s)')
        plt.ylabel('Joule(surface)')
        plt.ylim(bottom=0)
        plt.xlim(left=0)
        plt.savefig(path + "/graphs" + port + "/cluster/port" + port + ".kmeans." + totalnames[total.index(d)] + ".png")
        plt.close()

        if port == '2':
            if (min(group1) >= 13 and max(group2) < 15) or (min(group2) >= 13 and max(group1) < 15):
                groupTime += 1
                diff.append([totalnames[total.index(d)]])
                #d, p = ks_2samp(value1, value2)
                u1, p1 = mannwhitneyu(value1, value2, alternative='less')
                u2, p2 = mannwhitneyu(value1, value2, alternative='greater')
                if p1 >= 0.05 and p2 >= 0.05:
                    countSame += 1
        if port == '3':
            if (min(group1) >= 18 and max(group2) < 20) or (min(group2) >= 18 and max(group1) < 20):
                groupTime += 1
                diff.append([totalnames[total.index(d)]])
                #d, p = ks_2samp(value1, value2)
                u1, p1 = mannwhitneyu(value1, value2, alternative='less')
                u2, p2 = mannwhitneyu(value1, value2, alternative='greater')
                if p1 >= 0.05 and p2 >= 0.05:
                    countSame += 1

    print("The amount of 2 clusters based on measure moment are:", groupTime)
    print("The amount of 2 clusters that are cluster on measure moment and follow the same distribution are:", countSame)

    df_diff = pandas.DataFrame.from_records(diff, columns=['Name'])
    df_diff.to_csv(path + "/graphs" + port + "/timediff.csv")

elif test == '5':
    samedist = []
    samedist2 = []
    count = 0
    count2 = 0
    countTest = 0
    for d1 in total:
        for i2 in range(total.index(d1)+1, len(total)):
            name1 = totalnames[total.index(d1)]
            name2 = totalnames[i2]
            if name1.split(".")[1] == name2.split(".")[1] and (name1.split(".")[0]).split("-", 2)[:-1] == (name2.split(".")[0]).split("-", 2)[:-1]:
                value1 = []
                for point in range(len(d1)):
                    if allnames[total.index(d1)][point] not in df_outlier.Name.values:
                        value1.append(d1[point][1])
                value2 = []
                for point in range(len(total[i2])):
                    if allnames[i2][point] not in df_outlier.Name.values:
                        value2.append(total[i2][point][1])
            
                u1, p1 = mannwhitneyu(value1, value2, alternative='less')
                u2, p2 = mannwhitneyu(value1, value2, alternative='greater')
                s, p = ks_2samp(value1, value2)
                countTest += 1
                if p1 >= 0.05 and p2 >= 0.05:
                    #print("Same median:", name1, name2, p1, p2)
                    count += 1
                    if p > 0.05:
                        count2 += 1
                        samedist2.append([name1, name2, p])
                    plt.figure()
                    plt.subplot(211)
                    y1 = [y[1] for y in d1]
                    y2 = [y[1] for y in total[i2]]
                    y1.sort()
                    y2.sort()
                    plt.scatter([x for x in range(len(d1))], y1, c='b', marker='.')
                    plt.scatter([x for x in range(len(total[i2]))], y2, c='r', marker='.')
                    plt.xlabel('ID')
                    plt.ylabel('Energy consumption (Joule)')
                    plt.ylim(bottom=0)
                    
                    plt.subplot(212)
                    plt.scatter([x[0] for x in d1], [y[1] for y in d1], c='b', marker='.')
                    plt.scatter([x[0] for x in total[i2]], [y[1] for y in total[i2]], c='r', marker='.')
                    plt.xlabel('Run-time (Seconds)')
                    plt.ylabel('Energy consumption (Joule)')
                    plt.ylim(bottom=0)
                    plt.xlim(left=0)
                    plt.savefig(path + '/graphs' + port + '/samedist/port' + port + '.mann.' + name1 + '-' + name2 + '.png')
                    plt.close()
                    
                    samedist.append([name1, name2, p1, p2])
    print("The amount of programs that have the same distribution:", count)
    print("Total count:", countTest)

    df = pandas.DataFrame.from_records(samedist, columns=['Program1', 'Program2', 'p1', 'p2'])
    df.to_csv(path + '/graphs' + port + '/samedist/port' + port + 'same_distribution.csv')

    print("The amount of programs that have the same distribution:", count2)

    df2 = pandas.DataFrame.from_records(samedist2, columns=['Program1', 'Program2', 'p'])
    df2.to_csv(path + '/graphs' + port + '/samedist/port' + port + 'same_distribution2.csv')


#use 2 for secondary clusters and len(total)/2 otherwise
#    cluster = DBSCAN(eps=0.3, min_samples=len(total)/2, metric='euclidean').fit([[x[0]/max(totaltime),x[1]/max(total)] for x in data])
#    label = cluster.labels_
#    if -1 in label:


#        plt.figure()
#        kdist.sort()
#        plt.scatter([i for i in range(len(kdist))], kdist, c='b', marker='.')
#        plt.ylim(bottom=0)
#        plt.savefig(path + "/outlier" + port + "/kdist" + filename + ".png")
#        plt.close()

#    kmeans = KMeans(n_clusters=2).fit(data)
#    labelK = list(kmeans.labels_)
#    print("toch wel", labelK)
#    if labelK.count(1) < 3 or labelK.count(0) < 3:
#        print("Kmeans", labelK, filename)
#        file = open("/outlier" + port + "/kmeans.txt", "a")
#        file.write("Kmeans " + str(labelK) + " " + filename + "\n")
#        file.close()
