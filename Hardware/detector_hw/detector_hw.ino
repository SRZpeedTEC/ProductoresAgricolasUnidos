/*
 * Sistema de Identificación de Colores
 * Arduino encargado de detectar colores usando el sensor TCS3200.
 * Detecta tomate rojo, verde, amarillo y papa, activando LEDs indicativos.
 */

// Pines para el sensor TCS3200
#define S0 4
#define S1 5
#define S2 6
#define S3 7
#define sensorOut 8

// Pines para LEDs indicativos
#define LED_ROJO 10
#define LED_VERDE 11
#define LED_AMARILLO 3
#define LED_PAPA 9

void setup() {
  // Configuración de pines como salidas
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(sensorOut, INPUT);
  
  pinMode(LED_ROJO, OUTPUT);
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_AMARILLO, OUTPUT);
  pinMode(LED_PAPA, OUTPUT);

  // Configuración inicial del sensor
  digitalWrite(S0, HIGH); // Escala de frecuencia al 100%
  digitalWrite(S1, LOW);

  Serial.begin(9600); // Comunicación serial para diagnóstico
}

// Función para medir frecuencia de color
int getColorFrequency(bool s2State, bool s3State) {
  digitalWrite(S2, s2State); // Configuración del filtro de color
  digitalWrite(S3, s3State);
  delay(50); // Tiempo de estabilización del sensor
  return pulseIn(sensorOut, LOW); // Medir frecuencia del sensor
}

// Variables para frecuencias de cada color
int rojo, verde, azul;

void loop() {
  // Obtener frecuencias de cada color
  rojo = getColorFrequency(LOW, LOW);   // Frecuencia para rojo
  verde = getColorFrequency(HIGH, HIGH); // Frecuencia para verde
  azul = getColorFrequency(LOW, HIGH);  // Frecuencia para azul

  // Determinar color basado en umbrales
  if (rojo >= 70 && rojo <= 90 && verde >= 60 && verde <= 95 && azul >= 90 && azul <= 110) {
    // Papa
    Serial.println("Papa detectada (Código: 103)");
    encenderLed(LED_PAPA);
  } else if (rojo >= 90 && verde <= 80 && azul <= 85) {
    // Tomate rojo
    Serial.println("Tomate rojo detectado (Código: 104)");
    encenderLed(LED_ROJO);
  } else if (rojo >= 70 && rojo <= 80 && verde >= 90 && verde <= 110 && azul >= 100) {
    // Tomate verde
    Serial.println("Tomate verde detectado (Código: 101)");
    encenderLed(LED_VERDE);
  } else if (rojo >= 75 && verde >= 95 && azul >= 90 && azul <= 105) {
    // Tomate amarillo
    Serial.println("Tomate amarillo detectado (Código: 102)");
    encenderLed(LED_AMARILLO);
  } else {
    Serial.println("No se pudo identificar el objeto");
  }
}

// Función para encender LED por 3 segundos
void encenderLed(int ledPin) {
  digitalWrite(ledPin, HIGH);
  delay(3000);
  digitalWrite(ledPin, LOW);
}
