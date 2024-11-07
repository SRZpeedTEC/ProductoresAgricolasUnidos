// Definición de los pines del sensor TCS3200
const int S0 = 4;
const int S1 = 5;
const int S2 = 6;
const int S3 = 7;
const int sensorOut = 8;

// Pines para los LEDs
const int ledPapa = 9;
const int ledTomate = 10;
const int ledDesconocido = 11;

// Pin de control de velocidad del motor DC
const int motorPin = 3; // Conectar a la base del transistor TIP120 con una resistencia de 220Ω

// Variables para el tiempo de encendido de los LEDs
unsigned long ledTimer = 0;
const unsigned long ledDuration = 3000; // Duración en milisegundos (3 segundos)
bool ledActive = false;

// Variable para controlar la velocidad del motor (0 a 255)
int velocidadMotor = 250; // Ajusta este valor entre 0 (apagado) y 255 (máxima velocidad)

void setup() {
  // Configuración de los pines del sensor como salidas
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(sensorOut, INPUT);

  // Configuración de los pines de los LEDs como salidas
  pinMode(ledPapa, OUTPUT);
  pinMode(ledTomate, OUTPUT);
  pinMode(ledDesconocido, OUTPUT);

  // Configuración del pin del motor como salida
  pinMode(motorPin, OUTPUT);

  Serial.begin(9600);

  // Configura el sensor a alta frecuencia de salida
  digitalWrite(S0, HIGH);
  digitalWrite(S1, LOW);
}

void controlarMotor(int velocidad) {
  // Ajusta la velocidad del motor en el rango de 0 a 255
  analogWrite(motorPin, velocidad);
}

int getColorFrequency(int s2State, int s3State) {
  digitalWrite(S2, s2State);
  digitalWrite(S3, s3State);
  delay(100); // Espera para estabilizar la lectura
  return pulseIn(sensorOut, LOW); // Lee la frecuencia
}

void loop() {
  // Leer los valores de frecuencia para cada color
  int red = getColorFrequency(LOW, LOW);    // Configuración para rojo
  int green = getColorFrequency(HIGH, HIGH); // Configuración para verde
  int blue = getColorFrequency(LOW, HIGH);   // Configuración para azul
  
  // Imprimir valores en el monitor serial
  Serial.print("Rojo: ");
  Serial.print(red);
  Serial.print(" Verde: ");
  Serial.print(green);
  Serial.print(" Azul: ");
  Serial.println(blue);

  // Si el LED ya está encendido, verifica si ha pasado el tiempo
  if (ledActive && (millis() - ledTimer >= ledDuration)) {
    // Apaga todos los LEDs y resetea el estado
    digitalWrite(ledPapa, LOW);
    digitalWrite(ledTomate, LOW);
    digitalWrite(ledDesconocido, LOW);
    ledActive = false;
  }

  // Condiciones para identificar tomate, papa y tomate verde
  if (!ledActive) { // Solo procesa si no hay un LED encendido actualmente
    if (red < 100 && green > 150 && blue > 100) {
      Serial.println("Tomate rojo detectado");
      digitalWrite(ledTomate, HIGH);
      ledActive = true;
      ledTimer = millis();
    } 
    else if (red < 100 && green < 150 && blue < 150) {
      Serial.println("Papa detectada");
      digitalWrite(ledPapa, HIGH);
      ledActive = true;
      ledTimer = millis();
    } 
    else if (green > 200 && red > 100 && blue < 150) { 
      Serial.println("Tomate verde detectado");
      digitalWrite(ledTomate, HIGH);
      ledActive = true;
      ledTimer = millis();
    } 
    else {
      Serial.println("Objeto desconocido");
      digitalWrite(ledDesconocido, HIGH);
      ledActive = true;
      ledTimer = millis();
    }
  }

  // Control de la velocidad del motor
  controlarMotor(velocidadMotor); // Ajusta la velocidad del motor aquí

  delay(500); // Retardo antes de la siguiente lectura
}
