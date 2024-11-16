// Definición de pines del sensor TCS3200 (Sensor de Color)
const int S0 = 4; // Pin digital para el control de frecuencia del sensor (S0)
const int S1 = 5; // Pin digital para el control de frecuencia del sensor (S1)
const int S2 = 6; // Pin digital para seleccionar el filtro de color (S2)
const int S3 = 7; // Pin digital para seleccionar el filtro de color (S3)
const int sensorOut = 8; // Pin digital para la salida de frecuencia del sensor

// Pines para los LEDs de detección de color
const int ledPapa = 9;          // LED para papa detectada
const int ledTomateRojo = 10;   // LED para tomate rojo detectado
const int ledTomateVerde = 11;  // LED para tomate verde detectado
const int ledTomateAmarillo = 3;// LED para tomate amarillo detectado

// Pines para los LEDs de tamaño de la papa
const int ledPapaPequena = 13;  // LED para papa pequeña
const int ledPapaGrande = A0;   // LED para papa grande

// Pines para el sensor ultrasónico HC-SR04
const int trigPin = 12; // Pin digital para la señal de disparo (Trig)
const int echoPin = A1; // Pin digital para la señal de eco (Echo)

// Variables para la detección de tamaño con el ultrasónico
int distanciaPequenaMax = 10;   // Rango máximo para papa pequeña en cm
int distanciaGrandeMin = 11;   // Rango mínimo para papa grande en cm

// Variables para controlar el tiempo de encendido de los LEDs
unsigned long ledTimer = 0;             // Variable para almacenar el tiempo de inicio del LED
const unsigned long ledDuration = 3000;// Duración del encendido del LED (3 segundos)
bool ledActive = false;                 // Estado del LED (activo o no)

void setup() {
  // Configuración de los pines del sensor de color como salidas
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(sensorOut, INPUT); // Pin del sensor de color como entrada

  // Configuración de los pines de los LEDs como salidas
  pinMode(ledPapa, OUTPUT);
  pinMode(ledTomateRojo, OUTPUT);
  pinMode(ledTomateVerde, OUTPUT);
  pinMode(ledTomateAmarillo, OUTPUT);
  pinMode(ledPapaPequena, OUTPUT);
  pinMode(ledPapaGrande, OUTPUT);

  // Configuración de los pines del sensor ultrasónico
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Configuración inicial del sensor de color para alta frecuencia
  digitalWrite(S0, HIGH); // Configura S0 en HIGH para alta frecuencia
  digitalWrite(S1, LOW);  // Configura S1 en LOW para alta frecuencia

  Serial.begin(9600); // Inicia la comunicación serial para monitoreo
}

// Función para obtener la frecuencia del color filtrado por el sensor TCS3200
int getColorFrequency(int s2State, int s3State) {
  digitalWrite(S2, s2State); // Configura el filtro de color con S2
  digitalWrite(S3, s3State); // Configura el filtro de color con S3
  delay(50);                 // Pequeño retardo para estabilizar la lectura
  return pulseIn(sensorOut, LOW); // Lee la frecuencia del sensor
}

// Función para medir la distancia con el sensor ultrasónico
int medirDistancia() {
  digitalWrite(trigPin, LOW);  // Asegura que el pin de disparo (Trig) comience en LOW
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH); // Envia un pulso de 10 microsegundos al Trig
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Lee el tiempo de duración del pulso de eco (Echo)
  long duracion = pulseIn(echoPin, HIGH);
  
  // Calcula la distancia en cm (velocidad del sonido: 343 m/s)
  int distancia = duracion * 0.034 / 2;
  return distancia;
}

void loop() {
  // Leer los valores de frecuencia para cada color
  int red = getColorFrequency(LOW, LOW);    // Configuración del sensor para rojo
  int green = getColorFrequency(HIGH, HIGH); // Configuración del sensor para verde
  int blue = getColorFrequency(LOW, HIGH);   // Configuración del sensor para azul
  
  // Imprime los valores de color en el monitor serial para diagnóstico
  Serial.print("Rojo: ");
  Serial.print(red);
  Serial.print(" Verde: ");
  Serial.print(green);
  Serial.print(" Azul: ");
  Serial.println(blue);

  // Si el LED está encendido, verifica si ha pasado el tiempo de encendido
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

  // Condiciones para identificar tomates y papas
  if (!ledActive) { // Solo procesa si no hay un LED encendido actualmente
    if (red > 70 && green > 90 && blue > 100) {
      Serial.println("Tomate verde detectado");
      digitalWrite(ledTomateVerde, HIGH);
      ledActive = true;
      ledTimer = millis();
    } else if (red > 50 && green < 90 && blue > 70) {
      Serial.println("Tomate amarillo detectado");
      digitalWrite(ledTomateAmarillo, HIGH);
      ledActive = true;
      ledTimer = millis();
    } else if (red < 50 && green < 70 && blue < 70) {
      Serial.println("Papa detectada");
      digitalWrite(ledPapa, HIGH);
      ledActive = true;
      ledTimer = millis();

      // Medir tamaño de la papa con el sensor ultrasónico
      int distancia = medirDistancia();
      Serial.print("Distancia medida: ");
      Serial.println(distancia);

      if (distancia <= distanciaPequenaMax) {
        Serial.println("Papa pequeña detectada");
        digitalWrite(ledPapaPequena, HIGH);
      } else if (distancia >= distanciaGrandeMin) {
        Serial.println("Papa grande detectada");
        digitalWrite(ledPapaGrande, HIGH);
      }
    } else if (red > 90 && green < 80 && blue < 70) {
      Serial.println("Tomate rojo detectado");
      digitalWrite(ledTomateRojo, HIGH);
      ledActive = true;
      ledTimer = millis();
    }
  }
}
