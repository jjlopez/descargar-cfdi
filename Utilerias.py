class Utilerias:

    def mezcla_listas(self, listaA, listaB):
        resultante = listaA.copy()
        resultante.update(listaB)
        return resultante
