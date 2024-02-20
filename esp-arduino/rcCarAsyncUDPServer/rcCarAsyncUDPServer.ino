#include "WiFi.h"
#include "AsyncUDP.h"

const char* porta = "1234";
const char* ssid = "Sua rede wifi";
const char* password = "Sua senha";

uint8_t* comando;

unsigned long tempo;
unsigned long timer;

bool setaAtiv = false;

int pinSeta;
int volante = 90; //por padrão volante inicia em 90 graus
int acelerador = 0;
int freio = 0;

int motor1 = 1; // por padrão motor 1 ativo
int motor2 = 0; // por padrão motor 2 desativo


AsyncUDP udp;

#include <ArduinoJson.h>

#include <ESP32Servo.h>
Servo myservo1;  // create servo object to control a servo
#define vServo 13  //GP2 ESP-01

//declaracao dos pinos utilizados para controlar a velocidade de rotacao
#define PINO_ENA 27
#define PINO_ENB 14

//declaracao dos pinos utilizados para controlar o sentido do motor
#define PINO_IN1 25
#define PINO_IN2 26
#define PINO_IN3 32
#define PINO_IN4 33

//declaracao dos pinos utilizados para controlar luzes
#define pinLedFarol 15
#define pinLedFarolAux 2
#define pinLedLanterna 18
#define pinLedSetaSD 4
#define pinLedSetaSE 5


void setup() {
  Serial.begin(115200);

  //motor DC Car
  //configuração dos pinos como saida
  pinMode(PINO_ENA, OUTPUT);
  pinMode(PINO_ENB, OUTPUT);
  pinMode(PINO_IN1, OUTPUT);
  pinMode(PINO_IN2, OUTPUT);
  pinMode(PINO_IN3, OUTPUT);
  pinMode(PINO_IN4, OUTPUT);

  //inicia o codigo com os motores parados
  digitalWrite(PINO_IN1, LOW);
  digitalWrite(PINO_IN2, LOW);
  digitalWrite(PINO_IN3, LOW);
  digitalWrite(PINO_IN4, LOW);
  digitalWrite(PINO_ENA, LOW);
  digitalWrite(PINO_ENB, LOW);

 //configuração dos pinos como saida
  pinMode(pinLedFarol, OUTPUT);
  pinMode(pinLedFarolAux, OUTPUT);
  pinMode(pinLedLanterna, OUTPUT);
  pinMode(pinLedSetaSD, OUTPUT);
  pinMode(pinLedSetaSE, OUTPUT);

//inicia o codigo com as luzes apagadas
  digitalWrite(pinLedFarol, LOW);
  digitalWrite(pinLedFarolAux, LOW);
  digitalWrite(pinLedLanterna, LOW);
  digitalWrite(pinLedSetaSD, LOW);
  digitalWrite(pinLedSetaSE, LOW);

  myservo1.setPeriodHertz(50);         // Standard 50hz servo
  myservo1.attach(vServo, 500, 2400);  // attaches the servo on pin 18 to the servo object
  myservo1.write(volante);

  conectaWiFi();
}



void conectaWiFi() {

  if (WiFi.status() == WL_CONNECTED) {
    return;
  }

  Serial.print("Conectando-se na rede: ");
  Serial.print(ssid);
  Serial.println("  Aguarde!");

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);  // Conecta na rede WI-FI
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("Conectado com sucesso, na rede: ");
  Serial.print(ssid);
  Serial.print("  IP obtido: ");
  Serial.println(WiFi.localIP());
}



long piscaSeta(int pin, long timer) {
  unsigned long temp = 200;
  long tempo = millis();
  
  // Serial.print("tempo: ");
  // Serial.println(tempo);
  // Serial.print("timer: ");
  // Serial.println(timer);
  // Serial.print("timer + temp: ");
  // long x = (timer + temp);
  // Serial.println(x);

  if (setaAtiv) {
    if (tempo >= (timer + temp)) {
      if (digitalRead(pin)) {
        digitalWrite(pin, LOW);
      } else {
        digitalWrite(pin, HIGH);
      }
      return (tempo + temp) ;
    }
  }
  return timer;
}



void mantemConexoes() {
  conectaWiFi();  //se não há conexão com o WiFI, a conexão é refeita
}


