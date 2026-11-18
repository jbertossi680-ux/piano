# MINI MIDI - Teclado Electrónico con Arduino y Python

## 1. Integrantes

- Parraga Santino
- Ozan Franco
- Bertossi Juan

## 2. Descripción del proyecto

Mini MIDI es un teclado electrónico de 12 pulsadores conectado a Arduino y controlado mediante una aplicación desarrollada en Python.

Cada botón permite reproducir una nota musical o un acorde desde la computadora.

El programa cuenta con dos modos:

- **Notas:** cada botón reproduce una nota individual.
- **Acordes:** cada botón reproduce un acorde configurable.

También permite modificar la tonalidad, octava, transposición y velocidad de las notas. Además, se puede asignar una raíz y un tipo de acorde diferente a cada botón.

El proyecto funciona como un instrumento musical, por lo que no tiene condiciones de victoria o derrota.

## 3. Componentes utilizados

### Hardware

| Componente | Función |
|---|---|
| Arduino | Detecta las pulsaciones y se comunica con Python. |
| 12 pulsadores | Activan las notas y acordes. |
| Cables | Realizan las conexiones. |
| Protoboard | Facilita el armado del circuito. |
| Cable USB | Conecta Arduino con la computadora. |

### Conexiones

Los pulsadores están conectados a las entradas digitales del Arduino:

| Pulsador | Pin |
|   ---   | --- |
|    1    |  2  |
|    2    |  3  |
|    3    |  4  |
|    4    |  5  |
|    5    |  6  |
|    6    |  7  |
|    7    |  8  |
|    8    |  9  |
|    9    |  10  |
|   10    |  11  |
|   11    |  12  |
|   12    |  13  |
| Común |  A0  |

Se utiliza `INPUT_PULLUP` para las entradas y un sistema antirrebote de 25 milisegundos.

### Software y librerías

- Arduino IDE.
- Python 3.
- Tkinter.
- PySerial.
- Mido.
- python-rtmidi.
- loopMIDI.

## 4. Comunicación entre Arduino y Python

La comunicación se realiza mediante USB y el puerto serial, a una velocidad de **115200 baudios**.

Arduino envía mensajes indicando cuándo se presiona o se suelta un botón.

Ejemplos:

- `ON,0`: se presionó el primer botón.
- `OFF,0`: se soltó el primer botón.
- `ON,1`: se presionó el segundo botón.

Los índices van del 0 al 11.

Python recibe estos mensajes y genera las señales MIDI correspondientes:

- `note_on`: activa una nota.
- `note_off`: detiene una nota.

La comunicación es unidireccional: Python no envía información al Arduino.

## 5. Instalación y ejecución

### Paso 1: Instalar Python

Descargar Python 3 desde:

https://www.python.org/downloads/

### Paso 2: Instalar las librerías

Ejecutar en CMD:

```bash
pip install pyserial mido python-rtmidi
```

### Paso 3: Instalar loopMIDI

Descargar desde:

https://www.tobias-erichsen.de/software/loopmidi.html

Crear un puerto MIDI virtual con el nombre `Arduino MIDI`.

### Paso 4: Cargar el código en Arduino

1. Abrir Arduino IDE.
2. Conectar el Arduino mediante USB.
3. Abrir el código del Arduino.
4. Seleccionar la placa y el puerto COM.
5. Cargar el programa.

### Paso 5: Ejecutar Python

1. Conectar el Arduino.
2. Abrir `midi_con_acordes.py`.
3. Seleccionar el puerto COM.
4. Seleccionar el puerto MIDI de loopMIDI.
5. Elegir el modo de funcionamiento.
6. Configurar los parámetros musicales.
7. Presionar **CONECTAR**.

El controlador estará listo para utilizarse. Para escuchar los sonidos, se necesita un instrumento o programa compatible con MIDI conectado al puerto virtual.

## 6. Capturas de pantalla

### Interfaz principal

<img width="621" height="845" alt="WhatsApp Image 2026-11-18 at 12 08 17 PM" src="https://github.com/user-attachments/assets/b75a4951-caa2-4ee6-bce8-6000129cdfc9" />


### Configuración de acordes

<img width="403" height="618" alt="WhatsApp Image 2026-11-18 at 12 08 32 PM" src="https://github.com/user-attachments/assets/e3351ca6-f506-4945-8534-80c20ac31f6c" />


### Selección de modos

<img width="613" height="832" alt="WhatsApp Image 2026-11-18 at 12 08 47 PM" src="https://github.com/user-attachments/assets/43ea709a-2676-4761-95e2-187174686885" />


### Sistema conectado

<img width="811" height="847" alt="WhatsApp Image 2026-11-18 at 12 11 14 PM" src="https://github.com/user-attachments/assets/d6689ae9-acc9-4262-8989-b8a1b17240cd" />


## 7. Cambios respecto al anteproyecto

Durante el desarrollo se realizaron las siguientes modificaciones:

- Se pasó de 8 a 12 pulsadores.
- Se agregó un modo de reproducción de acordes.
- Se incorporó la configuración individual de los 12 botones.
- Se añadieron controles de octava, transposición y velocidad.
- Se desarrolló una interfaz gráfica más completa en Python.
- Se reemplazó la división del teclado en dos mitades por la configuración individual de cada botón.

No se incorporaron el LED ni el buzzer planteados originalmente. Tampoco se implementó la comunicación de retorno desde Python hacia Arduino.

Estos cambios permitieron ampliar las posibilidades musicales y la personalización del instrumento.

## 8. Funcionamiento general

El proyecto funciona en tres etapas:

1. **Arduino:** detecta las pulsaciones y envía los datos por USB.
2. **Python:** recibe los datos y calcula las notas o acordes correspondientes.
3. **MIDI:** envía las señales al puerto virtual de loopMIDI para reproducir los sonidos.

El resultado es un controlador MIDI físico que permite tocar notas y acordes mediante 12 pulsadores.
