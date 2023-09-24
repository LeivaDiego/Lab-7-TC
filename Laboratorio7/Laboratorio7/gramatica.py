import re

# Clase que representa una gramatica
class Gramatica:
    
    # Inicializador de la clase
    def __init__(self):
        self.producciones = {}
        self.correcta = True

    # Valida una linea de la gramatica con la regex
    def validate_line(self, linea):
        # Regex en la que se basa la validacion
        # regex = r"^[A-Z]->([A-Za-z0-9]+|ε)(\|[A-Za-z0-9]+|\|ε)*$"

        # 1. Verificar la estructura general
        if "->" not in linea:
            return False, "La produccion no contiene '->'"
        
        cabeza, cuerpos_str = linea.split("->")
        
        # 2. Verificar la cabeza de la produccion
        cabeza = cabeza.strip()
        if not re.match(r"^[A-Z]$", cabeza):
            return False, f"El inicio de la produccion '{cabeza}' no es una letra mayuscula unica"
        
        # 3. Verificar los cuerpos de la produccion
        cuerpos = cuerpos_str.split("|")
        for cuerpo in cuerpos:
            cuerpo = cuerpo.strip()
            if not re.match(r"^[A-Za-z0-9]+|ε$", cuerpo):
                return False, f"La produccion'{cuerpo}' no es valida"
        
        return True, ""

    # carga la producciones de una gramatica de un archivo
    def load_grammar(self, archivo):
        valid = True
        msg = ""
        gramatica = []

        with open(archivo, 'r', encoding='utf-8') as f:
            for linea in f:
                # Limpieza de espacios innecesarios al principio y al final
                linea = linea.strip()
                gramatica.append(linea)

                # validacion de gramatica
                validado, mensaje = self.validate_line(linea)
                if not validado:
                    valid = False
                    print(f"Error en la linea '{linea}': {mensaje}")
                else:
                    cabeza, cuerpos_str = linea.split('->')
                    self.producciones[cabeza.strip()] = [cuerpo.strip() for cuerpo in cuerpos_str.split("|")]

        print("La gramatica:")
        for linea in gramatica:
            print(linea)
        if valid:
            print("es valida\n")
            self.correcta = True
        else:
            print("no es valida\n")
            self.correcta = False