void listen() {

  if (udp.listen(1234)) {
    udp.onPacket([](AsyncUDPPacket packet) {
      // Serial.write(packet.data(), packet.length());
      // Serial.println();

      // Tratamento com Json
      DynamicJsonDocument doc(500);
      // Deserialize the JSON document
      DeserializationError error = deserializeJson(doc, packet.data());
      // Test if parsing succeeds.
      if (error) {
        Serial.print(F("deserializeJson() failed: "));
        Serial.println(error.f_str());
        return;
      }

      if (doc.containsKey("V")) {
        int volante = doc["V"];
        volante = map(volante, 0, 100, 160, 20);
        myservo1.write(volante);
        Serial.print("Volante: ");
        Serial.println(volante);
      }

      if (doc.containsKey("A") && doc.containsKey("RE")) {
        int acelerador = doc["A"];
        int direcao1 = doc["RE"];
        acelerador = map(acelerador, 0, 100, 0, 100);
        motorCar(direcao1, acelerador);

        Serial.print("direcao: ");
        Serial.println(direcao1);

        Serial.print("acelerador: ");
        Serial.println(acelerador);
      }

      if (doc.containsKey("4X4")) {
        int tracao = doc["4X4"];

        if (tracao == 1) {
          motorCarTracao(1, 1);
        }

        if (tracao == 0) {
          motorCarTracao(1, 0);
        }

        Serial.print("Tracao: ");
        Serial.println(tracao);
      }

      if (doc.containsKey("FAROL")) {
        int velue = doc["FAROL"];
        if (velue == 1) { digitalWrite(pinLedFarol, HIGH); 
        digitalWrite(pinLedLanterna, HIGH);}
        if (velue == 0) { digitalWrite(pinLedFarol, LOW); }
        if (velue == 1) { digitalWrite(pinLedLanterna, HIGH); }
        if (velue == 0) { digitalWrite(pinLedLanterna, LOW); }
        Serial.print("FAROL: ");
        Serial.println(velue);
      }

      if (doc.containsKey("AUX")) {
        int velue = doc["AUX"];
        if (velue == 1) { digitalWrite(pinLedFarolAux, HIGH); }
        if (velue == 0) { digitalWrite(pinLedFarolAux, LOW); }
        Serial.print("AUX: ");
        Serial.println(velue);
      }

      if (doc.containsKey("SETADIR")) {
        int velue = doc["SETADIR"];
        if (velue == 1) {
          setaAtiv = true;
          pinSeta = pinLedSetaSD;
          digitalWrite(pinLedSetaSE, LOW);
        }
        if (velue == 0) {
          digitalWrite(pinLedSetaSD, LOW);
          setaAtiv = false;
        }
        Serial.print("SETADIR: ");
        Serial.println(velue);
      }

      if (doc.containsKey("SETAESQ")) {
        int velue = doc["SETAESQ"];
        if (velue == 1) {
          setaAtiv = true;
          pinSeta = pinLedSetaSE;
          digitalWrite(pinLedSetaSD, LOW);
        }
        if (velue == 0) {
          digitalWrite(pinLedSetaSE, LOW);
          setaAtiv = false;
        }
        Serial.print("SETAESQ: ");
        Serial.println(velue);
      }

      delay(10);
    });
  }
}


void loop() {
  mantemConexoes();

  while (true) {
  
    timer = piscaSeta(pinSeta, timer);
    listen();
    // testeMotor()
  }
  Serial.println("Fim codigo!");
}



void motorCarTracao(int mot1, int mot2) {
  motor1 = mot1;
  motor2 = mot2;
}



void motorCar(int direcao, int velocidade) {
  //PD CONSTRUIR CLASSE MOTOR
  velocidade = map(velocidade, 0, 100, 0, 256);

  Serial.print("Direção: ");
  Serial.println(direcao);
  Serial.print("velocidade: ");
  Serial.println(velocidade);

  if (motor1 == 1) {

    if (direcao == 1) {
      digitalWrite(PINO_IN1, LOW);
      digitalWrite(PINO_IN2, HIGH);
      analogWrite(PINO_ENA, velocidade);

    } else {
      digitalWrite(PINO_IN1, HIGH);
      digitalWrite(PINO_IN2, LOW);
      analogWrite(PINO_ENA, velocidade);
    }
  } else {
    analogWrite(PINO_ENA, 0);
  }

  if (motor2 == 1) {

    if (direcao == 1) {
      digitalWrite(PINO_IN3, LOW);
      digitalWrite(PINO_IN4, HIGH);
      analogWrite(PINO_ENB, velocidade);
    } else {
      digitalWrite(PINO_IN3, HIGH);
      digitalWrite(PINO_IN4, LOW);
      analogWrite(PINO_ENB, velocidade);
    }
  } else {
    analogWrite(PINO_ENB, 0);
  }
}


void testeMotor() {
  motorCar(1, 50);
  delay(1000);
  motorCar(1, 60);
  delay(1000);
  motorCar(2, 50);
  delay(1000);
  motorCar(2, 60);
  delay(1000);
  motorCar(1, 0);

  motorCar(1, 50);
  delay(1000);
  motorCar(1, 60);
  delay(1000);
  motorCar(2, 50);
  delay(1000);
  motorCar(2, 60);
  delay(1000);
  motorCar(1, 0);
}