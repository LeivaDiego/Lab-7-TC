from gramatica import Gramatica


g1 = Gramatica()
g2 = Gramatica()

g1.load_grammar("gramatica1.txt")
g1.remover_epsilon_productions()
pause = input("\npresione enter para continuar...\n")
g2.load_grammar("gramatica2.txt")
g2.remover_epsilon_productions()