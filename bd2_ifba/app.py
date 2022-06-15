import csv

import pandas as pd


def ja_foram_avaliados_juntos(item, item2, lista_item1_item2_frequencia):
    for i in range(0, len(lista_item1_item2_frequencia)):
        if item in lista_item1_item2_frequencia[i] and item2 in lista_item1_item2_frequencia[i]:
            return True
    return False


def apriori(dataframe, min_confianca):
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
        if frequencia/len(lista_itens) > min_confianca:
            item_frequencia_filtrado[item] = frequencia

    # agora pegamos essa lista filtrada e comparamos os itens 2 a 2 buscando a frequencia em que eles aparacem juntos e colocando esses dados uma lista
    item1_item2_frequencia = []
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

    # agora vamos filtrar a ultima lista deixando apenas as duplas que possuem uma frequencia maior que o minimo
    item1_item2_frequencia_filtrada = []
    for i in range(len(item1_item2_frequencia)):
        if item1_item2_frequencia[i][2]/total_de_compras > min_confianca:
            item1_item2_frequencia_filtrada.append(item1_item2_frequencia[i])

    # agora vamos calcular o support de cada dupla e escrever um arquivo csv com esses dados
    with open('./data/resultado.csv', mode='w') as arquivo:
        escritor = csv.writer(arquivo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        escritor.writerow(['ANTECEDENTE', 'CONSEQUENTE', 'CONFIANCA', 'SUPORTE'])

        for dupla in item1_item2_frequencia_filtrada:
            item = dupla[0]
            item2 = dupla[1]
            frequencia_da_dupla = dupla[2]
            frequencia1 = item_frequencia_filtrado[item]
            frequencia2 = item_frequencia_filtrado[item2]
            suporte_da_dupla = frequencia_da_dupla / total_de_compras
            suporte1 = frequencia1/total_de_compras
            suporte2 = frequencia2/total_de_compras
            if suporte1 < suporte2:
                antecedente = item
                consequente = item2
            else:
                antecedente = item2
                consequente = item

            confianca = frequencia_da_dupla/item_frequencia_filtrado[antecedente]
            escritor.writerow([antecedente, consequente, confianca, suporte_da_dupla])


if __name__ == "__main__":
    entrada = pd.read_csv('./data/data.csv')
    min_confianca = 0.2
    apriori(entrada, min_confianca)
    saida = pd.read_csv('./data/resultado.csv')
    print(saida)
