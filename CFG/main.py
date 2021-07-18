import sys
import random

##epsilon este notat cu "epsilon" pentru a nu lua niciun caracter

def get_section(name, lista):
    flag = False
    l_ret = []
    for line in lista:
        if line.lower() == name.lower():   #trebuie sa fac caracterele mici, pt ca nu stiu cum sunt scrise in fisier
            flag = True
            continue
        if line.lower() == "end":
            flag = False
        if flag == True:
            l_ret.append(line)
    return l_ret        #vom avem lista cu valorile dintre numele dat si "end", numele fiind pe rand variabile,
                        #terminali, relatii

def load_config_file(file_name):    ##AICI INTRU PRIMA DATA
    lista=[]
    f=open(file_name)
    for line in f:
        line=line.strip()
        if len(line)>0:
            lista.append(line)              ##scap de liniile din fisier care sunt goale, presupun ca nu exista
                                            ##comentarii, intrucat '#' poate fi folosit ca si terminal
    variabile= get_section("Variabile:", lista)    #creez cele 3 sectiuni(3 liste)
    terminali= get_section("Terminali:", lista)
    relatii= get_section("Relatii:", lista)
                                          #aici se incepe verificarea validitatii sectiunilor
    ok=True
    for var in variabile:
        if var < 'A' or var >'Z':       #se stie ca variabilele sunt caractere cuprinse intre A si Z
            ok = False
    if ok == False:
        print("Este o problema la variabile")
    else:
        for term in terminali:            #terminalii sunt orice caracter cu exceptia celor care sunt variabile
                                                            #deci inainta de [A,Z]
            if term >='A' and term <='Z':
                ok=False
        if ok==False:
            print("Este o problema la terminali")
        else:                                  #o relatie este definata prin faptul ca in stanga trebuie sa fie
            l_relatii=[]                         #o variabila si in dreapta un string compus din variabile si terminali
            for x in relatii:
                y=x.split(",")
                l_relatii.append([y[0], y[1]])
                if y[0] not in variabile:        #daca in stanga nu se gaseste o variabila, nu este o relatie valida
                    print(f"({y[0]},{y[1]}) nu este o relatie")
                    ok=False
                else:
                    if y[1] != "epsilon":  #trebuie sa verific ca nu este epsilon, acesta nefacand parte din terminali
                        for lit in y[1]:
                            if lit not in variabile:              #daca in dreapta avem un caracter care nu este
                                if lit not in terminali:         #variabila si nici terminal, inseamna ca nu este relatie
                                    print(f"({y[0]},{y[1]}) nu este o relatie")
                                    ok = False
                relatii=l_relatii   #in acelasi timp creem si lista de liste cu relatii

    return variabile, terminali, relatii, ok

def schimbare (flag, cuv):
    flag = True  #presupunem ca nu mai exista variabile in cuvant
    i=0
    while i<len(cuv) and flag == True:
        if cuv[i] in variabile:
            var=cuv[i]
            flag = False
        i+=1
    if flag == False:  #inseamna ca a gasit o variabila
        i=i-1       #ma mutasem cu o pozitie inainte
        apartitii=0
        for lit in relatii:
            if var == lit[0]:
                apartitii+=1
        k=random.randint(1,apartitii)
        j=0     #iau a k a relatie care pleaca din variabila mea si o pun in cuvantul meu
        while k!=0 and  j<len(relatii):
            if var == relatii[j][0]:
                k-=1
            j+=1
        inainte = cuv[0:i]
        dupa= cuv[i+1:]
        cuv=[]
        cuv.extend(inainte)
        if relatii[j-1][1] != 'epsilon':   #daca este epsilon, nu se mai trece in cuvantul creat
            cuv.extend(list(relatii[j-1][1]))   #j-1 pentru ca sare cu 1 peste pozitia dorita
        cuv.extend(dupa)
    return flag, cuv

#----------------------------------------------------------------------------------------------
#Se afiseaza un cuvant din grammar daca acesta este valid

variabile, terminali, relatii, ok = load_config_file(sys.argv[1])
print(f"Variabile: {variabile}")
print(f"Terminali: {terminali}")
print(f"relatii: {relatii}")

if ok == True:
    print("Fisierul contine un grammar!")
    print("Vom afisa un cuvant din grammar, prezentand etapele de formare")
    cuv=[relatii[0][0]]   #am pus in lista variabila de start #intotdeauna variabila de stat va fi prima pusa
    flag = False
    while flag == False:
        flag, cuv = schimbare(flag, cuv)
        if flag == False:          #am pus aceasta conditie pentru a se evita ultima afisare. In absenta ei,
            print("".join(cuv))    #se va afisa de 2 ori varianta finala pentru ca while ul se termina atunci cand nu
                                # mai exista variabile in cuvant, deci dupa ultima modificare, mai trece o data prin
                                #cuvant cautand o variabila si, negasind-o, se opreste(devine True)
else:
    print("nu contine grammar")
