#include <U8glib.h>


U8GLIB_ST7920_128X64_1X u8g(8, 9, 10, 11, 4, 5, 6, 7, 18, 17, 16, 12);
uint8_t x;
uint8_t y;
uint8_t incomingByte;
#define COLS 42
#define ROWS 21
char mapa[COLS*ROWS] = {};

const uint8_t wall[] U8G_PROGMEM = {
  0xE0, // 111
  0xE0, // 111
  0xE0  // 111
};
const uint8_t zombie[] U8G_PROGMEM = {
  0xA0, // 101
  0x40, // 010
  0xA0  // 101
};
const uint8_t box[] U8G_PROGMEM = {
  0xE0, // 111
  0xA0, // 101
  0xE0  // 111
};
const uint8_t player[] U8G_PROGMEM = {
  0x40, // 010
  0xE0, // 111
  0x40  // 010
};
const uint8_t blank[] U8G_PROGMEM = {
  0x00, // 000
  0x00, // 000
  0x00  // 000
};

void draw(void) {
  // graphic commands to redraw the complete screen should be placed here  
  uint8_t i;
  uint8_t j;
   u8g.firstPage();  
   do {
     for(i=0;i<COLS;i++){
       for(j=0;j<ROWS;j++){
         switch(mapa[i+j*COLS]){
           case 'z':
             u8g.drawBitmapP( i*3, j*3, 1, 3, zombie);
             break;
           case 'b':
             u8g.drawBitmapP( i*3, j*3, 1, 3, box);
             break;
           case 'w':
             u8g.drawBitmapP( i*3, j*3, 1, 3, wall);
             break;
           case 'p':
             u8g.drawBitmapP( i*3, j*3, 1, 3, player);
             break;
           default:
             break;
         }
       }
     }
   } while( u8g.nextPage() );
}

void init_map(void){
  uint8_t i;
  uint8_t j;
  for(i=0;i<COLS;i++){
    for(j=0;j<ROWS;j++){
    x = i;
    y = j;
    write_map_position('0');
  }
  }
}

void write_map_position (uint8_t value){
    mapa[x+y*COLS] = (char) value;
}

void setup(void) {
  Serial.begin(9600);
  init_map();
  u8g.setFont(u8g_font_osb18);
}

void loop(void) {

    if (Serial.available() > 0) {
          // lee el byte entrante:
          incomingByte = Serial.read();
          //init_map();
          while(Serial.available() == 0){}
          x = Serial.read();
          while(Serial.available() == 0){}
          y = Serial.read();
          
          switch (incomingByte) {
                 case 'g':
                   u8g.firstPage();
                   do {
                     u8g.drawStr(0, 20, "YOU");
                     u8g.drawStr(22, 42, "WIN!");
                   } while( u8g.nextPage() );
                   break;
                 case 'l':
                   u8g.firstPage();
                   do {
                     u8g.drawStr(0, 20, "YOU");
                     u8g.drawStr(22, 42, "LOSE!");
                   } while( u8g.nextPage() );
                   break;
                 case 'w':
                 case 'z':
                 case 'b':
                 case 'p':
                     write_map_position(incomingByte);
                     break;
                     
                 case 'r':
                     
                     draw();
                     init_map();
                     
                       /*uint32_t i;
                       for(i=0;i<(COLS*ROWS);i++){
                            Serial.write(mapa[i]);
                        }*/
                      break;
                 default:
                     break;
            }  
      }
  delay(10);
}
