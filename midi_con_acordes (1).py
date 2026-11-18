import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import mido
import threading

arduino = None
midi = None
conectado = False
notas_activas = {}
bloqueo = threading.Lock()
modo = "notas"
acordes_por_tecla = {i: "C Mayor" for i in range(12)}
intervalos_acordes = {
    "Mayor": [0, 4, 7],
    "Menor": [0, 3, 7],
    "Disminuido": [0, 3, 6],
    "Aumentado": [0, 4, 8],
    "Sus2": [0, 2, 7],
    "Sus4": [0, 5, 7],
    "Séptima (7)": [0, 4, 7, 10],
    "Mayor séptima (maj7)": [0, 4, 7, 11],
    "Menor séptima (m7)": [0, 3, 7, 10],
    "Menor maj7": [0, 3, 7, 11],
    "Semidisminuido (m7b5)": [0, 3, 6, 10]
}

tono = 0
octava = 4
transposicion = 0
velocidad = 100

teclas = {
    "C": 0,
    "C#": 1,
    "D": 2,
    "D#": 3,
    "E": 4,
    "F": 5,
    "F#": 6,
    "G": 7,
    "G#": 8,
    "A": 9,
    "A#": 10,
    "B": 11
}

def actualizar_valores(*args):
    global tono, octava, transposicion, velocidad

    tono = teclas[nota_var.get()]
    octava = int(octava_var.get())
    transposicion = int(trans_var.get())
    velocidad = int(vel_var.get())

def enviar_nota(indice, encendida):
    global notas_activas

    if midi is None:
        return

    with bloqueo:
        if encendida:
            # Esta lista y el cálculo original se conservan para el modo notas.
            notas = [72, 71, 69, 67, 65, 64, 62, 60, 59, 57, 55, 53]
            nota_base = notas[indice] + (octava - 4) * 12
            nota_base += tono + transposicion
            nota_base = max(0, min(127, nota_base))

            if modo == "notas":
                # Modo notas: se conserva exactamente el cálculo original.
                notas_a_encender = [nota_base]
            else:
                # Modo acordes: cada botón tiene asignada una raíz y un tipo
                # de acorde, independientes de la nota asociada al botón.
                nombre_acorde = acordes_por_tecla[indice]
                raiz, tipo_acorde = nombre_acorde.split(" ", 1)
                nota_raiz = 60 + (octava - 4) * 12 + teclas[raiz]
                nota_raiz += transposicion
                intervalos = intervalos_acordes[tipo_acorde]
                notas_a_encender = [
                    max(0, min(127, nota_raiz + intervalo))
                    for intervalo in intervalos
                ]

            enviadas = []
            for nota in notas_a_encender:
                midi.send(mido.Message(
                    "note_on",
                    note=nota,
                    velocity=velocidad,
                    channel=0
                ))
                enviadas.append(nota)

            notas_activas[indice] = enviadas

        else:
            if indice in notas_activas:
                notas = notas_activas.pop(indice)
                for nota in notas:
                    midi.send(mido.Message(
                        "note_off",
                        note=nota,
                        velocity=0,
                        channel=0
                    ))

def leer_arduino():
    global conectado

    while conectado:
        try:
            linea = arduino.readline().decode(
                "utf-8", errors="ignore"
            ).strip()

            if not linea:
                continue

            partes = linea.split(",")

            if len(partes) != 2:
                continue

            accion = partes[0]
            indice = int(partes[1])

            if 0 <= indice < 12:
                if accion == "ON":
                    enviar_nota(indice, True)

                elif accion == "OFF":
                    enviar_nota(indice, False)

        except Exception:
            break

def conectar():
    global arduino, midi, conectado

    if conectado:
        return

    try:
        puerto = puerto_var.get()
        nombre_midi = midi_var.get()

        arduino = serial.Serial(
            puerto,
            115200,
            timeout=1
        )

        midi = mido.open_output(nombre_midi)

        conectado = True

        hilo = threading.Thread(
            target=leer_arduino,
            daemon=True
        )
        hilo.start()

        estado_var.set("Conectado")

    except Exception as error:
        conectado = False
        messagebox.showerror(
            "Error de conexión",
            str(error)
        )

def desconectar():
    global conectado, arduino, midi

    conectado = False

    with bloqueo:
        if midi:
            for notas in list(notas_activas.values()):
                for nota in notas:
                    midi.send(mido.Message(
                        "note_off",
                        note=nota,
                        velocity=0,
                        channel=0
                    ))

            notas_activas.clear()
            midi.close()
            midi = None

    if arduino:
        arduino.close()
        arduino = None

    estado_var.set("Desconectado")

def cerrar():
    desconectar()
    ventana.destroy()

ventana = tk.Tk()
ventana.title("Controlador MIDI Arduino")
ventana.geometry("500x650")
ventana.resizable(False, False)

nota_var = tk.StringVar(value="C")
octava_var = tk.StringVar(value="4")
trans_var = tk.StringVar(value="0")
vel_var = tk.IntVar(value=100)
puerto_var = tk.StringVar(value="COM5")
midi_var = tk.StringVar()
estado_var = tk.StringVar(value="Desconectado")
modo_var = tk.StringVar(value="notas")

