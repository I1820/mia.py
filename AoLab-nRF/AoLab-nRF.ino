#include <SPI.h>
#include <nRF24L01.h>
#include <RF24.h>
#include "printf.h"
#include <elapsedMillis.h>
#define interval 10

elapsedMillis stopwatch;
RF24 radio(9, 10);

/* Radio pipe addresses for the 6 nodes to communicate. */
const uint64_t pipes[6] = {
	0xE7D3F03577,
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
	radio.begin();
	radio.setPALevel(RF24_PA_MAX);
	radio.setDataRate(RF24_250KBPS);
	radio.setRetries(10,5);
	radio.setChannel(0);
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

	if (radio.available()) {
		char ingress[33] = {0};

		radio.read(&ingress, 33);

		/* Send ingress information to serial */
		Serial.println(ingress);

		/* Send back the acknowledgement */
		radio.openWritingPipe(pipes[0]);
		radio.stopListening();
		delayMicroseconds(200);
		if (ingress[0] == '@') {
			for(int i = 0; i < 2; i++) {
				char ack[5] = "ack";
				ack[3] = ingress[1];
				ack[4] = 0;
				radio.write(ack, 4);
				delayMicroseconds(200);
			}
		}

	}

	if (Serial.available()) {
		String egress = Serial.readString();
		
		int index = 0;
		char charbuff[50];
		
		for(int i = 0; i < 32; i++) {
			if(egress[i] == '.')
				index = i + 1;
		}
		egress.toCharArray(charbuff, index + 1);
		radio.openWritingPipe(pipes[5]);
		radio.stopListening();
		radio.write(charbuff,index);
		delay(3);
		radio.startListening();
		radio.openReadingPipe(0, pipes[5]);

		/* waiting for the ack from actuator */

		int flag = false;
		/* stopwatch reseting */
		stopwatch = 0;
		char ack[5] = "set";
		ack[3] = charbuff[1];
		ack[4] = 0;
		while (interval > stopwatch && flag == false) {
			if (radio.available()) {
				char ingress[33] = {0};
				radio.read(&ingress, 33);
				Serial.println("r" + String(ingress));
				if (!strcmp(ingress, ack)) {
					flag = true;
					break;
				}
			}
		}
	}
}
