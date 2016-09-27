#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "printf.h"
#include <elapsedMillis.h>
#define interval 10

elapsedMillis stopwatch;
RF24 radio(9, 10);
int count=0;
boolean flag = false;
const uint64_t pipes[6] = { 0xE7D3F03577,
	0xC2C2C2C2C2,
	0xC2C2C2C2C3,
	0xC2C2C2C2C4,
	0xC2C2C2C2C5,
	0xC2C2C2C2C6
};   // Radio pipe addresses for the 6 nodes to communicate.
byte node_address=1;
void ack(char text[]);
String out_char="";
String c="";
char charbuff[50];
char charbuff1[50];

void setup()
{
	while (!Serial);
	Serial.begin(9600);
	printf_begin();
	radio.begin();
	radio.setPALevel( RF24_PA_MAX ) ;
	radio.setRetries(10,5);
	radio.setChannel(108);
	radio.openReadingPipe(0, pipes[0]);
	radio.openReadingPipe(0, pipes[1]);
	radio.openReadingPipe(0, pipes[2]);
	radio.openReadingPipe(0, pipes[3]);
	radio.openReadingPipe(0, pipes[4]);
	radio.openReadingPipe(1, pipes[5]);
	radio.startListening();
	radio.printDetails();
}
void loop()
{
	radio.startListening();
	radio.openReadingPipe(0, pipes[0]);

	radio.openReadingPipe(1, pipes[5]);
	if (radio.available())
	{
		char text[33] = {0};
		radio.read(&text, 33);
		Serial.println(text);
		switch (text[1]) {
			case '1':
				radio.openWritingPipe(pipes[0]);
				radio.stopListening();
				delayMicroseconds(200);
				for(int i=0;i<2;i++){
					radio.write("ack1",sizeof("ack1"));
					delayMicroseconds(200);
				}
				break;
			case '2':
				radio.openWritingPipe(pipes[0]);
				radio.stopListening();
				delayMicroseconds(200);
				for(int i=0;i<2;i++){
					radio.write("ack2",sizeof("ack2"));
					delayMicroseconds(200);
				}
				break;
			case '3':
				radio.openWritingPipe(pipes[0]);
				radio.stopListening();
				delayMicroseconds(200);
				for(int i=0;i<2;i++){
					radio.write("ack3",sizeof("ack3"));
					delayMicroseconds(300);
				}
				break;
			case '4':
				radio.openWritingPipe(pipes[0]);
				radio.stopListening();
				delayMicroseconds(200);
				for(int i=0;i<2;i++){
					radio.write("ack4",sizeof("ack4"));
					delayMicroseconds(300);
				}
				break;
			case '9':
				radio.openWritingPipe(pipes[0]);
				radio.stopListening();
				delayMicroseconds(200);
				for(int i=0;i<2;i++){
					radio.write("ack9",sizeof("ack9"));
					delayMicroseconds(300);
				}
				break;
		}
	}
	int index1=0;
	if ( Serial.available() )
	{
		c = Serial.readString();
		for(int i=0;i<32;i++){
			if(c[i]=='.')
				index1=i+1;
		}
		c.toCharArray(charbuff1, index1+1);
		radio.openWritingPipe(pipes[5]);
		radio.stopListening();
		radio.write(charbuff1,index1);
		flag=false;
		stopwatch=0; //stopwatch reset
		while(interval>stopwatch && flag==false)
		{
			if (radio.available())
			{
				char text[33] = {0};
				radio.read(&text, 33);
				Serial.println("recived:");
				Serial.println(text);
				int result=strcmp(text, "set1");
				if(result==0)
				{
					flag=true;//out_char="";
					break;
				}
			}
		}
	}
}
