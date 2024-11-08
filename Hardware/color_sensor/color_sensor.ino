// Definición de los pines del sensor TCS3200
const int S0 = 4;
const int S1 = 5;
const int S2 = 6;
const int S3 = 7;
const int sensorOut = 8;

// Pines para los LEDs
const int ledPapa = 9;
const int ledTomateRojo = 10;
const int ledTomateVerde = 11;
const int ledTomateAmarillo = 12;

// Variables para el tiempo de encendido de los LEDs
unsigned long ledTimer = 0;
const unsigned long ledDuration = 3000; // Duración en milisegundos (3 segundos)
bool ledActive = false;

void setup() {
  // Configuración de los pines del sensor como salidas
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(sensorOut, INPUT);

  // Configuración de los pines de los LEDs como salidas
  pinMode(ledPapa, OUTPUT);
  pinMode(ledTomateRojo, OUTPUT);
  pinMode(ledTomateVerde, OUTPUT);
  pinMode(ledTomateAmarillo, OUTPUT);

  Serial.begin(9600);

  // Configura el sensor a alta frecuencia de salida
  digitalWrite(S0, HIGH);
  digitalWrite(S1, LOW);
}

// Función para obtener la frecuencia del color filtrado
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
    digitalWrite(ledTomateRojo, LOW);
    digitalWrite(ledTomateVerde, LOW);
    digitalWrite(ledTomateAmarillo, LOW);
    ledActive = false;
  }

  // Condiciones para identificar cada tipo de objeto
  if (!ledActive) { // Solo procesa si no hay un LED encendido actualmente
    if (red < 100 && green > 150 && blue > 100) { // Tomate rojo
      Serial.println("Tomate rojo detectado");
      digitalWrite(ledTomateRojo, HIGH);
      ledActive = true;
      ledTimer = millis();
    } 
    else if (red < 100 && green < 150 && blue < 150) { // Papa
      Serial.println("Papa detectada");
      digitalWrite(ledPapa, HIGH);
      ledActive = true;
      ledTimer = millis();
    } 
    else if (green > 200 && red > 100 && blue < 150) { // Tomate verde
      Serial.println("Tomate verde detectado");
      digitalWrite(ledTomateVerde, HIGH);
      ledActive = true;
      ledTimer = millis();
    } 
    else if (red > 150 && green > 150 && blue < 100) { // Tomate amarillo
      Serial.println("Tomate amarillo detectado");
      digitalWrite(ledTomateAmarillo, HIGH);
      ledActive = true;
      ledTimer = millis();
    }
  }

  delay(500); // Retardo antes de la siguiente lectura
}
