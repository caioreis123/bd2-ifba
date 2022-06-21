import csv

import pandas as pd


def ja_foram_avaliados_juntos(item, item2, lista_item1_item2_frequencia):
    for i in range(0, len(lista_item1_item2_frequencia)):
        if item in lista_item1_item2_frequencia[i] and item2 in lista_item1_item2_frequencia[i]:
            return True
    return False


def apriori(dataframe, suporte_minimo):
    dataset = dataframe.values
    total_de_compras = len(dataset)

    # criamos uma lista com todos os itens
    lista_itens = [item for item in dataframe.columns if item != 'TID']


    # criamos um dicionario em que as chaves são os nomes dos itens e seus valores são a frequencia em que eles aparecem na base de dados
    item_frequencia = {}
    for item in lista_itens:
        item_frequencia[item] = sum(dataframe[item].array)

    # filtramos os items com confianças menores que o minimo
    item_frequencia_filtrado = {}
    for item, frequencia in item_frequencia.items():
        suporte_do_item = frequencia/total_de_compras
        if suporte_do_item > suporte_minimo:
            item_frequencia_filtrado[item] = frequencia

    # agora pegamos esse dicionario filtrado e comparamos os itens 2 a 2 buscando a frequencia em que eles aparacem juntos e colocando esses dados uma lista
    item1_item2_frequencia = []  # exemplo: [['pao', 'leite', '3'], ['leite', 'cafe', '5']]
    for item, frequencia in item_frequencia_filtrado.items():
        for item2, frequencia2 in item_frequencia_filtrado.items():
            if item == item2:
                continue
            frequencia_juntos = 0
            if ja_foram_avaliados_juntos(item, item2, item1_item2_frequencia):
                continue
            for i in range(0, total_de_compras):
                id_do_item = lista_itens.index(item)
                id_do_item2 = lista_itens.index(item2)
                compra = dataset[i][1:] # necessario para nao contar com o TID
                if compra[id_do_item] == 1 and compra[id_do_item2] == 1:
                    frequencia_juntos += 1
            item1_item2_frequencia.append([item, item2, frequencia_juntos])

    # agora vamos filtrar a ultima lista deixando apenas as duplas que possuem um suporte maior que o minimo
    item1_item2_frequencia_filtrada = []
    for i in range(len(item1_item2_frequencia)):
        frequencia_da_dupla = item1_item2_frequencia[i][2]
        suporte_da_dupla = frequencia_da_dupla / total_de_compras
        if suporte_da_dupla > suporte_minimo:
            item1_item2_frequencia_filtrada.append(item1_item2_frequencia[i])

    # agora vamos calcular o support e confianca de cada dupla, e escrever um arquivo csv com esses dados
    with open('./data/resultado.csv', mode='w') as arquivo:
        escritor = csv.writer(arquivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        escritor.writerow(['ANTECEDENTE', 'CONSEQUENTE', 'CONFIANCA', 'SUPORTE'])

        # identificar qual dos produtos de cada dupla será o antecedente e qual será o consequente
        for dupla in item1_item2_frequencia_filtrada: # exemplo: [['pao', 'leite', '3']
            item, item2, frequencia_da_dupla = dupla
            frequencia1 = item_frequencia_filtrado[item] #exemplo:{'pao': 3, 'leite': 2, 'cafe': 5}
            frequencia2 = item_frequencia_filtrado[item2]
            suporte_da_dupla = frequencia_da_dupla / total_de_compras
            suporte1 = frequencia1/total_de_compras
            suporte2 = frequencia2/total_de_compras
            if suporte1 < suporte2: # priorizamos o menor suporte, pois isso vai levar a uma confianca maior, conf=sup(xUy)/sup(x) ou conf=freq(xUy)/freq(x)
                antecedente = item
                consequente = item2
                suporte_do_antecedente = suporte1
            else:
                antecedente = item2
                consequente = item
                suporte_do_antecedente = suporte2

            frequencia_do_antecedente = item_frequencia_filtrado[antecedente]
            confianca = frequencia_da_dupla / frequencia_do_antecedente
            confianca_alt = suporte_da_dupla/suporte_do_antecedente # essa confianca alternativa é so para demonstrar as duas formas diferentes de se calcular a confianca
            assert confianca == confianca_alt
            escritor.writerow([antecedente, consequente, confianca, suporte_da_dupla])


if __name__ == "__main__":
    # suporte é a frequência em que um item aparece com relação ao total
    # confiança mede a frequência do item A em que o item B aparece. (As ocorrências totais do antecedente fica no denominador, enquanto no numerador fica a quantidade de ocorrência comum). x+y/x
    entrada = pd.read_csv('./data/data.csv')
    suporte_minimo = 0.2
    apriori(entrada, suporte_minimo)
    saida = pd.read_csv('./data/resultado.csv')
    print(saida)
