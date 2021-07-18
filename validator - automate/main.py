import sys
from os import path


def get_section(name, l_gen):   #functie ce returneaza o lista de elemente (alfabet, stari, tranzitii)-> lista finala
                            # este cuprinsa in lista initiala l_gen si incepe dupa elementul name, terminandu-se la intalnirea
                            # cuvantului cheie "end"
    flag = False
    l_ret = []

    for line in l_gen:
        if line == name + ":":
            flag = True
            continue
        if line == "end":
            flag = False
        if flag == True:
            l_ret.append(line)
    return l_ret

def load_config_file(file_name):
    l_gen = []
    if path.exists(file_name) == True:

        f = open(file_name)
        for line in f:   ##scap de liniile goale si de cele cu comentarii
            line = line.strip().lower()
            if len(line) > 0 and line[0] != "#":
                l_gen.append(line)

        l_sigma = get_section("sigma", l_gen)  #se apeleaza functia ce returneaza lista de elemente continuta in l_gen
                                               #si care incepe de la cuvantul cheie dat, in cazul de fata "sigma"

        l_states = get_section("states", l_gen)
        l_transitions = get_section("transitions", l_gen)

        ok = 0   #trebuie sa vad daca apar erori, codul 0 este cel optim, corect

        if len(l_sigma) == 0 or len(l_states) == 0 or len(l_transitions) == 0:
            ok=1      #lipseste cel putin una dintre cele 3

        else:        #verifica daca tranzitiile sunt corecte doar in cazul in care sectiunile exista
                    #altfel sigur va deveni ok 2 la verificarea din for si nu ne vom mai dea seama
                    #ca eroarea vine de fapt de la lipsa uneia dintre cele 3 sectiuni(ok==1)
            for trans in l_transitions:
                tmp = trans.split(",")
                if tmp[0] not in l_states or tmp[1] not in l_sigma or tmp[2] not in l_states:
                     ok = 2        #cel putin o tranzitie nu respecta regula dorita
                                   #adica: stare, cuvant, stare
        return l_sigma, l_states, l_transitions, ok
    else:
        return 0,0,0,-1


l_sigma, l_states, l_transitions, code = load_config_file(sys.argv[1])
if code == 0:
    print("valid config file")
else:
    print("config file", sys.argv[1], "is not valid err:", code)

    # code 0 => valid
    # code 1 => nu exista alfabet, tranzitii sau stari
    # code 2 => cel putin o tranzitie nu este corecta (nu respecta forma ceruta: stare, element din alfabet, stare)
    # code -1 => nu exista fisierul