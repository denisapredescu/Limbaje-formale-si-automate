#linia de comanda este:
#python main.py   dfa_config_file(.txt)  input_string

import sys

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
    f = open(file_name)
    for line in f:
        line = line.strip().lower()
        if len(line) > 0 and line[0] != "#":
            l_gen.append(line)
    l_sigma = get_section("sigma", l_gen)      #se apeleaza functia ce returneaza lista de elemente continuta in l_gen
                                                # si care incepe de la cuvantul cheie dat, in cazul de fata "sigma"
    l_states = get_section("states", l_gen)
    l_transitions = get_section("transitions", l_gen)


    l_states_ex=[]      #vreau sa creez liste in lista de stari, listele din interior contin 3 elemente: primul este starea, al doilea
                            # 0/1 in cazul in care starea e initiala, sl treilea 0/1  in functie daca starea e finala
    for state in l_states:   #la inceput starea arata ceva de genul: q1,f  => vreau sa arate asa: [q1, 0, 1]
        tmp=state.split(",")
        tmp_state=[]
        tmp_state.append(tmp[0])
        is_start_state=0
        is_final_state=0
        for entry in tmp[1:]:
            if entry == "f":
                is_final_state = 1
            if entry == "s":
                is_start_state = 1
        tmp_state.append(is_start_state)
        tmp_state.append(is_final_state)
        l_states_ex.append(tmp_state)

    l_states=[]
    for state in l_states_ex:
        l_states.append(state[0])   # iau doar starile fara a preciza tipul lor

    ok = 0

    if len(l_sigma) == 0 or len(l_states) == 0 or len(l_transitions) == 0:   # trebuie ca existe alfabet, stari si tranzitii pentru
        ok=1                                                            # a exista un automat, altfel pastrez un cod de eroare
    else:    #intru doar daca nu s-a gasit deja o eroare
        for trans in l_transitions:
            tmp = trans.split(",")
            if tmp[0] not in l_states or tmp[1] not in l_sigma or tmp[2] not in l_states:     #verific daca sunt corecte tranzitiile
                                                                                        # adica: stare,element_din_alfabet,stare
                ok = 2
    #print(l_states)
    #print(l_sigma)
    #print(l_transitions)


    return l_sigma, l_states_ex, l_transitions, ok

#--------------------------------------------------------------------------------
def dfa_compute(input_string, l_sigma, l_states, l_transitions):

    l_transitions_ex=[]   #vreau sa creez liste in lista de tranzitii, listele din interior contin 3 elemente: primul este starea de plecare,
                          # al doilea este un termen din alfabet si al treilea  este starea in care ajungem in urma tranzitiei respective
    for trans in l_transitions:
        l=trans.split(",")
        l_transitions_ex.append(l)
    l_transitions=l_transitions_ex


    for state in l_states:
        if state[1]==1:    #caut starea de start
            start=state[0]

    x=0
    while x < len(input_string):    #input_string = stringul dat pe care il verific daca apartine limbajului
        for trans in l_transitions:
            if trans[0]==start and trans[1]==input_string[x]:   #daca gasesc o tranzitie care incepe cu starea salvata in "start"
                                                            # si are ca si caracter litera unde am ajuns in  stringul dat, ajungi trec mai
                                                            # departe, adica starea in care ajunge trin acea tranzitie se pune in start si se
                                                            # poate merge mai de parte in stringul dat
                start=trans[2]
                break
        x += 1

    ok=0
    for state in l_states:
        if state[2] == 1 and state[0] == start:   #verific daca starea in care am ajuns in urma stringului este stare finala
            ok=1
    if ok==0:
          print("ultima stare nu e finala")
    return ok


file=sys.argv[1]
input_string=sys.argv[2]

l_sigma, l_states, l_transitions, code=load_config_file(file)
if code==0:
    print("valid config file")
else:
    print("config file", sys.argv[1], "is not valid err:", code)

    # code 0 => valid
    # code 1 => nu exista alfabet, tranzitii sau stari
    # code 2 => cel putin o tranzitie nu este corecta (nu respecta forma ceruta: stare, element din alfabet, stare)

#input_string = "babb" - acceptat

accept_status=dfa_compute(input_string, l_sigma, l_states, l_transitions)

print("string", input_string, "accept status is:", accept_status, end="")     #accept_status: 0/1  - respins/acceptat
if accept_status==1:
    print(" >> accept")
else:
    print(" >> reject")



