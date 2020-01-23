def calcularMaximoIngreso(listaA):
    copiaA = listaA
    inicio = 0
    resta = (0, 0, 0)

    while copiaA:
        maxRel = copiaA.index(max(copiaA))
        #    print(copiaA[inicio:maxRel], 'a')
        minRel = copiaA.index(min(copiaA[:maxRel+1]))
        #    print(copiaA, minRel, maxRel)
        if copiaA[maxRel]-copiaA[minRel] > resta[0]:
            diff = len(listaA)-len(copiaA)
            resta = (copiaA[maxRel]-copiaA[minRel], minRel+diff, maxRel+diff)

        inicio = maxRel+1
        copiaA = copiaA[inicio:]
    return resta

if _name_ == "__main__":
    listaA = [1, 4, 5, 2, 4] # [12, 1, 4, 5, 2, 4], [2,15,4,1,2], [1, 4, 5, 2, 4]
    resta = calcularMaximoIngreso(listaA)

    print("El ingreso maximo era de {} si se compraba el dia {} y se vendia el dia {}".format(resta[0], resta[1], resta[2]))