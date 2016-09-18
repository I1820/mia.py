#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "printf.h"

RF24 radio(9, 10);
/* Radio pipe addresses for the 6 nodes to communicate. */
const uint64_t pipes[6] = { 0xE7D3F03577,
	0xC2C2C2C2C2,
	0xC2C2C2C2C3,
	0xC2C2C2C2C4,
	0xC2C2C2C2C5,
	0xC2C2C2C2C6
};

void setup()
{
	while (!Serial);
	Serial.begin(9600);
	printf_begin();

	/* nRF startup :) */
	radio.begin();
	radio.setPALevel(RF24_PA_MAX);
	radio.setRetries(10, 5);
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
	radio.openReadingPipe(0, pipes[1]);
	radio.openReadingPipe(0, pipes[2]);
	radio.openReadingPipe(0, pipes[3]);
	radio.openReadingPipe(0, pipes[4]);
	radio.openReadingPipe(1, pipes[5]);
	if (radio.available()) {
		char text[33] = {0};
		radio.read(&text, sizeof(text));
		Serial.println(text);
		switch (text[1]) {
			case '1':
				radio.openWritingPipe(pipes[0]);
				radio.stopListening();
				delayMicroseconds(200);
				for(int i = 0; i < 2; i++){
					radio.write("ack1", sizeof("ack1"));
					delayMicroseconds(200);
				}
				break;
			case '2':
				radio.openWritingPipe(pipes[0]);
				radio.stopListening();
				delayMicroseconds(200);
				for (int i = 0; i < 2; i++) {
					radio.write("ack2", sizeof("ack2"));
					delayMicroseconds(200);
				}
				break;
			case '3':
				radio.openWritingPipe(pipes[0]);
				radio.stopListening();
				delayMicroseconds(200);
				for(int i = 0; i < 2; i++) {
					radio.write("ack3", sizeof("ack3"));
					delayMicroseconds(300);
				}
				break;
			case '4':
				radio.openWritingPipe(pipes[0]);
				radio.stopListening();
				delayMicroseconds(200);
				for (int i = 0; i < 2; i++){
					radio.write("ack4", sizeof("ack4"));
					delayMicroseconds(300);
				}
				break;
		}
	}
	int index = 0;
	char charbuff[50];
	if (Serial.available())
	{
		String input = Serial.readString();
		Serial.println(input);

		for (int i = 0; i < 32; i++) {
			if (input[i] == '.')
				index = i + 1;
		}
		input.toCharArray(charbuff, index + 1);
		radio.openWritingPipe(pipes[5]);
		radio.stopListening();
		radio.write(charbuff, index);
	}
}
