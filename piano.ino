const int teclas[] = {
  2, 3, 4, 5, 6, 7,
  8, 9, 10, 11, 12, 13
};

const int comun = A0;
const int cantidad = 12;

bool estadoEstable[cantidad];
bool ultimaLectura[cantidad];
unsigned long ultimoCambio[cantidad];

const unsigned long debounce = 25;

void setup() {
  Serial.begin(115200);

  pinMode(comun, OUTPUT);
  digitalWrite(comun, LOW);

  for (int i = 0; i < cantidad; i++) {
    pinMode(teclas[i], INPUT_PULLUP);

    estadoEstable[i] = HIGH;
    ultimaLectura[i] = HIGH;
    ultimoCambio[i] = 0;
  }
}

void loop() {
  unsigned long ahora = millis();

  for (int i = 0; i < cantidad; i++) {
    bool lectura = digitalRead(teclas[i]);

    if (lectura != ultimaLectura[i]) {
      ultimaLectura[i] = lectura;
      ultimoCambio[i] = ahora;
    }

    if ((ahora - ultimoCambio[i]) >= debounce) {
      if (lectura != estadoEstable[i]) {
        estadoEstable[i] = lectura;

        if (lectura == LOW) {
          Serial.print("ON,");
          Serial.println(i);
        } else {
          Serial.print("OFF,");
          Serial.println(i);
        }
      }
    }
  }
}