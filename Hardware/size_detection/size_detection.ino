// Pines del sensor ultrasónico
#define TRIG 12  // Pin TRIG del sensor ultrasónico
#define ECHO 13  // Pin ECHO del sensor ultrasónico

// Pines para los LEDs
#define LED_PEQUENA 7  // LED para papa pequeña
#define LED_GRANDE 8   // LED para papa grande

// Variables para el contador
int contadorPapaPequena = 0;  // Contador de papas pequeñas
int contadorPapaGrande = 0;   // Contador de papas grandes

// Variables para seguimiento de lecturas consecutivas
int lecturaActual = 0;  // 1 para papa grande, 2 para papa pequeña, 0 para ninguna
int contadorLecturas = 0; // Cuenta las lecturas consecutivas

void setup() {
  // Configuración de pines
  pinMode(TRIG, OUTPUT);  // Pin TRIG como salida
  pinMode(ECHO, INPUT);   // Pin ECHO como entrada
  pinMode(LED_PEQUENA, OUTPUT);  // Pin para LED de papa pequeña
  pinMode(LED_GRANDE, OUTPUT);   // Pin para LED de papa grande

  // Inicia la comunicación serial
  Serial.begin(9600);
  Serial.println("Sistema de Clasificación de Papas Iniciado");

  // Mostrar el encabezado de la interfaz
  Serial.println("Interfaz de Monitoreo:");
  Serial.println("Clasificación de Papas");
  Serial.println("-------------------------");
}

float medirDistancia() {
  // Envía un pulso TRIG
  digitalWrite(TRIG, LOW);
  delayMicroseconds(2);  // Espera 2 microsegundos
  digitalWrite(TRIG, HIGH);
  delayMicroseconds(10);  // Pulso de 10 microsegundos
  digitalWrite(TRIG, LOW);

  // Lee el tiempo del eco
  long duracion = pulseIn(ECHO, HIGH);

  // Calcula la distancia en centímetros
  float distancia = duracion * 0.034 / 2;
  return distancia;
}

void loop() {
  // Medir distancia
  float distancia = medirDistancia();

  // Mostrar la distancia medida
  Serial.print("Distancia detectada: ");
  Serial.print(distancia);
  Serial.println(" cm");

  // Clasificar tamaño y actualizar contadores
  if (distancia > 5 && distancia <= 7) { 
    // Papa grande detectada
    if (lecturaActual == 1) {
      contadorLecturas++;
    } else {
      lecturaActual = 1;
      contadorLecturas = 1;
    }

    digitalWrite(LED_GRANDE, HIGH);   // Enciende LED para papa grande
    digitalWrite(LED_PEQUENA, LOW);  // Asegura que el LED pequeño esté apagado
    Serial.println("Clasificación: Papa grande");

  } else if (distancia > 4 && distancia <= 6) { 
    // Papa pequeña detectada
    if (lecturaActual == 2) {
      contadorLecturas++;
    } else {
      lecturaActual = 2;
      contadorLecturas = 1;
    }

    digitalWrite(LED_PEQUENA, HIGH);  // Enciende LED para papa pequeña
    digitalWrite(LED_GRANDE, LOW);   // Asegura que el LED grande esté apagado
    Serial.println("Clasificación: Papa pequeña");

  } else {
    // Nada detectado
    Serial.println("Clasificación: Nada detectado");
    digitalWrite(LED_PEQUENA, LOW);  // Apaga ambos LEDs
    digitalWrite(LED_GRANDE, LOW);
    contadorLecturas = 0;  // Reinicia el contador de lecturas consecutivas
    lecturaActual = 0;
  }

  // Si hay 4 lecturas consecutivas iguales, aumenta el contador
  if (contadorLecturas >= 4) {
    if (lecturaActual == 1) {  // Papa grande
      contadorPapaGrande++;
      Serial.print("Total Papas Grandes: ");
      Serial.println(contadorPapaGrande);
    } else if (lecturaActual == 2) {  // Papa pequeña
      contadorPapaPequena++;
      Serial.print("Total Papas Pequeñas: ");
      Serial.println(contadorPapaPequena);
    }
    contadorLecturas = 0;  // Reinicia el contador de lecturas
  }

  // Mostrar información en la interfaz serial
  Serial.println("-------------------------");
  Serial.print("Papas Grandes: ");
  Serial.println(contadorPapaGrande);
  Serial.print("Papas Pequeñas: ");
  Serial.println(contadorPapaPequena);
  Serial.println("-------------------------");

  // Pausa para evitar lecturas continuas
  delay(1000);  // 1 segundo de espera antes de la próxima medición
}
