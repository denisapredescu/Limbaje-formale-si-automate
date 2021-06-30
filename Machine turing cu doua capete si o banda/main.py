import sys

def get_section(name, l_gen):  #creez listele specifice sectiunilor

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

def load_config_file(file_name):    #functie care verifica daca este corecta configurarea din fisier
    l_gen = []
    f = open(file_name)
    for line in f:
        line = line.strip().lower()
        if len(line) > 0:
            l_gen.append(line)
    l_states = get_section("states", l_gen)  #se creeaza listele
    l_input = get_section("input alphabet", l_gen)
    l_tape = get_section("tape alphabet", l_gen)

    l_transitions = get_section("transitions", l_gen)

    l_states_ex=[]

    for state in l_states:
        tmp=state.split()
        tmp_state=[]
        tmp_state.append(tmp[0])
        is_start_state=0
        is_state=0
        for entry in tmp[1:]:  #se retine care stare este cea de start, cea de reject si cea de accept
            if entry == "a":
                is_state = 1
            if entry == "r":
                is_state = 2
            if entry == "s":
                is_start_state = 1

        tmp_state.append(is_start_state)
        tmp_state.append(is_state)
        l_states_ex.append(tmp_state)

    l_states=[]
    for state in l_states_ex:
        l_states.append(state[0])   # iau doar starile fara a preciza tipul lor

    _ok = 0  #verificarea configurarii

    if len(l_input) == 0 or len(l_tape) == 0 or len(l_states) == 0 or len(l_transitions) == 0:
        _ok = 1    #cod pentru "nu exista cel putin una dintre sectiuni"
    else:
        for trans in l_transitions:
            tmp = trans.split()
            if tmp[0] not in l_states or tmp[1] not in l_states or tmp[2] not in l_tape or tmp[3] not in l_tape:  #verific daca sunt corecte tranzitiile
                _ok = 2  #cod pt nu este corecta tranzitia
            else:
                if tmp[6] != "r" and tmp[6] != "l" and tmp[6] != "p" and tmp[7] != "r" and tmp[7] != "l" and tmp[7] != "p":
                    _ok = 3  #cod pentru invalid left/right/pe loc

    return l_states_ex, l_input, l_tape,  l_transitions, _ok

#--------------------------------------------------------------------------------

def compute(input_string, l_input, l_states, l_transitions):

    for v in input_string[:-1]:   #verific daca inputul dat este in lista de caractere destinate inputului
        if v not in l_input:
            return -1

    l_transitions_ex=[]

    for trans in l_transitions:
        l=trans.split()
        l_transitions_ex.append(l)
    l_transitions=l_transitions_ex     #creezi lista de liste specifica tranzitiilor

    c1=0  #capat 1 (pozitie ain input a capatului)
    c2=0  #capat 2

    for state in l_states:
        if state[1]==1:
            start=state[0]    #starea de inceput

    #in cazul configurarii noastre, c1=c2=0

    string_nou=[x for x in input_string]  #fac lista din stringul input pentru al putea parcurge cu usurinta

    #procesul se repeta pana cand se ajunge in starea de accept sau de reject
    while start!="q_reject" and start!="q_accept":
        for trans in l_transitions:
            if trans[0]==start and trans[2]==string_nou[c1] and trans[3]==string_nou[c2]:
                start=trans[1]     #schimb starea de start (pun starea unde am ajuns si de unde o sa plec la urmatoarea tranzitie)

                if trans[4]!="e":    #schimb valoarea din input in cazul in care acea valoare e diferita de "e";
                                        # "e" zice ca nu se schimba valoarea
                    string_nou[c1]=trans[4]   #pentru capat1
                if trans[5]!="e":
                    string_nou[c2]=trans[5]   #pentru capat2

                #l-left
                #r-right
                #p-pe loc
                if trans[6]=="r":   #aici vad daca trebuie sa ma mut la stanga sau la dreapta sau sa raman pe loc
                    c1+=1
                elif trans[6]=="l":
                    if c1!=0:
                        c1-=1

                if trans[7]=="r":
                    c2+=1
                elif trans[7]=="l":
                    if c2!=0:
                        c2-=1
                break

    #verific daca starea la care am ajuns este de reject sau de accept
    ok=0
    for state in l_states:
        if state[2] == 1 and state[0] == start:
            ok=1

    return ok, "".join(string_nou)

#------------------------------------------------MAIN----------------------------------------------------------------

l_states, l_input, l_tape, l_transitions, code=load_config_file(sys.argv[1])
if code==0:
    print("valid config file")

    #EXERCITIUL 2
    #simulatorul va simula daca un input este corect:
    #in momentul de fata ma gandesc ca un simulator bun pentru un turing machine cu 2 capete este sa vedem
    #daca numarul de "0" este egal cu numarul de "1" L={0*1*|len(0)=len(1)>=1}
    #input_string = "000111_"


    # EXERCITIUL 3
    # EXEMPLE de cazuri verificate
    # input_string = "001#01_"  #nu este prefix
    # input_string = "001#0_"  #este prefix
    # input_string = "001#_"  #nu este prefix (pentru ca trebuie sa existe cel putin un caracter/numar ca sa fie prefix
    # pentru un cuvant)
    # input_string = "001#001_"  #nu este prefix (este exact cuvantul dat, ca sa fie prefix trebuia sa fie doar
    # prima parte din cuvant)
    # input_string = "#10_"  #nu exista "w"-cuvant
    # input_string = "101#10_"  # este prefix

    # EXERCITIUL 3
    # input_string = "a+_"  # nu se poate; accept status 0
    # input_string = "+a_"  # nu se poate; accept status 0
    input_string = "a+aaaaaa_"  # accept status 1

    print("stringul", input_string, end=" ")
    accept_status, input_string =compute(input_string, l_input, l_states, l_transitions)

    print("devine ", input_string, " accept status is: ",
          accept_status)  # accept_status: 0/1  - respins/acceptat

else:
    print("config file", sys.argv[1], "is not valid err:", code)





