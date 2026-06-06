// ======================================
// TCS230/TCS3200 Corrosion Detection
// ======================================

const int pinOut = 18;
const int pinS2  = 19;
const int pinS3  = 21;
const int pinS0  = 23;

const int pinBoton = 26;
const int pinGndBoton = 25;

// Umbral obtenido durante calibración
const int UMBRAL = 2525;

bool estadoAnterior = HIGH;
unsigned long ultimoEvento = 0;

// ======================================

void setup() {

  Serial.begin(115200);

  pinMode(pinOut, INPUT);

  pinMode(pinS2, OUTPUT);
  pinMode(pinS3, OUTPUT);

  pinMode(pinS0, OUTPUT);
  digitalWrite(pinS0, HIGH);

  pinMode(pinGndBoton, OUTPUT);
  digitalWrite(pinGndBoton, LOW);

  pinMode(pinBoton, INPUT_PULLUP);
}

// ======================================

unsigned long leerFrecuencia(bool s2, bool s3) {

  digitalWrite(pinS2, s2);
  digitalWrite(pinS3, s3);

  delay(20);

  unsigned long suma = 0;

  for (int i = 0; i < 10; i++) {

    unsigned long duracion =
      pulseIn(pinOut, HIGH, 200000);

    if (duracion == 0)
      duracion = 200000;

    unsigned long frecuencia =
      1000000UL / duracion;

    suma += frecuencia;

    delay(5);
  }

  return suma / 10;
}

// ======================================

long calcularBrillo() {

  unsigned long rojo =
    leerFrecuencia(LOW, LOW);

  unsigned long azul =
    leerFrecuencia(LOW, HIGH);

  unsigned long verde =
    leerFrecuencia(HIGH, HIGH);

  return (rojo + verde + azul) / 3;
}

// ======================================

void clasificarPieza() {

  long brillo = calcularBrillo();

  if (brillo < UMBRAL) {

    Serial.println("CORROIDA");

  } else {

    Serial.println("NO_CORROIDA");

  }
}

// ======================================

void loop() {

  bool estadoActual =
    digitalRead(pinBoton);

  if (estadoAnterior == HIGH &&
      estadoActual == LOW &&
      millis() - ultimoEvento > 250) {

    clasificarPieza();

    ultimoEvento = millis();
  }

  estadoAnterior = estadoActual;
}