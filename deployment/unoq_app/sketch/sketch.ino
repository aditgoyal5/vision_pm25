// #include <Arduino.h>
// #include <Arduino_LED_Matrix.h>

// #define PMS_UART Serial

// Arduino_LED_Matrix matrix;

// uint8_t pms_frame[32];
// int pms_idx = 0;

// int pm25 = -1;
// int pm25_smooth = -1;
// uint32_t valid_frames = 0;
// uint32_t checksum_errors = 0;
// uint32_t total_bytes = 0;

// unsigned long boot_ms = 0;
// unsigned long last_bar_ms = 0;
// unsigned long last_number_ms = 0;
// bool matrix_ready = false;
// bool show_number = false;

// // 8x13 grayscale framebuffer (0..7)
// uint8_t fb[104];

// // 3x5 digit font (row-major 3x5 = 15 bits per digit)
// const uint8_t DIGITS[10][15] = {
//   {1,1,1, 1,0,1, 1,0,1, 1,0,1, 1,1,1}, // 0
//   {0,1,0, 1,1,0, 0,1,0, 0,1,0, 1,1,1}, // 1
//   {1,1,1, 0,0,1, 1,1,1, 1,0,0, 1,1,1}, // 2
//   {1,1,1, 0,0,1, 0,1,1, 0,0,1, 1,1,1}, // 3
//   {1,0,1, 1,0,1, 1,1,1, 0,0,1, 0,0,1}, // 4
//   {1,1,1, 1,0,0, 1,1,1, 0,0,1, 1,1,1}, // 5
//   {1,1,1, 1,0,0, 1,1,1, 1,0,1, 1,1,1}, // 6
//   {1,1,1, 0,0,1, 0,1,0, 0,1,0, 0,1,0}, // 7
//   {1,1,1, 1,0,1, 1,1,1, 1,0,1, 1,1,1}, // 8
//   {1,1,1, 1,0,1, 1,1,1, 0,0,1, 1,1,1}  // 9
// };

// void clearFb() {
//   for (int i = 0; i < 104; i++) fb[i] = 0;
// }

// void setPx(int row, int col, uint8_t v) {
//   if (row < 0 || row >= 8 || col < 0 || col >= 13) return;
//   fb[row * 13 + col] = v;
// }

// void drawDigit3x5(int digit, int top, int left, uint8_t bright) {
//   if (digit < 0 || digit > 9) return;
//   for (int r = 0; r < 5; r++) {
//     for (int c = 0; c < 3; c++) {
//       if (DIGITS[digit][r * 3 + c]) {
//         setPx(top + r, left + c, bright);
//       }
//     }
//   }
// }

// void showNumber3Digits(int value) {
//   if (value < 0) value = 0;
//   if (value > 999) value = 999;

//   int h = value / 100;
//   int t = (value / 10) % 10;
//   int o = value % 10;

//   clearFb();

//   // 3 digits * 3 cols + 2 gaps = 11 cols; center in 13 cols => left=1
//   int left = 1;
//   int top = 1; // 5 rows in 8-high panel

//   drawDigit3x5(h, top, left + 0, 7);
//   drawDigit3x5(t, top, left + 4, 7);
//   drawDigit3x5(o, top, left + 8, 7);

//   matrix.setGrayscaleBits(3);
//   matrix.draw(fb);
// }

// void showBar(int value) {
//   clearFb();

//   int v = value;
//   if (v < 0) v = 0;
//   if (v > 200) v = 200;

//   int cols_on = (v * 13) / 200;
//   if (cols_on < 0) cols_on = 0;
//   if (cols_on > 13) cols_on = 13;

//   for (int r = 0; r < 8; r++) {
//     for (int c = 0; c < cols_on; c++) {
//       setPx(r, c, 7);
//     }
//   }

//   matrix.setGrayscaleBits(3);
//   matrix.draw(fb);
// }

// void sendCmd(const uint8_t *cmd, size_t n) {
//   PMS_UART.write(cmd, n);
//   PMS_UART.flush();
// }

// void forcePmsActive() {
//   const uint8_t wakeCmd[]   = {0x42, 0x4D, 0xE4, 0x00, 0x01, 0x01, 0x74};
//   const uint8_t activeCmd[] = {0x42, 0x4D, 0xE1, 0x00, 0x01, 0x01, 0x71};
//   sendCmd(wakeCmd, sizeof(wakeCmd));
//   delay(100);
//   sendCmd(activeCmd, sizeof(activeCmd));
//   delay(100);
// }

