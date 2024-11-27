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
#define LED_MALO 12

// Contadores de detección
int contadorPapa = 0;
int contadorTomateRojo = 0;
int contadorTomateVerde = 0;
int contadorTomateAmarillo = 0;
int contadorMalEstado = 0;

// Variables para seguimiento de lecturas consecutivas
int lecturaActual = 0;  // 1 para papa, 2 para tomate rojo, etc.
int contadorLecturas = 0; // Cuenta las lecturas consecutivas

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
  pinMode(LED_MALO, OUTPUT);

  // Configuración inicial del sensor
  digitalWrite(S0, HIGH); // Escala de frecuencia al 100%
  digitalWrite(S1, LOW);

  Serial.begin(9600); // Comunicación serial para diagnóstico
  Serial.println("Sistema de Identificación de Colores Iniciado");
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

  // Imprimir frecuencias en la consola serial
  Serial.print("Rojo: ");
  Serial.print(rojo);
  Serial.print(" | Verde: ");
  Serial.print(verde);
  Serial.print(" | Azul: ");
  Serial.println(azul);

  // Determinar color basado en umbrales
  int nuevaLectura = 0; // Variable temporal para almacenar la lectura actual

  if (rojo >= 35 && rojo <= 60 && verde >= 58 && verde <= 85 && azul >= 70 && azul < 95) {
    nuevaLectura = 1; // Papa detectada
  } else if (rojo >= 45 && rojo <= 70 && verde >= 120 && verde <= 145 && azul >= 120 && azul < 145) {
    nuevaLectura = 2; // Tomate rojo detectado
  } else if (rojo >= 30 && rojo < 50 && verde >= 45 && verde < 60 && azul >= 60 && azul <= 75) {
    nuevaLectura = 3; // Tomate verde detectado
  } else if (rojo >= 20 && rojo < 35 && verde >= 40 && verde < 55 && azul >= 70 && azul <= 85) {
    nuevaLectura = 4; // Tomate amarillo detectado
  } else {
    nuevaLectura = 5; // Verdura en mal estado
  }

  // Comparar lectura actual con la anterior
  if (nuevaLectura == lecturaActual) {
    contadorLecturas++;
  } else {
    lecturaActual = nuevaLectura;
    contadorLecturas = 1;
  }

  // Si hay 4 lecturas consecutivas iguales, actualizar el contador correspondiente
  if (contadorLecturas >= 4) {
    switch (lecturaActual) {
      case 1:
        contadorPapa++;
        Serial.println("Papa detectada. Total: " + String(contadorPapa));
        encenderLed(LED_PAPA);
        break;
      case 2:
        contadorTomateRojo++;
        Serial.println("Tomate rojo detectado. Total: " + String(contadorTomateRojo));
        encenderLed(LED_ROJO);
        break;
      case 3:
        contadorTomateVerde++;
        Serial.println("Tomate verde detectado. Total: " + String(contadorTomateVerde));
        encenderLed(LED_VERDE);
        break;
      case 4:
        contadorTomateAmarillo++;
        Serial.println("Tomate amarillo detectado. Total: " + String(contadorTomateAmarillo));
        encenderLed(LED_AMARILLO);
        break;
      case 5:
        contadorMalEstado++;
        Serial.println("Verdura en mal estado detectada. Total: " + String(contadorMalEstado));
        encenderLed(LED_MALO);
        break;
    }
    contadorLecturas = 0; // Reiniciar el contador de lecturas consecutivas
  }

  // Imprimir todos los conteos acumulados
  Serial.println("Resumen de detecciones:");
  Serial.println("Papa: " + String(contadorPapa));
  Serial.println("Tomate rojo: " + String(contadorTomateRojo));
  Serial.println("Tomate verde: " + String(contadorTomateVerde));
  Serial.println("Tomate amarillo: " + String(contadorTomateAmarillo));
  Serial.println("Verduras en mal estado o mala lectura: " + String(contadorMalEstado));

  delay(1000); // Retraso de 1 segundo entre lecturas
}

// Función para encender LED por 3 segundos
void encenderLed(int ledPin) {
  digitalWrite(ledPin, HIGH);
  delay(3000);
  digitalWrite(ledPin, LOW);
}
