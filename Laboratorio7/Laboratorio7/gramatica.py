import re

# Clase que representa una gramatica
class Gramatica:
    
    # Inicializador de la clase
    def __init__(self):
        self.producciones = {}

    # Valida una linea de la gramatica con la regex
    def validate_line(self, line):
        regex = r"^[A-Z]->([A-Za-z0-9]+|ε)(\|[A-Za-z0-9]+|\|ε)*$"
        return re.match(regex, line)

    # carga la producciones de una gramatica de un archivo
    def load_grammar(self, path):
        flag = True
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                # Limpieza de espacios innecesarios al principio y al final
                line = line.strip()
                if not self.validate_line(line):
                    print(f"La linea {line} no cumple")
                    flag = False
                else:
                    cabeza, cuerpos = line.split("->")
                    self.producciones = cuerpos.split("|")
        return flag

    def __str__(self):
        return '\n'.join([f"{k} -> {' | '.join(v)}" for k, v in self.producciones.items()])