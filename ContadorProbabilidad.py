
import csv
import os
from collections import Counter

ARCHIVO_TIRADAS = "registro_tiradas.csv"
ARCHIVO_PERSONALIZADOS = "dados_personalizados.csv"

DADOS_ESTANDAR = [4, 6, 8, 10, 12, 20, 21]

registros = []
dados_personalizados = {}


# =====================================
# CARGAR DATOS
# =====================================

def cargar_datos():

    global registros, dados_personalizados

    if os.path.exists(ARCHIVO_TIRADAS):
        with open(ARCHIVO_TIRADAS, newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f)

            for fila in lector:
                registros.append({
                    "dado": fila["dado"],
                    "resultado": int(fila["resultado"])
                })

    if os.path.exists(ARCHIVO_PERSONALIZADOS):
        with open(ARCHIVO_PERSONALIZADOS, newline="", encoding="utf-8") as f:
            lector = csv.DictReader(f)

            for fila in lector:
                nombre_dado = fila["dado"]
                numero = int(fila["numero"])
                nombre_cara = fila["nombre"]

                if nombre_dado not in dados_personalizados:
                    dados_personalizados[nombre_dado] = {}

                dados_personalizados[nombre_dado][numero] = nombre_cara


def guardar_tiradas():

    with open(ARCHIVO_TIRADAS, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["dado", "resultado"])

        for r in registros:
            escritor.writerow([r["dado"], r["resultado"]])


