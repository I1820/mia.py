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
		char ingress[33] = {0};
		radio.read(&ingress, sizeof(ingress));

		/* Send ingress information to serial */
		Serial.println(ingress);

		/* Send back the acknowledgement */
		radio.openWritingPipe(pipes[0]);
		radio.stopListening();
		delayMicroseconds(200);
		if (ingress[0] == '@') {
			for(int i = 0; i < 2; i++){
				char ack[5] = "ack";
				ack[3] = ingress[1];
				ack[4] = 0;
				radio.write(ack, 4);
				delayMicroseconds(200);
			}
		}
	}

	if (Serial.available())
	{
		String input = Serial.readString();
		int index = 0;
		char charbuff[32];
		do {
			Serial.println("s" + input);
			index = input.indexOf('.');
			if (index != -1 && index < 31) {
				String egress = input.substring(0, index + 1);
				Serial.println("r" + egress);
				egress.toCharArray(charbuff, 32);
				radio.openWritingPipe(pipes[5]);
				radio.stopListening();
				radio.write(charbuff, index + 1);
				input = input.substring(index + 1);
			}
		} while(index != -1 && input.length() > 0);
	}
}
