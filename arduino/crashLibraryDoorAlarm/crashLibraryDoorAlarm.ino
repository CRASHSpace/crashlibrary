#define SENSOR_PIN 3
#define OUTPUT_PIN 13

#define DEBOUNCE_MS 500

boolean previousState;
unsigned long eventStartMs;

void setup() {
  digitalWrite(SENSOR_PIN,HIGH);
  pinMode(SENSOR_PIN, INPUT);
  Serial.begin(9600);
  previousState = digitalRead(SENSOR_PIN);
  eventStartMs=0;
}

void loop() {
  boolean currentState = digitalRead(SENSOR_PIN);
  
  if (previousState == currentState) {
    eventStartMs = millis();  
  } else if ((eventStartMs + DEBOUNCE_MS) > millis()) {
    previousState = currentState;
    if (currentState) { 
      //Serial.println("open");
      Serial.println(1);
    } else {
      //Serial.println("close");
      Serial.print(0);
    }
  }
    
  digitalWrite(OUTPUT_PIN,currentState);
 
 
  
}