def guardar_dados_personalizados():

    with open(ARCHIVO_PERSONALIZADOS, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(["dado", "numero", "nombre"])

        for dado, caras in dados_personalizados.items():
            for numero, nombre in caras.items():
                escritor.writerow([dado, numero, nombre])


# =====================================
# CREAR DADO PERSONALIZADO
# =====================================

def crear_dado():

    print("\n=== CREAR DADO PERSONALIZADO ===")

    nombre = input("Nombre del dado: ").strip()

    if not nombre:
        print("El nombre no puede estar vacío.")
        return

    if nombre in dados_personalizados or nombre in [
        f"D{x}" for x in DADOS_ESTANDAR
    ]:
        print("Ya existe un dado con ese nombre.")
        return

    try:
        cantidad = int(input("Número de caras: "))

        if cantidad < 2:
            print("El dado debe tener al menos 2 caras.")
            return

    except ValueError:
        print("Introduce un número válido.")
        return

    caras = {}

    for numero in range(1, cantidad + 1):

        while True:
            nombre_cara = input(
                f"Nombre de la cara {numero}: "
            ).strip()

            if nombre_cara:
                caras[numero] = nombre_cara
                break

            print("El nombre no puede estar vacío.")

    dados_personalizados[nombre] = caras

    guardar_dados_personalizados()

    print(f"\n¡Dado '{nombre}' creado correctamente!")
    mostrar_caras(nombre)


# =====================================
# ELIMINAR DADO PERSONALIZADO
# =====================================

def eliminar_dado():

    if not dados_personalizados:
        print("\nNo hay dados personalizados para eliminar.")
        return

    print("\n=== ELIMINAR DADO PERSONALIZADO ===")

    lista_dados = list(dados_personalizados.keys())

    for i, dado in enumerate(lista_dados, 1):
        print(f"{i}. {dado}")

    print("0. Cancelar")

    try:
        opcion = int(input("\nSelecciona el dado que quieres eliminar: "))

        if opcion == 0:
            print("Operación cancelada.")
            return

        if opcion < 1 or opcion > len(lista_dados):
            print("Selección incorrecta.")
            return

        dado = lista_dados[opcion - 1]

        print(f"\nDado seleccionado: {dado}")

        confirmar = input(
            "¿Quieres eliminar este dado y todas sus tiradas? (S/N): "
        ).strip().upper()

        if confirmar == "S":

            del dados_personalizados[dado]

            global registros

            registros = [
                r for r in registros
                if r["dado"] != dado
            ]

            guardar_dados_personalizados()
            guardar_tiradas()

            print(f"\nEl dado '{dado}' ha sido eliminado.")
            print("Sus registros estadísticos también han sido eliminados.")

        else:
            print("\nOperación cancelada.")

    except ValueError:
        print("Introduce un número válido.")


# =====================================
# MOSTRAR CARAS
# =====================================

def mostrar_caras(dado):

    if dado.startswith("D"):
        cantidad = int(dado[1:])

        for numero in range(1, cantidad + 1):
            print(f"{numero}. Cara {numero}")

    else:
        for numero, nombre in dados_personalizados[dado].items():
            print(f"{numero}. {nombre}")


def obtener_caras(dado):

    if dado.startswith("D"):
        cantidad = int(dado[1:])
        return {
            numero: f"Cara {numero}"
            for numero in range(1, cantidad + 1)
        }

    return dados_personalizados[dado]


# =====================================
# SELECCIONAR DADO
# =====================================

def seleccionar_dado():

    opciones = [f"D{x}" for x in DADOS_ESTANDAR]
    opciones += list(dados_personalizados.keys())

    print("\n=== SELECCIONAR DADO ===")

    for i, dado in enumerate(opciones, 1):
        print(f"{i}. {dado}")

    try:
        opcion = int(input("\nSelecciona una opción: "))

        if 1 <= opcion <= len(opciones):
            return opciones[opcion - 1]

    except ValueError:
        pass

    print("Selección incorrecta.")
    return None


# =====================================
# ESTADÍSTICAS
# =====================================

def mostrar_estadisticas(dado):

    caras = obtener_caras(dado)

    tiradas = [
        r["resultado"]
        for r in registros
        if r["dado"] == dado
    ]

    contador = Counter(tiradas)
    total = len(tiradas)

    print("\n" + "=" * 40)
    print(f"ESTADÍSTICAS DEL DADO: {dado}")
    print("=" * 40)

    print(f"Total de tiradas: {total}")
    print(f"Probabilidad teórica por cara: {100/len(caras):.2f}%")

    print("-" * 40)
    print(f"{'NÚMERO':<10}{'NOMBRE':<10}{'VECES':<8}{'PROBABILIDAD'}")
    print("-" * 40)

    for numero, nombre in caras.items():

        frecuencia = contador[numero]

        porcentaje = (
            frecuencia / total * 100
            if total > 0 else 0
        )

        print(
            f"{numero:<10}{nombre[:10]:<10}"
            f"{frecuencia:<10}{porcentaje:.2f}%"
        )

    print("-" * 40)
    print(f"TOTAL DE TIRADAS: {total}")
    print("=" * 40)


# =====================================
# REGISTRAR TIRADAS
# =====================================

def registrar_tiradas():

    dado = seleccionar_dado()

    if dado is None:
        return

    caras = obtener_caras(dado)
    cantidad = len(caras)

    print(f"\n=== REGISTRO DE {dado} ===")
    mostrar_caras(dado)

    mostrar_estadisticas(dado)

    print("\nIntroduce el número obtenido.")
    print("Escribe 0 para volver al menú.")

    while True:

        try:
            resultado = int(input("\nResultado: "))

            if resultado == 0:
                break

            if resultado not in caras:
                print(f"Introduce un número entre 1 y {cantidad}.")
                continue

            registros.append({
                "dado": dado,
                "resultado": resultado
            })

            guardar_tiradas()

            print(f"\nResultado registrado: {caras[resultado]}")

            # Actualizar estadísticas automáticamente
            mostrar_estadisticas(dado)

        except ValueError:
            print("Introduce un número entero válido.")


# =====================================
# CONSULTAR ESTADÍSTICAS
# =====================================

def consultar_estadisticas():

    dado = seleccionar_dado()

    if dado is not None:
        mostrar_estadisticas(dado)


# =====================================
# REINICIAR REGISTROS
# =====================================

def reiniciar_registros():

    global registros

    print("\n1. Reiniciar todos los dados")
    print("2. Reiniciar un dado concreto")
    print("3. Cancelar")

    opcion = input("\nSelecciona: ")

    if opcion == "1":

        confirmar = input("¿Borrar todas las tiradas? (S/N): ").upper()

        if confirmar == "S":
            registros = []
            guardar_tiradas()
            print("Todos los registros han sido eliminados.")

    elif opcion == "2":

        dado = seleccionar_dado()

        if dado is not None:

            confirmar = input(
                f"¿Borrar las tiradas de {dado}? (S/N): "
            ).upper()

            if confirmar == "S":

                registros = [
                    r for r in registros
                    if r["dado"] != dado
                ]

                guardar_tiradas()
                print(f"Registros de {dado} eliminados.")



# =====================================
# MENÚ PRINCIPAL
# =====================================

def menu():

    while True:

        print("\n" + "=" * 40)
        print("               CONTADOR")
        print("             PROBABILIDAD")
        print("-" * 40)
        print("By:Valbef                     v1.0.0")
        print("=" * 40)

        print("1. Registrar tiradas")
        print("2. Consultar estadísticas")
        print("3. Crear dado personalizado")
        print("4. Eliminar dado personalizado")
        print("5. Reiniciar registros")
        print("6. Salir")

        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":
            registrar_tiradas()

        elif opcion == "2":
            consultar_estadisticas()

        elif opcion == "3":
            crear_dado()

        elif opcion == "4":
            eliminar_dado()

        elif opcion == "5":
            reiniciar_registros()

        elif opcion == "6":
            print("\nDatos guardados. Hasta pronto.")
            break

        else:
            print("Opción incorrecta.")


# =====================================
# INICIAR PROGRAMA
# =====================================

cargar_datos()
menu()