// void parsePmsFrame() {
//   uint16_t sum = 0;
//   for (int i = 0; i < 30; i++) sum += pms_frame[i];
//   uint16_t expected = ((uint16_t)pms_frame[30] << 8) | pms_frame[31];

//   if (sum != expected) {
//     checksum_errors++;
//     return;
//   }

//   pm25 = ((uint16_t)pms_frame[12] << 8) | pms_frame[13];
//   valid_frames++;

//   if (pm25_smooth < 0) pm25_smooth = pm25;
//   else pm25_smooth = (pm25_smooth * 7 + pm25 * 3) / 10;
// }

// void readSensor() {
//   int budget = 24;
//   while (PMS_UART.available() && budget-- > 0) {
//     uint8_t b = (uint8_t)PMS_UART.read();
//     total_bytes++;

//     if (pms_idx == 0 && b != 0x42) continue;
//     if (pms_idx == 1 && b != 0x4D) {
//       pms_idx = 0;
//       continue;
//     }

//     pms_frame[pms_idx++] = b;
//     if (pms_idx == 32) {
//       pms_idx = 0;
//       parsePmsFrame();
//     }
//   }
// }

// void setup() {
//   PMS_UART.begin(9600);
//   delay(500);
//   forcePmsActive();

//   boot_ms = millis();
// }

// void loop() {
//   readSensor();

//   // Respect UNO Q startup warning before matrix access
//   if (!matrix_ready && (millis() - boot_ms >= 30000UL)) {
//     matrix.begin();
//     matrix.clear();
//     matrix_ready = true;
//     last_bar_ms = millis();
//     last_number_ms = millis();
//   }

//   if (!matrix_ready) {
//     delay(2);
//     return;
//   }

//   unsigned long now = millis();

//   // Alternate: bar for ~6s, number for ~2s
//   if (now - last_number_ms >= 8000UL) {
//     last_number_ms = now;
//     show_number = true;
//   }

//   if (show_number) {
//     showNumber3Digits(pm25_smooth < 0 ? 0 : pm25_smooth);
//     // keep number visible for 2s
//     if (now - last_number_ms >= 2000UL) {
//       show_number = false;
//       last_bar_ms = now;
//     }
//   } else if (now - last_bar_ms >= 250UL) {
//     last_bar_ms = now;
//     showBar(pm25_smooth < 0 ? 0 : pm25_smooth);
//   }

//   delay(2);
// }

#include <Arduino.h>
#include <Arduino_LED_Matrix.h>
#include <Arduino_RouterBridge.h>

#define PMS_UART Serial

Arduino_LED_Matrix matrix;

uint8_t pmsFrame[32];
int pmsIndex = 0;

volatile int pm25 = -1;
volatile int pm25Smooth = -1;
volatile uint32_t validFrames = 0;
volatile uint32_t checksumErrors = 0;
volatile uint32_t totalBytes = 0;

unsigned long bootMs = 0;
unsigned long lastDisplayMs = 0;
bool matrixReady = false;

uint8_t fb[104];

const uint8_t DIGITS[10][15] = {
  {1,1,1, 1,0,1, 1,0,1, 1,0,1, 1,1,1}, // 0
  {0,1,0, 1,1,0, 0,1,0, 0,1,0, 1,1,1}, // 1
  {1,1,1, 0,0,1, 1,1,1, 1,0,0, 1,1,1}, // 2
  {1,1,1, 0,0,1, 0,1,1, 0,0,1, 1,1,1}, // 3
  {1,0,1, 1,0,1, 1,1,1, 0,0,1, 0,0,1}, // 4
  {1,1,1, 1,0,0, 1,1,1, 0,0,1, 1,1,1}, // 5
  {1,1,1, 1,0,0, 1,1,1, 1,0,1, 1,1,1}, // 6
  {1,1,1, 0,0,1, 0,1,0, 0,1,0, 0,1,0}, // 7
  {1,1,1, 1,0,1, 1,1,1, 1,0,1, 1,1,1}, // 8
  {1,1,1, 1,0,1, 1,1,1, 0,0,1, 1,1,1}  // 9
};

int ping() { return 1234; }
int get_pm25() { return pm25; }
int get_pm25_smooth() { return pm25Smooth; }
int get_frames() { return (int)validFrames; }
int get_errors() { return (int)checksumErrors; }
int get_bytes() { return (int)totalBytes; }

