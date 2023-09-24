import re
from itertools import combinations

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
                return False, f"La produccion '{cuerpo}' no es valida"
        
        return True, ""

    # carga la producciones de una gramatica de un archivo
    def load_grammar(self, archivo):
        valid = True
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


    # Identificar simbolos anulables
    def find_nullables(self):
        print("\n--- Comenzando el proceso para identificar simbolos anulables ---")
        anulables = set()
        cambios = True

        while cambios:
            print("\nRealizando una iteracion para encontrar mas simbolos anulables")
            cambios = False

            for cabeza, cuerpos in self.producciones.items():
                for cuerpo in cuerpos:
                    print(f"\n Evaluando la produccion: {cabeza} -> {cuerpo}")

                    # Si el cuerpo es ε o todos sus simbolos son anulables y son no terminales
                    if cuerpo == "ε":
                        print("El cuerpo es ε")
                        if cabeza not in anulables:
                            print(f"Añadiendo {cabeza} a los simbolos anulables")
                            anulables.add(cabeza)
                            cambios = True
                        else:
                            print(f"{cabeza} ya esta en los simbolos anulables")

                    elif all([simbolo in anulables for simbolo in cuerpo if simbolo.isupper()]):
                        print("Todos los simbolos del cuerpo son anulables")
                        if cabeza not in anulables:
                            print(f"Añadiendo {cabeza} a los simbolos anulables")
                            anulables.add(cabeza)
                            cambios = True
                        else:
                            print(f"{cabeza} ya esta en los simbolos anulables")
                    else:
                        print(f"El cuerpo no es ε y no todos sus simbolos son anulables")

        print("\n--- Finalizando el proceso de identificacion de simbolos anulables ---")
        return anulables


    # Generar nuevas producciones considerando los simbolos anulables
    def generate_non_epsilon_productions(self, anulables):
        print("\n--- Comenzando el proceso para generar producciones sin ε ---")
        nuevas_producciones = {}

        for cabeza, cuerpos in self.producciones.items():
            print(f"\nEvaluando las producciones para: {cabeza}")
            nuevas_producciones[cabeza] = []

            for cuerpo in cuerpos:
                print(f" Evaluando el cuerpo: {cuerpo}")
                # Si el cuerpo no es ε
                if cuerpo != "ε":
                    indices_anulables = [i for i, simbolo in enumerate(cuerpo) if simbolo in anulables]
                    print(f"Indices de simbolos anulables en el cuerpo: {indices_anulables}")

                    # Generar todas las combinaciones posibles de reemplazo
                    print("Generando combinaciones para reemplazo")
                    for i in range(len(indices_anulables) + 1):
                        for combinacion in combinations(indices_anulables, i):
                            print(f" Generando nuevo cuerpo para la combinacion {combinacion}")
                            nuevo_cuerpo = ''.join([cuerpo[j] for j in range(len(cuerpo)) if j not in combinacion])
                            if nuevo_cuerpo:
                                print(f"Nueva produccion generada: {cabeza} -> {nuevo_cuerpo}")
                                nuevas_producciones[cabeza].append(nuevo_cuerpo)
                else:
                    print("El cuerpo es ε, no se toma en cuenta")

            # Eliminar duplicados
            print(f"Actualizando producciones para {cabeza} sin duplicados")
            nuevas_producciones[cabeza] = list(set(nuevas_producciones[cabeza]))

        print("\n--- Finalizando el proceso de generacion de producciones sin ε ---\n")
        self.producciones = nuevas_producciones




    # Remover producciones-ε de la gramatica
    def remover_epsilon_productions(self):
        if self.correcta:
            print("Eliminando producciones-ε de la gramatica")
        
            # Paso 1: Encontrar simbolos anulables
            anulables = self.find_nullables()
            print(f"Simbolos anulables identificados: {', '.join(anulables)}\n")
        
            # Paso 2: Generar nuevas producciones sin ε
            self.generate_non_epsilon_productions(anulables)
            print("Nuevas producciones sin ε generadas:")
            for cabeza, cuerpos in self.producciones.items():
                print(f"{cabeza} -> {' | '.join(cuerpos)}")
        
            # Paso 3: Eliminar las producciones que derivan solo ε
            # (Nota: Este paso ya esta integrado en el metodo generate_non_epsilon_productions)
            print("\nLas producciones-ε de la gramatica han sido eliminadas\n") 
        else:
            print("\nNo se puede usar esta gramatica porque no es valida\n")