for variable in (
    nota_var, octava_var, trans_var, vel_var
):
    variable.trace_add("write", actualizar_valores)

actualizar_valores()

titulo = ttk.Label(
    ventana,
    text="CONTROLADOR MIDI",
    font=("Arial", 17, "bold")
)
titulo.pack(pady=15)

marco = ttk.Frame(ventana, padding=15)
marco.pack(fill="both", expand=True)

ttk.Label(marco, text="Puerto Arduino:").pack(anchor="w")

puertos = [
    p.device for p in serial.tools.list_ports.comports()
]

puerto_menu = ttk.Combobox(
    marco,
    textvariable=puerto_var,
    values=puertos
)
puerto_menu.pack(fill="x", pady=5)

ttk.Label(marco, text="Puerto MIDI de loopMIDI:").pack(anchor="w")

salidas = mido.get_output_names()

midi_menu = ttk.Combobox(
    marco,
    textvariable=midi_var,
    values=salidas,
    state="readonly"
)
midi_menu.pack(fill="x", pady=5)

if salidas:
    coincidencia = next(
        (p for p in salidas if "Arduino MIDI" in p),
        salidas[0]
    )
    midi_var.set(coincidencia)

ttk.Label(marco, text="Modo de funcionamiento:").pack(anchor="w")
modo_menu = ttk.Combobox(
    marco,
    textvariable=modo_var,
    values=["notas", "acordes"],
    state="readonly"
)
modo_menu.pack(fill="x", pady=5)

def cambiar_modo(*args):
    global modo
    modo = modo_var.get()

modo_menu.bind("<<ComboboxSelected>>", cambiar_modo)

def configurar_acordes():
    ventana_acordes = tk.Toplevel(ventana)
    ventana_acordes.title("Asignar acordes a los 12 botones")
    ventana_acordes.geometry("390x520")
    ventana_acordes.resizable(False, False)

    contenedor = ttk.Frame(ventana_acordes, padding=12)
    contenedor.pack(fill="both", expand=True)

    ttk.Label(
        contenedor,
        text="Elegí el acorde que reproduce cada botón",
        font=("Arial", 11, "bold")
    ).pack(pady=(0, 8))

    ttk.Label(
        contenedor,
        text="Cada botón puede tener una nota raíz y un tipo de acorde distintos."
    ).pack(pady=(0, 10))

    raices = list(teclas.keys())
    opciones_acordes = [
        f"{raiz} {tipo}"
        for raiz in raices
        for tipo in intervalos_acordes
    ]

    variables_acordes = {}
    for indice in range(12):
        fila = ttk.Frame(contenedor)
        fila.pack(fill="x", pady=3)

        ttk.Label(
            fila,
            text=f"Botón {indice + 1}:",
            width=11
        ).pack(side="left")

        variable = tk.StringVar(value=acordes_por_tecla[indice])
        variables_acordes[indice] = variable

        ttk.Combobox(
            fila,
            textvariable=variable,
            values=opciones_acordes,
            state="readonly",
            width=29
        ).pack(side="right", fill="x", expand=True)

    def guardar_acordes():
        for indice, variable in variables_acordes.items():
            acordes_por_tecla[indice] = variable.get()

        ventana_acordes.destroy()
        messagebox.showinfo(
            "Acordes guardados",
            "Se guardaron los acordes asignados a los 12 botones."
        )

    ttk.Button(
        contenedor,
        text="GUARDAR",
        command=guardar_acordes
    ).pack(pady=12)

ttk.Button(
    marco,
    text="CONFIGURAR ACORDES",
    command=configurar_acordes
).pack(fill="x", pady=5)

ttk.Label(marco, text="Tonalidad:").pack(anchor="w")

ttk.Combobox(
    marco,
    textvariable=nota_var,
    values=list(teclas.keys()),
    state="readonly"
).pack(fill="x", pady=5)

ttk.Label(marco, text="Octava:").pack(anchor="w")

ttk.Spinbox(
    marco,
    from_=0,
    to=8,
    textvariable=octava_var
).pack(fill="x", pady=5)

ttk.Label(marco, text="Transposición (semitonos):").pack(anchor="w")

ttk.Spinbox(
    marco,
    from_=-24,
    to=24,
    textvariable=trans_var
).pack(fill="x", pady=5)

ttk.Label(marco, text="Velocidad:").pack(anchor="w")

ttk.Scale(
    marco,
    from_=1,
    to=127,
    variable=vel_var,
    orient="horizontal"
).pack(fill="x", pady=5)

botones = ttk.Frame(marco)
botones.pack(pady=15)

ttk.Button(
    botones,
    text="CONECTAR",
    command=conectar
).pack(side="left", padx=5)

ttk.Button(
    botones,
    text="DESCONECTAR",
    command=desconectar
).pack(side="left", padx=5)

ttk.Label(
    marco,
    textvariable=estado_var,
    font=("Arial", 11, "bold")
).pack(pady=10)

ventana.protocol("WM_DELETE_WINDOW", cerrar)
ventana.mainloop()
