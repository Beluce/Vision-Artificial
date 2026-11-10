String datoSerial;

char letra;

int pinRED = 3;
int pinGREEN = 5;
int pinBLUE = 6;

void setup() {
  Serial.begin(9600);

  pinMode(pinRED, OUTPUT);
  pinMode(pinGREEN, OUTPUT);
  pinMode(pinBLUE, OUTPUT);

}

void loop() {

  if(Serial.available()){

    datoSerial = Serial.readStringUntil('\n');

    letra = datoSerial.charAt(0);

    if(letra == 'A'){
      analogWrite(pinRED, 0);
      analogWrite(pinGREEN, 0); //AZUL
      analogWrite(pinBLUE, 255);
    }else if(letra == 'E'){
      analogWrite(pinRED, 0);
      analogWrite(pinGREEN, 255); //VERDE
      analogWrite(pinBLUE, 0);
    }else if(letra == 'I'){
      analogWrite(pinRED, 255);
      analogWrite(pinGREEN, 0); //ROJO
      analogWrite(pinBLUE, 0);
    }else if(letra == 'O'){
      analogWrite(pinRED, 255);
      analogWrite(pinGREEN, 100); //AMARILLO
      analogWrite(pinBLUE, 0);
    }else if(letra == 'U'){
      analogWrite(pinRED, 0);
      analogWrite(pinGREEN, 255); //CYAN
      analogWrite(pinBLUE, 255);
    }else{
      analogWrite(pinRED, 0);
      analogWrite(pinGREEN, 0); //APAGADO
      analogWrite(pinBLUE, 0);
    }

  }

}
