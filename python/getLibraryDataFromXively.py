#!/usr/bin/env python

import httplib
import urllib

import time as systime

from datetime import datetime, timedelta, date, time
import StringIO


# Cosm API key
API_KEY = 'M2CFRoL9JEmbzJMXKZgUkPbybBnr9VhTQkVeZ5K1nvSWCZhM'

# feed identifier we wish to read

# server name
server = 'api.xively.com'
feed_id = 63888
headers = {'X-ApiKey': API_KEY}

conn = httplib.HTTPConnection(server)
#conn.set_debuglevel(6)

maxinterval = timedelta(seconds =6*3600)
endtime = datetime.now()

# set a time before your first data point
initdate = date(2012,7,1)
inittime = time(8,0)
starttime = datetime.combine(initdate,inittime)
firsttime = starttime

# set the data you want to read (seemed to error out more often if requesting more that one type)
for sensor in ('force','door'):
    print sensor
    starttime = datetime.combine(initdate,inittime)
    
    outfile = open('{0:s}Data.csv'.format(sensor),'w')

    outfile.write('{0:s},{1:s}\n'.format(datetime,sensor))

    # set this number to something big enough to get all of your data
    for i in range(1000):
#        systime.sleep(3)
        print str(i)+'  '+starttime.isoformat()
        if starttime > endtime:
            break
        params = urllib.urlencode({'start':starttime.isoformat() , 'duration':'6hours', 'interval':'0','limit':1000})
        url = 'http://{0:s}/v2/feeds/{1:d}/datastreams/{2:s}.{3:s}'.format(server,feed_id,sensor,'csv')+'?'+params
#        print url
        systime.sleep(1)
        conn.request('GET', url, '', headers)
        systime.sleep(0.25)
   
        try:
            response = conn.getresponse()
        except httplib.ResponseNotReady:
            try:
                systime.sleep(1)
                response = conn.getresponse()
            except httplib.ResponseNotReady:
                continue
            continue
        
        if response.status != 200:
            # delay
            print response.status, response.reason
            systime.sleep(1)
            continue
        
        data = response.read()
        if len(data):
            log = StringIO.StringIO(data)
            for rec in log.readlines():
                timestamp,value = rec.rstrip().split(',')
                tmpdate,tmptime = timestamp.rstrip('Z').split('T')
                Y,m,d = tmpdate.split('-')
                H,M,tmpS = tmptime.split(':') 
                S,ms = tmpS.split('.')

                starttime = datetime.combine(date(int(Y),int(m),int(d)),time(int(H),int(M),int(S),int(ms)))

                #print rec,
                #outfile.write('{0:s},{1:s},{2:s}\n'.format(tmpdate,tmptime,value))
                delta = starttime - firsttime
                outfile.write('{0:s},{1:s}\n'.format(starttime.isoformat(' '),value))
#                outfile.write('{0:s}\t{1:s}\n'.format(datetime.isoformat(' '),value))

            #print ''
            # increment starttime by a single tick
            #starttime = starttime + timedelta.resolution
            starttime = starttime + timedelta(seconds=1)
        else:
            # increment starttime by 6 hrs
            print "Skipping forward:"
            starttime = starttime + maxinterval
   
    outfile.close()
