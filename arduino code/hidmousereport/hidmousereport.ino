#include <Mouse.h>
#include <hiduniversal.h>
#include "hidmouserptparser.h"

USB Usb;
HIDUniversal Hid(&Usb);
HIDMouseReportParser Mou(nullptr);

// py part
String serial;
int maxMov = 127;

void setup() {
	Mouse.begin();
	Serial.begin(115200);

#if !defined(__MIPSEL__)
    while (!Serial); // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
#endif
    Serial.println("Start");

	if (Usb.Init() == -1)
		Serial.println("OSC did not start.");
	
	delay(200);

	if (!Hid.SetReportParser(0, &Mou))
		ErrorMessage<uint8_t > (PSTR("SetReportParser"), 1);
}

void loop() {
  Usb.Task();

  if(Serial.available() > 0)
  {
    serial = Serial.readStringUntil('!'); 
    if (serial.startsWith("coords:"))
    {
      serial.replace("coords:", "");
      int idxComma = serial.indexOf(",");
      int idxEx = serial.indexOf("!");

      int x = serial.substring(0, idxComma).toInt();
      int y = serial.substring(idxComma + 1, -1).toInt();

      // Serial.println("moving : " + String(x) + ", " + String(y));

      int totalX = 0;
      int totalY = 0;

      int maxX = abs(x / maxMov);
      int maxY = abs(y / maxMov);

      int iter = (maxX >= maxY) ? maxX : maxY;
      for (int i = 0; i < iter; i++) {
        int moveX = (i < maxX) ? ((x >= 0) ? maxMov : maxMov * -1) : 0;
        int moveY = (i < maxY) ? ((y >= 0) ? maxMov : maxMov * -1) : 0;

        totalX += moveX;
        totalY += moveY;
        Mouse.move(moveX, moveY);
      }
      Mouse.move(x % maxMov, y % maxMov);
    }
  }
}

void onButtonDown(uint16_t buttonId) {
	Mouse.press(buttonId);
	Serial.print("Button ");
	switch (buttonId) {
		case MOUSE_LEFT:
			Serial.print("MOUSE_LEFT");
			break;

		case MOUSE_RIGHT:
			Serial.print("MOUSE_RIGHT");
			break;
		
		case MOUSE_MIDDLE:
			Serial.print("MOUSE_MIDDLE");
			break;

		case MOUSE_BUTTON4:
			Serial.print("MOUSE_BUTTON4");
			break;

		case MOUSE_BUTTON5:
			Serial.print("MOUSE_BUTTON5");
			break;
		default:
			Serial.print("OTHER_BUTTON");
			break;
	}
	Serial.println(" pressed");
}

void onButtonUp(uint16_t buttonId) {
	Mouse.release(buttonId);
	Serial.print("Button ");
	switch (buttonId) {
		case MOUSE_LEFT:
			Serial.print("MOUSE_LEFT");
			break;

		case MOUSE_RIGHT:
			Serial.print("MOUSE_RIGHT");
			break;
		
		case MOUSE_MIDDLE:
			Serial.print("MOUSE_MIDDLE");
			break;

		case MOUSE_BUTTON4:
			Serial.print("MOUSE_BUTTON4");
			break;

		case MOUSE_BUTTON5:
			Serial.print("MOUSE_BUTTON5");
			break;
    case MOUSE_BUTTON6:
			Serial.print("MOUSE_BUTTON6");
			break;
    case MOUSE_BUTTON7:
			Serial.print("MOUSE_BUTTON7");
			break;
    case MOUSE_BUTTON8:
			Serial.print("MOUSE_BUTTON8");
			break;
		default:
			Serial.print("OTHER_BUTTON");
			break;
	}
	Serial.println(" released");
}

void onTiltPress(int8_t tiltValue) {
	Serial.print("Tilt pressed: ");
	Serial.println(tiltValue);
}

void onMouseMove(int8_t xMovement, int8_t yMovement, int8_t scrollValue) {
	Mouse.move(xMovement, yMovement, scrollValue);
	Serial.print("Mouse moved:\t");
	Serial.print(xMovement);
	Serial.print("\t");
	Serial.print(yMovement);
	Serial.print("\t");
	Serial.println(scrollValue);
}