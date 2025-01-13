
int CURRENT_SENSOR_PIN = A0;


void setup()
{
    Serial.begin(9600);
}

void loop()
{

    unsigned int x = 0;
    float AcsValue = 0.0, Samples = 0.0, AvgAcs = 0.0, AcsValueF = 0.0;

    for (int x = 0; x < 150; x++)
    {                                              // Get 150 samples
        AcsValue = analogRead(CURRENT_SENSOR_PIN); // Read current sensor values
        Samples = Samples + AcsValue;              // Add samples together
        delay(3);                                  // let ADC settle before next sample 3ms
    }
    AvgAcs = Samples / 150.0; // Taking Average of Samples
    Serial.print(AvgAcs);
    delay(100);
}

