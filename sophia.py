from PIL import Image

global mi_unicode
mi_unicode = {
    '"': 404,
    "'": 405,
    " ": 0,
    "\n":1, 
    "a": 2,
    "b": 3,
    "c": 4,
    "d": 5,
    "e": 10,
    "f": 11,
    "g": 12,
    "h": 13,
    "i": 14,
    "j": 15,
    "k": 20,
    "l": 21,
    "m": 22,
    "n": 23,
    "ñ": 24,
    "o": 25,
    "p": 30,
    "q": 31,
    "r": 32,
    "s": 33,
    "t": 34,
    "u": 35,
    "v": 40,
    "w": 41,
    "x": 42,
    "y": 43,
    "z": 44,
    "A": 100,
    "B": 101,
    "C": 102,
    "D": 103,
    "E": 104,
    "F": 105,
    "G": 110,
    "H": 111,
    "I": 112,
    "J": 113,
    "K": 114,
    "L": 115,
    "M": 120,
    "N": 121,
    "Ñ": 122,
    "O": 123,
    "P": 124,
    "Q": 125,
    "R": 130,
    "S": 131,
    "T": 132,
    "U": 133,
    "V": 134,
    "W": 135,
    "X": 140,
    "Y": 141,
    "Z": 142,
    "0": 200,
    "1": 201,
    "2": 202,
    "3": 203,
    "4": 204,
    "5": 210,
    "6": 211,
    "7": 212,
    "8": 213,
    "9": 214,
    ",": 300,
    ".": 301,
    ";": 302,
    ":": 303,
    "?": 304,
    "{": 305,
    "}": 310,
    "[": 311,
    "]": 312,
    "/": 400,
    "-": 401,
    "+": 402,
    "*": 403,
    "_": 410,
}

def desencriptar(rutaPlantilla, rutaOutput):

    plantilla = Image.open(rutaPlantilla)

    matriz=list(plantilla.getdata())

    def reverse(valor):
        return next((k for k, v in mi_unicode.items() if v == valor), None)

    flat=[]
    flatNums=[]
    for row in matriz:
        for i in row:
            i=str(i)
            flat.append(i[-1])

    for x in flat:
        x=int(x)
        flatNums.append(x)
    flatNums= [flatNums[i:i+3] for i in range(0, len(flatNums), 3)]
    flatNums= [[int(''.join(map(str, fila)))] for fila in flatNums]
    # puta si lo lees

    flatNums = [int(''.join(map(str, fila))) for fila in flatNums]

    mensaje = []
    for n in flatNums:
        if n == 999:        # terminador
            break
        mensaje.append(reverse(n))

    if rutaOutput==None:
        return "".join(mensaje)
    else:
        with open(rutaOutput, "w", encoding="utf-8") as out:
            out.write("".join(mensaje))


def luoscode(c):
    if c not in mi_unicode:
        raise ValueError (f"{c} cannot be passed as a encryptable character")
    return mi_unicode[c]

def encriptar(RutaPlantilla, mensaje):
    plantilla= Image.open(RutaPlantilla).convert("RGB")

    caracteres=[]
    numeros=[]
    for i in mensaje:
        i=luoscode(i)
        i=str(i)
        if len(i)==2:
            caracteres.append("0")
        elif len(i)==1:
            if i==" ":
                continue
            caracteres.append("0")
            caracteres.append("0")
        caracteres.append(i)
    caracteres.append("999")    # terminador
    for a in caracteres:
        a=str(a)
        numeros.append(a[0])
        if len(a)==3:
            numeros.append(a[1])
            numeros.append(a[2])
        elif len(a)==2:
            numeros.append(a[1])
    numeros=[int(x) for x in numeros]

    flatPixels = [min(num - (num % 10), 240) for px in plantilla.getdata() for num in px]

    mapaCifrado=[]

    for i in range(max(len(flatPixels), len(numeros))):
        if i < len(flatPixels) and i < len(numeros):
            mapaCifrado.append(flatPixels[i] + numeros[i])
        elif i < len(flatPixels):
            mapaCifrado.append(flatPixels[i])
        else:
            mapaCifrado.append(numeros[i])
    while len(mapaCifrado) % 3 != 0:
        mapaCifrado.append(0)

    matrizCifrada = [mapaCifrado[i:i+3] for i in range(0, len(mapaCifrado), 3)]
    while len(mapaCifrado) % 3 != 0:
        mapaCifrado.append(0)

    final = Image.new("RGB", plantilla.size)
    final.putdata([tuple(px) for px in matrizCifrada])
    final.save("DatosCifrados.png")

    print("Mensaje cifrado correctamente")
    return None


def encriptar_archivo(RutaPlantilla, rutaArchivo):

    plantilla = Image.open(RutaPlantilla).convert("RGB")

    flatPixels = [min(num - (num % 10), 240) for px in plantilla.getdata() for num in px]

    def rawfile(path):
        with open(path, "r", encoding="utf-8", newline="") as f:
            return f.read()

    archivoCifrado = [luoscode(c) for c in rawfile(rutaArchivo)]

    flatCrypted = []
    for k in archivoCifrado:
        for digit in str(k).zfill(3):
            flatCrypted.append(int(digit))

    flatCrypted += [9, 9, 9]

    if len(flatCrypted) > len(flatPixels):
        raise ValueError("El archivo es demasiado grande para esta imagen")

    fullMatrix = []
    for i in range(len(flatPixels)):
        if i < len(flatCrypted):
            fullMatrix.append(flatPixels[i] + flatCrypted[i])
        else:
            fullMatrix.append(flatPixels[i])

    finalMatrix = [tuple(fullMatrix[i:i+3]) for i in range(0, len(fullMatrix), 3)]

    final = Image.new("RGB", plantilla.size)
    final.putdata(finalMatrix)
    final.save("DatosCifrados.png")

    print("Archivo Cifrado correctamente")

encriptar_archivo(r"/home/luos/Documentos/programas/cosas/otras cosas/benson.png", r"/home/luos/Documentos/programas/Python/cosas/archivo.json")

desencriptar(r"/home/luos/Documentos/programas/DatosCifrados.png", r"/home/luos/Documentos/programas/output")