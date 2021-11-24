import datetime

def f_periodo_de_ate(de,ate,fmt):
    '''
    Função que retorna uma lista com todas as data de
    um determinado periodo.

    Parametros:
        de: data inicial, formato datetime
        ate: data final, formato datetime
        fmt: formato de saida de data
    '''

    date_list = []
    ini = de
    if ini == ate:
        return list([ini])
    else:
        while(ini <= ate):
            date_list.append(ini)
            ini = ini + datetime.timedelta(days=1)


        l = []
        for i in date_list:
            if i.strftime(fmt) not in l:
                l.append(i.strftime(fmt))
        return l

def f_periodo(dias):
    '''
    usar a funcao f_periodo_v6 pois a mesma contempla varias
    melhorias
    '''

    out = ''

    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(0, dias)]

    for i in date_list:
        data = str(i.year)[2:] + str(i.month).zfill(2) + str(i.day).zfill(2)
        df_1,df_2,df_3,df_4,df_t2,df_t = f_main(data)
        out += f_difv(df_t,data)
        out += f_difc(df_t2,data)

    return out

def f_periodo_V2(dias):
    '''
    usar a funcao f_periodo_v6 pois a mesma contempla varias
    melhorias
    '''
    
    out = ''

    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(0, dias)]

    return date_list

def f_periodo_V3(dias):
    '''
    usar a funcao f_periodo_v6 pois a mesma contempla varias
    melhorias
    '''

    dias = f_periodo_V2(dias=dias)

    lista = []

    for dia in dias:
        lista.append(str(1) + str(dia.year)[2:].zfill(2) + str(dia.month).zfill(2) + str(dia.day).zfill(2))

    return lista
	
def f_periodo_V4(dias):
    '''
    usar a funcao f_periodo_v6 pois a mesma contempla varias
    melhorias
    '''

    dias = f_periodo_V2(dias=dias)

    lista = []

    for dia in dias:
        lista.append(str(20) + str(dia.year)[2:].zfill(2) + '-' + str(dia.month).zfill(2) + '-' + str(dia.day).zfill(2))

    return lista

def f_periodo_V5(dias):
    '''
    usar a funcao f_periodo_v6 pois a mesma contempla varias
    melhorias
    '''

    l = []
    
    for i in f_periodo_V2(dias):
        l.append(int(str(i.day) + str(i.month).zfill(2) + str(i.year)[2:4]))
    
    return l
    
def f_periodo_v6(fmt,dias):
    '''
    funcao ideal para formatacao de data, pois pega o formato informado
    e retorna uma lista com valores unicos
    '''
        
    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(0, dias)]
    
    l = []
    for i in date_list:
        if i.strftime(fmt) not in l:
            l.append(i.strftime(fmt))
    
    return l
