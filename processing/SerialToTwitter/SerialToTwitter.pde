import processing.serial.*;

/*
Code lifted from 
RobotGrrl.com
AND
http://www.instructables.com/id/Twittering-Laser-Tripwire-with-Webcam-Capture/

Code licensed under:
CC-BY

*/

// First step is to register your Twitter application at dev.twitter.com
// Once registered, you will have the info for the OAuth tokens
// You can get the Access token info by clicking on the button on the
// right on your twitter app's page
// Good luck, and have fun!

// This is where you enter your Oauth info
static String OAuthConsumerKey = "";
static String OAuthConsumerSecret = "";

// This is where you enter your Access Token info
static String AccessToken = "";
static String AccessTokenSecret = "";

// Just some random variables kicking around
String myTimeline;
java.util.List statuses = null;
User[] friends;
Twitter twitter = new TwitterFactory().getInstance();
RequestToken requestToken;
String[] theSearchTweets = new String[11];


//Serial Stuffs

Serial myPort;
char inBuffer;
int wait, now, timeout = 10000;
boolean hold = false;


void setup() {
  
    size(200,200);
  println(Serial.list());
  myPort = new Serial(this, Serial.list()[0], 9600);
  fill(#36ff00);
  
  

}

void draw() {
  
  while (myPort.available() > 0)
  {
    inBuffer = myPort.readChar();   

    if(inBuffer=='1')
    {      
      if ( !hold )
      {
        fill(#ff0000);
        println("Tripped");
        //open("/home/action-owl/test.meep");
        connectTwitter();
        sendTweet("Somebody is visiting our library. #payItForward");
  
        wait = millis();
        hold = true;
      }
    }
  }
  
  now = millis();
    
  if (now > (wait + timeout))
  {
    hold = false;
    fill(#36ff00);
  }
    
  rect(0,0,200,200);
}


// Initial connection
void connectTwitter() {

  twitter.setOAuthConsumer(OAuthConsumerKey, OAuthConsumerSecret);
  AccessToken accessToken = loadAccessToken();
  twitter.setOAuthAccessToken(accessToken);

}

// Sending a tweet
void sendTweet(String t) {

  try {
    Status status = twitter.updateStatus(t);
    println("Successfully updated the status to [" + status.getText() + "].");
  } catch(TwitterException e) { 
    println("Send tweet: " + e + " Status code: " + e.getStatusCode());
  }

}


// Loading up the access token
private static AccessToken loadAccessToken(){
  return new AccessToken(AccessToken, AccessTokenSecret);
}


// Get your tweets
void getTimeline() {

  try {
    statuses = twitter.getUserTimeline(); 
  } catch(TwitterException e) { 
    println("Get timeline: " + e + " Status code: " + e.getStatusCode());
  }

  for(int i=0; i<statuses.size(); i++) {
    Status status = (Status)statuses.get(i);
    println(status.getUser().getName() + ": " + status.getText());
  }

}


// Search for tweets
void getSearchTweets() {

  String queryStr = "@RobotGrrl";

  try {
    Query query = new Query(queryStr);    
    query.setRpp(10); // Get 10 of the 100 search results  
    QueryResult result = twitter.search(query);    
    ArrayList tweets = (ArrayList) result.getTweets();    

    for (int i=0; i<tweets.size(); i++) {	
      Tweet t = (Tweet)tweets.get(i);	
      String user = t.getFromUser();
      String msg = t.getText();
      Date d = t.getCreatedAt();	
      theSearchTweets[i] = msg.substring(queryStr.length()+1);

      println(theSearchTweets[i]);
    }

  } catch (TwitterException e) {    
    println("Search tweets: " + e);  
  }

}

