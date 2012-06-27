import serial
import sys
import time
import tweepy
import urllib2


## defaults
serialPortName = '/dev/tty.usbserial';

## twitter auth
OAuthConsumerKey = "";
OAuthConsumerSecret = "";
AccessToken = "";
AccessTokenSecret = "";

#cosm auth
cosmAuthKey = ""
feedid = ""

## parse commandline args

if (len(sys.argv) > 1):
  serialPortName = sys.argv[1];

print "serial port :" + serialPortName;

if (len(sys.argv) > 6):
  OAuthConsumerKey = sys.argv[2];
  OAuthConsumerSecret = sys.argv[3];
  AccessToken = sys.argv[4];
  AccessTokenSecret = sys.argv[5];
  cosmAuthKey = sys.argv[6];
  feedid = sys.argv[7];

    

# test send tweet
auth = tweepy.OAuthHandler(OAuthConsumerKey, OAuthConsumerSecret)
auth.set_access_token(AccessToken, AccessTokenSecret)
api = tweepy.API(auth)
timestamp = str(time.time() * 1000)
tweet = 'test' + timestamp
print tweet
#api.update_status( tweet )


# test cosm update
# curl --request PUT      --data '{ "version":"1.0.0", "datastreams":[{"id":"door", "current_value":"0"}] }'      --header "X-ApiKey: 
#--verbose      http://api.cosm.com/v2/feeds/63853
opener = urllib2.build_opener(urllib2.HTTPHandler)


doorState = "0" 
ser = serial.Serial(serialPortName,9600);
##print ser.portstr
while 1:
  inBuffer =  ser.readline()
  if (inBuffer.count(":") > 0):
    data = inBuffer.split(':')
    doorState = data[0]
    if (len(data) > 1):
      value = data[1].strip()
      
      if (doorState == '0'):
        print "CLOSED: " + inBuffer
      else:
        print "OPEN: " + inBuffer


      json = '{ "version":"1.0.0", "datastreams":[{"id":"door", "current_value":"'+doorState+'"},{"id":"force", "current_value":"'+value+'"}] }'
      print json
      request = urllib2.Request('http://api.cosm.com/v2/feeds/'+feedid, data=json)
      request.add_header('X-ApiKey', cosmAuthKey)
      request.get_method = lambda: 'PUT'
      url = opener.open(request)
