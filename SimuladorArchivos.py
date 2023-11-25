import os
import datetime

class Archivo:
    def __init__(self, nombre, contenido=""):
        self.nombre = nombre
        self.contenido = contenido
        self.permisos = "755"

class Directorio:
    def __init__(self, nombre, padre=None):
        self.nombre = nombre
        self.padre = padre
        self.archivos = {}
        self.subdirectorios = {}

class SistemaDeArchivos:
    def __init__(self):
        self.raiz = Directorio("root")
        self.directorio_actual = self.raiz
        self.historico_comandos = []

    def ejecutar_comando(self, comando):
        self.historico_comandos.append((comando, datetime.datetime.now()))
        partes = comando.split()
        cmd = partes[0]

        try:
            if cmd == "mkdir" and len(partes) > 1:
                self.mkdir(partes[1])
            elif cmd == "pwd":
                print(self.pwd())
            elif cmd == "ls":
                self.ls()
            elif cmd == "cd" and len(partes) > 1:
                self.cd(partes[1])
            elif cmd.startswith("cat"):
                self.cat(comando[4:])
            elif cmd == "mv" and len(partes) > 2:
                self.mv(partes[1], partes[2])
            elif cmd == "rm" and len(partes) > 1:
                self.rm(partes[1])
            elif cmd == "chmod" and len(partes) > 2:
                self.chmod(partes[1], partes[2])
            elif cmd == "format":
                self.format()
            elif cmd == "cls":
                self.cls()
            elif cmd == "history":
                self.history()
            else:
                print("Comando no reconocido o faltan argumentos.")
        except Exception as e:
            print("Error:", e)

    def mkdir(self, nombre):
        if nombre in self.directorio_actual.subdirectorios:
            print(f"El directorio '{nombre}' ya existe.")
        else:
            self.directorio_actual.subdirectorios[nombre] = Directorio(nombre, self.directorio_actual)

    def pwd(self):
        directorio = self.directorio_actual
        ruta = ""
        while directorio:
            ruta = "/" + directorio.nombre + ruta
            directorio = directorio.padre
        return ruta

    def ls(self):
        if not self.directorio_actual.subdirectorios and not self.directorio_actual.archivos:
            print("No hay archivos o directorios en la ubicación actual.")
        else:
            for nombre in self.directorio_actual.subdirectorios:
                print("Dir -", nombre)
            for nombre in self.directorio_actual.archivos:
                print("File -", nombre)

    def cd(self, nombre):
        if nombre == "..":
            if self.directorio_actual.padre is None:
                print("No hay directorio padre.")
            else:
                self.directorio_actual = self.directorio_actual.padre
        elif nombre in self.directorio_actual.subdirectorios:
            self.directorio_actual = self.directorio_actual.subdirectorios[nombre]
        else:
            print(f"Directorio '{nombre}' no encontrado.")

    def cat(self, comando):
        partes = comando.split()
        if len(partes) < 1:
            print("Error: comando inválido. Debe ser 'cat <nombre_archivo>'.")
            return
        if ">" in partes:
            indice = partes.index(">")
            nombre = partes[indice + 1]
            contenido = " ".join(partes[indice + 2:]) if len(partes) > indice + 2 else ""
            self.crear_archivo(nombre, contenido)
        else:
            nombre = partes[1]
            self.mostrar_contenido_archivo(nombre)


    def crear_archivo(self, nombre, contenido):
        self.directorio_actual.archivos[nombre] = Archivo(nombre, contenido)
        if nombre in self.directorio_actual.archivos:
            print(f"Archivo '{nombre}' creado.")
        else:
            print(f"Error al crear el archivo '{nombre}'.")


    def mostrar_contenido_archivo(self, nombre):
        if nombre in self.directorio_actual.archivos:
            print(self.directorio_actual.archivos[nombre].contenido)
        else:
            print(f"Archivo '{nombre}' no encontrado.")

    def mv(self, antiguo, nuevo):
        if antiguo in self.directorio_actual.archivos:
            self.directorio_actual.archivos[nuevo] = self.directorio_actual.archivos.pop(antiguo)
        elif antiguo in self.directorio_actual.subdirectorios:
            dir = self.directorio_actual.subdirectorios.pop(antiguo)
            dir.nombre = nuevo
            self.directorio_actual.subdirectorios[nuevo] = dir
        else:
            print(f"No se encontró '{antiguo}'")

    def rm(self, nombre):
        if nombre in self.directorio_actual.archivos:
            del self.directorio_actual.archivos[nombre]
        elif nombre in self.directorio_actual.subdirectorios:
            del self.directorio_actual.subdirectorios[nombre]
        else:
            print(f"No se encontró '{nombre}'")

    def chmod(self, nombre, permisos):
        if nombre in self.directorio_actual.archivos:
            self.directorio_actual.archivos[nombre].permisos = permisos
        else:
            print(f"Archivo '{nombre}' no encontrado.")

    def format(self):
        self.raiz = Directorio("root")
        self.directorio_actual = self.raiz
        print("Sistema de archivos formateado.")

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def history(self):
        for comando in self.historico_comandos:
            print(comando)

def main():
    fs = SistemaDeArchivos()
    print("Bienvenido al simulador de sistema de archivos.")
    while True:
        comando = input("$ ")
        fs.ejecutar_comando(comando)

if __name__ == "__main__":
    main()


#TODO: hacer 2 comandos para cat (cat >) y (cat )