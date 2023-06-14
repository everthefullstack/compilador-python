def create_txt(lexer):
    #cria lista de tokens e imprime
    lista = []
    #caso tenha um erro, printa, mas não prossegue com a análise
    try:
        while True:
            token = lexer.token()
            
            if not token:
                break

            lista.append(token)

    except Exception as error:
        print(error)
        pass

    saida_txt = open("lex.txt", "w")

    for l in lista:
        saida_txt.write(str(l))
        saida_txt.write("\n")

    saida_txt.close()