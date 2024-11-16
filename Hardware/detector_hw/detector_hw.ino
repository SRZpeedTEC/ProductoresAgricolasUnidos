// Definición de los pines del sensor TCS3200
const int S0 = 4;
const int S1 = 5;
const int S2 = 6;
const int S3 = 7;
const int sensorOut = 8;

// Pines para los LEDs de color
const int ledPapa = 9;
const int ledTomateRojo = 10;
const int ledTomateVerde = 11;
const int ledTomateAmarillo = 3;

// Pines para el sensor ultrasónico
const int trigPin = 12;
const int echoPin = 11;

// Pines para los LEDs de tamaño de papa
const int ledPapaPequena = 13;
const int ledPapaGrande = A0;

// Variables para el tiempo de encendido de los LEDs
unsigned long ledTimer = 0;
const unsigned long ledDuration = 3000; // Duración en milisegundos (3 segundos)
bool ledActive = false;

// Rango de distancia para tamaño de papa (en centímetros)
const int distanciaPequenaMax = 10; // Ajusta según tus necesidades
const int distanciaGrandeMin = 11; // Ajusta según tus necesidades

void setup() {
  // Configuración de los pines del sensor de color como salidas
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(sensorOut, INPUT);

  // Configuración de los pines de los LEDs de color como salidas
  pinMode(ledPapa, OUTPUT);
  pinMode(ledTomateRojo, OUTPUT);
  pinMode(ledTomateVerde, OUTPUT);
  pinMode(ledTomateAmarillo, OUTPUT);

  // Configuración de los pines del sensor ultrasónico
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Configuración de los pines de los LEDs de tamaño de papa como salidas
  pinMode(ledPapaPequena, OUTPUT);
  pinMode(ledPapaGrande, OUTPUT);

  Serial.begin(9600);

  // Configura el sensor TCS3200 a alta frecuencia de salida
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

// Función para medir la distancia con el sensor ultrasónico
int medirDistancia() {
  // Envía un pulso de 10 microsegundos
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Calcula el tiempo que tarda en regresar el pulso
  long duracion = pulseIn(echoPin, HIGH);

  // Calcula la distancia en centímetros
  int distancia = duracion * 0.034 / 2; // Fórmula: distancia = (duración * velocidad del sonido) / 2
  return distancia;
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
    digitalWrite(ledPapaPequena, LOW);
    digitalWrite(ledPapaGrande, LOW);
    ledActive = false;
  }

  // Condiciones para identificar colores y activar LEDs
  if (!ledActive) { // Solo procesa si no hay un LED encendido actualmente
    if (red < 50 && green > 60 && blue > 65) { // Ajusta estos valores
      Serial.println("Tomate rojo detectado");
      digitalWrite(ledTomateRojo, HIGH);
      ledActive = true;
      ledTimer = millis();
    } 
    else if (red > 50 && green > 60 && blue < 70) { // Ajusta estos valores
      Serial.println("Tomate verde detectado");
      digitalWrite(ledTomateVerde, HIGH);
      ledActive = true;
      ledTimer = millis();
    } 
    else if (red > 40 && green > 40 && blue > 50) { // Ajusta estos valores
      Serial.println("Papa detectada");
      digitalWrite(ledPapa, HIGH);
      ledActive = true;
      ledTimer = millis();

      // Determina el tamaño de la papa
      int distancia = medirDistancia();
      Serial.print("Distancia medida: ");
      Serial.println(distancia);

      if (distancia <= distanciaPequenaMax) {
        Serial.println("Papa pequeña detectada");
        digitalWrite(ledPapaPequena, HIGH);
      } 
      else if (distancia >= distanciaGrandeMin) {
        Serial.println("Papa grande detectada");
        digitalWrite(ledPapaGrande, HIGH);
      }
    } 
    else {
      Serial.println("Objeto desconocido");
    }
  }
}
