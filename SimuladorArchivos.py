import os


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
        self.historico_comandos.append((comando))
        partes = comando.split()
        cmd = partes[0]

        comandos = {
            "mkdir": lambda: self.mkdir(partes[1]) if len(partes) > 1 else print("Se requiere un argumento para mkdir."),
            "pwd": lambda: print(self.pwd()),
            "ls": lambda: self.ls(partes[1] if len(partes) > 1 else None),
            "cd": lambda: self.cd(partes[1]) if len(partes) > 1 else print("Se requiere un argumento para cd."),
            "cat": lambda: self.cat(comando[4:]),
            "mv": lambda: self.mv(partes[1], partes[2]) if len(partes) > 2 else print("mv requiere dos argumentos."),
            "rm": lambda: self.rm(partes[1]) if len(partes) > 1 else print("Se requiere un argumento para rm."),
            "chmod": lambda: self.chmod(partes[1], partes[2]) if len(partes) > 2 else print("chmod requiere dos argumentos."),
            "format": self.format,
            "cls": self.cls,
            "history": self.history
        }

        try:
            if cmd in comandos:
                comandos[cmd]()
            else:
                print("Comando no reconocido o faltan argumentos.")
        except Exception as e:
            print(f"Error en comando {cmd}: {e}")


    def mkdir(self, nombre):
        if nombre in self.directorio_actual.subdirectorios:
            print(f"El directorio '{nombre}' ya existe.")
        else:
            self.directorio_actual.subdirectorios[nombre] = Directorio(
                nombre, self.directorio_actual
            )

    def pwd(self):
        directorio = self.directorio_actual
        ruta = ""
        while directorio:
            ruta = "/" + directorio.nombre + ruta
            directorio = directorio.padre
        return ruta

    def ls(self, ruta=None):
        directorio = self.directorio_actual
        if ruta:
            directorio = self.buscar_directorio(ruta)
            if not directorio:
                print(f"Directorio '{ruta}' no encontrado.")
                return

        if not directorio.subdirectorios and not directorio.archivos:
            print("No hay archivos o directorios en la ubicación actual.")
        else:
            for nombre in directorio.subdirectorios:
                print("Dir -", nombre)
            for nombre in directorio.archivos:
                print("File -", nombre)

    def buscar_directorio(self, ruta):
        partes = ruta.split("/")
        directorio = self.raiz if partes[0] == "root" else self.directorio_actual
        for parte in partes[1:]:
            if parte in directorio.subdirectorios:
                directorio = directorio.subdirectorios[parte]
            else:
                print(f"Directorio '{parte}' no encontrado.")
                return self.directorio_actual
        return directorio

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
            contenido = (
                " ".join(partes[indice + 2 :]) if len(partes) > indice + 2 else ""
            )
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
            self.directorio_actual.archivos[
                nuevo
            ] = self.directorio_actual.archivos.pop(antiguo)
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

    def permisos_a_cadena(self, permisos):
        representaciones = {
            "7": "rwx",
            "6": "rw-",
            "5": "r-x",
            "4": "r--",
            "3": "-wx",
            "2": "-w-",
            "1": "--x",
            "0": "---",
        }
        return "".join(representaciones.get(p, "---") for p in permisos)

    def chmod(self, permisos, nombre):
        if not permisos.isdigit() or not 000 <= int(permisos, 8) <= 777:
            print(
                "Error: los permisos deben ser un número octal de tres dígitos (000-777)."
            )
            return

        permisos_cadena = self.permisos_a_cadena(permisos)

        if nombre in self.directorio_actual.archivos:
            self.directorio_actual.archivos[nombre].permisos = permisos
            print(f"Permisos de '{nombre}' cambiados a {permisos} ({permisos_cadena}).")
        else:
            print(f"Archivo '{nombre}' no encontrado.")

    def format(self):
        self.raiz = Directorio("root")
        self.directorio_actual = self.raiz
        print("Sistema de archivos formateado.")

    def cls(self):
        os.system("cls" if os.name == "nt" else "clear")

    def history(self):
        for comando in self.historico_comandos:
            print(comando)


def main():
    fs = SistemaDeArchivos()
    os.system("cls" if os.name == "nt" else "clear")
    print("Simulador de Archivos.")
    while True:
        print(fs.pwd(), end=" ")
        comando = input("$ ")
        fs.ejecutar_comando(comando)


if __name__ == "__main__":
    main()


# TODO: hacer 2 comandos para cat (cat >) y (cat )
