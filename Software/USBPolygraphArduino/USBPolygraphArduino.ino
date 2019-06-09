/**********************************************************
  USB POLYGRAPH ARDUINO FIRMWARE VERSION 1
  First released to the public on MAY 2019
  Written by JuanGg on JUNE 2018
  https://juangg-projects.blogspot.com/
This work is licensed under GNU General Public License v3.0
***********************************************************/

/**********************************************************
   Takes readings from A0 (brt), A1 (gsr) and A2 (hrt) 
   four times a second, averages them and sends the formated 
   values (0000, 0000, 0000) through the serial port to a 
   python program that graphs them. A0 and A1 are reversed 
   before sending as their sensors work backwards. 
 **********************************************************/


#define led 13
bool transmit = false;
unsigned long prevMillis = 0;

int A0readings[4]; 
int A1readings[4];
int A2readings[4];
int readingsIndex = 0; 



void setup() 
{
	Serial.begin(115200); 
	pinMode(led,OUTPUT);
	pinMode(A0, INPUT);
	pinMode(A1, INPUT);
	pinMode(A2, INPUT);

}

void loop() 
{
  int data=Serial.read(); 
  switch(data)
  {
    case '0':
      digitalWrite(led,LOW);
      transmit = false;
      break;      
    case '1':
      digitalWrite(led,HIGH); 
      transmit = true;
      break;
  }

  unsigned long currentMillis = millis();
  if(currentMillis - prevMillis >= 25)
  {
    prevMillis = currentMillis;
    if(readingsIndex == 3)
    {
      if(transmit)
      {
        Serial.print("(");
        print_fmt(map((A0readings[0] + A0readings[1] + A0readings[2] + A0readings[3])/4, 0, 1023, 1023, 0));
        Serial.print(", ");
        print_fmt(map((A1readings[0] + A1readings[1] + A1readings[2] + A1readings[3])/4, 0, 1023, 1023, 0));
        Serial.print(", ");
        print_fmt((A2readings[0] + A2readings[1] + A2readings[2] + A2readings[3])/4);
        Serial.println(")");
      }
      readingsIndex = 0;
    }
    else
    {
      readingsIndex ++;
    }
    A0readings[readingsIndex] = analogRead(A0);
    A1readings[readingsIndex] = analogRead(A1);
    A2readings[readingsIndex] = analogRead(A2);
  }
  
  
}

void print_fmt(int num)
{
  if(num == 0)
    Serial.print("0000");
  else if(num<10)
  {
    Serial.print("000");
    Serial.print(num);
  }
  else if(num<100)
  {
    Serial.print("00");
    Serial.print(num);
  }
  else if(num<1000)
  {
    Serial.print("0");
    Serial.print(num);
  }
  else
    Serial.print(num);
}



