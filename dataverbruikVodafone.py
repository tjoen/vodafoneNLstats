'''
Created on May 31, 2013

Simple csv file analyzer from the dutch vodafone website.

@author: nlaurens
'''

import os
import glob  # search for file
import csv #cvs file


# define local directory. This should be changed to relative paths.
dir_data = 'N:/Documents/Financien/Vodafone kosten/datagebruik'
dir_spraak = 'N:/Documents/Financien/Vodafone kosten/spraak'



maandDic ={} #make a dictionary so we can have str indices

#datagebruik
os.chdir(dir_data)
for files in glob.glob('*.csv'):
    verbruik = []
    maand =''
    with open(files, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            
            #catch the date
            if row[0] == 'Telefoonnummer:':
                maand = row[3].strip()
            
            if len(row)>5:
                tmp = row[4].split()
                if len(tmp) > 1:
                    if tmp[1] == 'KB':
                        tmp = str(tmp[0])
                        tmp = tmp.replace('.00', '')
                        verbruik.append( int(tmp) )
    totaalKB = sum(verbruik)
    totaalMB = totaalKB / 1024.0
    totaalGB = totaalMB / 1024.0
    maandDic[maand] = {}
    maandDic[maand]['data'] = totaalMB
     
#datagebruik
os.chdir(dir_spraak)
for files in glob.glob('*.csv'):
    verbruik = []
    maand =''
    with open(files, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:

            #catch the date
            if row[0] == 'Telefoonnummer:':
                maand = row[3].strip()
            
            if len(row)>5:
                tmp = row[5].split(':')
                if len(tmp)==3:
                    verbruik.append ( int(tmp[2]) + int(tmp[1])*60 + int(tmp[0]*3600) )

    totaalS = sum(verbruik)
    totaalM = totaalS/ 60.0
    maandDic[maand]['spraak'] = totaalM


aantalMaanden = 0

maxMin = 0
minMin = 10000
totaalMin = 0

maxData = 0
minData = 10000
totaalData = 0

for maand,verbruik in maandDic.iteritems():
    aantalMaanden = aantalMaanden + 1
    totaalMin = totaalMin + verbruik['spraak']
    maxMin = max(maxMin, verbruik['spraak'])
    minMin = min(minMin, verbruik['spraak'])    
    
    totaalData = totaalData + verbruik['data']
    maxData = max(maxData, verbruik['data'])
    minData = min(minData, verbruik['data'])
    
    print maand + '\n' + ('%.2f' % verbruik['data']) + 'MB - ' + ('%.2f' % verbruik['spraak']) + 'min' + '\n'
    
print 'totaal gebruik:'
print ('%.2f' % totaalMin)  + 'min'
print ('%.2f' % totaalMB)  + 'MB\n'

print 'Gem/Max/Min gebruik periode:'
print ('%.2f' % (totaalMin/aantalMaanden))  +' / ' + ('%.2f' % (maxMin))  + ' / ' +('%.2f' % (minMin))  +'min'
print ('%.2f' % (totaalData/aantalMaanden)) +' / ' + ('%.2f' % (maxData)) + ' / ' +('%.2f' % (minData))  +'MB\n'

    
    