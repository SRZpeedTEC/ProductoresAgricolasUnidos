// Definición de los pines del sensor TCS3200
const int S0 = 4;
const int S1 = 5;
const int S2 = 6;
const int S3 = 7;
const int sensorOut = 8;

void setup() {
  // Configuración de los pines como salidas
  pinMode(S0, OUTPUT);
  pinMode(S1, OUTPUT);
  pinMode(S2, OUTPUT);
  pinMode(S3, OUTPUT);
  pinMode(sensorOut, INPUT);
  
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

  // Condiciones para identificar tomate y papa (ajusta estos valores tras la calibración)
  if (red > 200 && green < 30 && blue < 30) {
    Serial.println("Tomate detectado");
 // } else if (red < 150 && green < 150 && blue < 150) {
 //   Serial.println("Papa detectada");
  } else {
    Serial.println("Objeto desconocido");
  }

  delay(500); // Retardo antes de la siguiente lectura
}