void clearFb() {
  for (int i = 0; i < 104; i++) {
    fb[i] = 0;
  }
}

void setPx(int row, int col, uint8_t value) {
  if (row < 0 || row >= 8 || col < 0 || col >= 13) {
    return;
  }
  fb[row * 13 + col] = value;
}

void drawDigit3x5(int digit, int top, int left, uint8_t brightness) {
  if (digit < 0 || digit > 9) {
    return;
  }

  for (int r = 0; r < 5; r++) {
    for (int c = 0; c < 3; c++) {
      if (DIGITS[digit][r * 3 + c]) {
        setPx(top + r, left + c, brightness);
      }
    }
  }
}

void showNumber3Digits(int value) {
  if (value < 0) value = 0;
  if (value > 999) value = 999;

  int h = value / 100;
  int t = (value / 10) % 10;
  int o = value % 10;

  clearFb();

  // 3 digits (3 cols each) + 2 gaps = 11 cols, centered in 13 cols
  int left = 1;
  int top = 1; // 5 rows high in 8 rows

  drawDigit3x5(h, top, left + 0, 7);
  drawDigit3x5(t, top, left + 4, 7);
  drawDigit3x5(o, top, left + 8, 7);

  matrix.setGrayscaleBits(3);
  matrix.draw(fb);
}

void sendCmd(const uint8_t *cmd, size_t n) {
  PMS_UART.write(cmd, n);
  PMS_UART.flush();
}

void forcePmsActive() {
  const uint8_t wakeCmd[]   = {0x42, 0x4D, 0xE4, 0x00, 0x01, 0x01, 0x74};
  const uint8_t activeCmd[] = {0x42, 0x4D, 0xE1, 0x00, 0x01, 0x01, 0x71};

  sendCmd(wakeCmd, sizeof(wakeCmd));
  delay(100);
  sendCmd(activeCmd, sizeof(activeCmd));
  delay(100);
  sendCmd(wakeCmd, sizeof(wakeCmd));
  delay(100);
  sendCmd(activeCmd, sizeof(activeCmd));
}

void parsePmsFrame() {
  uint16_t sum = 0;
  for (int i = 0; i < 30; i++) {
    sum += pmsFrame[i];
  }

  uint16_t expected = ((uint16_t)pmsFrame[30] << 8) | pmsFrame[31];

  if (sum != expected) {
    checksumErrors++;
    return;
  }

  pm25 = ((uint16_t)pmsFrame[12] << 8) | pmsFrame[13];
  validFrames++;

  if (pm25Smooth < 0) {
    pm25Smooth = pm25;
  } else {
    pm25Smooth = (pm25Smooth * 7 + pm25 * 3) / 10;
  }
}

void readSensor() {
  int budget = 24;

  while (PMS_UART.available() && budget-- > 0) {
    uint8_t b = (uint8_t)PMS_UART.read();
    totalBytes++;

    if (pmsIndex == 0 && b != 0x42) {
      continue;
    }

    if (pmsIndex == 1 && b != 0x4D) {
      pmsIndex = 0;
      continue;
    }

    pmsFrame[pmsIndex++] = b;

    if (pmsIndex == 32) {
      pmsIndex = 0;
      parsePmsFrame();
    }
  }
}

void setup() {
  PMS_UART.begin(9600);
  delay(500);
  forcePmsActive();

  Bridge.begin();
  Bridge.provide("ping", ping);
  Bridge.provide("get_pm25", get_pm25);
  Bridge.provide("get_pm25_smooth", get_pm25_smooth);
  Bridge.provide("get_frames", get_frames);
  Bridge.provide("get_errors", get_errors);
  Bridge.provide("get_bytes", get_bytes);

  bootMs = millis();
}

void loop() {
  Bridge.update();

  readSensor();

  // Respect UNO Q note: avoid matrix access during Linux startup
  if (!matrixReady && (millis() - bootMs >= 30000UL)) {
    matrix.begin();
    matrix.clear();
    matrixReady = true;
    lastDisplayMs = millis();
  }

  if (matrixReady) {
    unsigned long now = millis();

    // Update number every 300 ms
    if (now - lastDisplayMs >= 300UL) {
      lastDisplayMs = now;
      showNumber3Digits(pm25Smooth < 0 ? 0 : pm25Smooth);
    }
  }

  Bridge.update();
  delay(2);
}