#functiile get_section, load_config_file, dfa_compute sunt luate din laboratorul 1
#insa unele au suferit o mica modificare

#trebuie precizata starea aux: ea este o stare auxiliara din care nu se pleaca nicio tranzitie, dar in care pot ajunge
#stari. Ea apare atunci cand automatul nu este complet. In cazul acesta sunt stari care, prin intermediul unei litere
#din alfabel, nu se duce in nicio stare. Asadar, pentru a putea creea dfaul, presupun ca se duce in starea aux
#ajungi cand o sa se reuneasca starile in care se ajunge, nu se va tine cont de starea aux, ea reprezentand de fapt
#multimea vida

import sys

def get_section(name, l_gen):    #din lab 1 - preia din fisier blocul de date dorit si il transforma in lista
                                #blocul este cuprins intre numele dat ca parametru "name" si cuvantul cheie "end"
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

def load_config_file(file_name):   #functie din lab  - sectioneaza cele 3 parti (sigma, states, transitions), creand 3 liste corespunzatoare
    l_gen = []
    f = open(file_name)
    for line in f:
        line = line.strip().lower()
        if len(line) > 0 and line[0] != "#":
            l_gen.append(line)
    l_sigma = get_section("sigma", l_gen)
    l_states = get_section("states", l_gen)
    l_transitions = get_section("transitions", l_gen)


    l_states_ex=[]
    for state in l_states:   #o stare poate fi urmata de "s"-stare de inceput, "f"-stare finala
                                #trebuie sa determinam care este starea initiala si care sunt cele finale
                                #cel mai usor de retinut este ca pentru fiecare stare existenta sa fie transformata
                                #intro lista cu 3 elemente: stare, 0/1(daca este stare initiala), 0/1(daca este stare finala)
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
    for state in l_states_ex:    #se selecteaza doar starile fara detalii cu privire la acestea pentru a fi mai usor de
        l_states.append(state[0])    #verificat mai jos

    ok = 0   #se cauta daca configurarea din fisier este valida. In functie de valoarea lui "ok", receptam problema
             #daca ok == 0  inseamna ca este valida

    if len(l_sigma) == 0 or len(l_states) == 0 or len(l_transitions) == 0:      #verific daca cele 3 sectiuni exista
        ok=1
     #daca nu am eroare, verific in continuare
    l_trans=[]
    for trans in l_transitions:
        tmp = trans.split(",")
        if ok==0:      #daca am toate sectiunile, verific in continuare
                        #am preferat insa sa nu pun else la "if len(l_sigma) == 0 or len(l_states) == 0 or len(l_transitions) == 0:"
                        #deoarece vreau ca la final sa am si sectiunea "Transitions" impartita, ca in cazul in care configurarea
                        #este valida, sa pot lucra in continuare cu ea.
            if tmp[0] not in l_states or tmp[1] not in l_sigma or tmp[2] not in l_states:
                ok = 2              #verific daca starile din tranzitii sunt cele mentionate in sectiunea "States"(daca tranzitiile sunt valide)
        l_trans.append(tmp)

    return l_sigma, l_states_ex, l_trans, ok

#-----------------------------------------------------------------------------
def dfa_compute(input_string, l_sigma, l_states, l_transitions):
                #configurarea este valida si verific daca un input dat este acceptat sau respins
                #sectiunea transitions este impartita si poate fi parcursa cu usurinta
    for state in l_states:
        if state[1]==1:
            start=state[0]
    x=0

    while x < len(input_string):
        for trans in l_transitions:
            if trans[0]==start and trans[1]==input_string[x]:
                start=trans[2]
                break
            if start == "aux":   #din aux nu pleaca nicio tranzitie si nu este o stare finala
                return 0
        x += 1
    ok=0
    for state in l_states:
        if state[2] == 1 and state[0] == start:
            ok=1
    if ok==0:
          print("ultima stare nu e finala")
    return ok


def nfa(tranzitii):
         #stim ca intr-un nfa, o stare primind o litera, poate merge in mai multe stari
         #deci se modifica tranzitiile, acum va fi de forma stare-litera-lista_de_stari in care merge
   # new_states=[stari[0]]
    new_transitions=[]

    while len(tranzitii)!=0:
        i=tranzitii[0]     #iau prima tranzitie si verific daca mai exista alte tranzitii care prin
                          #plecand din aceeasi stare si prin intermediul aceleasi litere, se ajunge in alta stare
        aux = []
        stare_noua = []

        for j in tranzitii:
            if i[0]==j[0] and i[1]==j[1]:
                if j[2] not in stare_noua and j[2]!="aux":   #nu vrem sa il punem pe aux in starile in care se ajunge
                                                            #in cazul in care exista si alte stari pe langa
                    stare_noua.append(j[2])
            else:
                aux.append(j)    #pastrez in tranzitii doar pe cele la care nu am ajuns inca
                                    #pe cele care nu pleaca din aceeasi stare si/sau nu folosesc aceeasi litera

        tranzitii=aux

        if len(stare_noua)==0:
            stare_noua=["aux"]
        new_transitions.append([i[0],i[1], stare_noua])    #introduc in noua lista de tranzitii pe cea creata in care
                                                #pe a treia pozitie nu mai am o stare, ci o lista de stari

    return new_transitions

def completare(l_transitions):

    for sigma in l_sigma:
        for st in l_states:
            ok = False
            for t in l_transitions:
                if t[0]==st[0] and  t[1]==sigma:
                    ok=True
            if ok == False:
                l_transitions.append([st[0],sigma,"aux"])   #aux reprezinta multimea vida, nu este o stare finala
                                                            # si nu pleaca nicio trnzitie din ea
    return  l_transitions

def drum(start, sigma, new_states, new_transitions):
    #start este starea noua din DFA
    f=0
    for s in start:     #exista o singura stare de inceput(care este de la inceput pusa in new_states),insa pot fi mai multe stari finale
        for val in l_states:
            if s[0] == val[0]:
                if val[2] == 1:
                    f = 1
    if [start, 0, f] not in new_states:  #avand in vedere ca sunt mai multe litere in alfabet, o sa intre de mai multe ori
                                            #cu aceeasi stare de plecare
        new_states.append([start, 0, f])

    temp=[]

    for s in start:     #creez lista se stari in care ajunge
        for trans in transitions:
            if s==trans[0] and sigma==trans[1]:
                for l in trans[2]:
                    if l not in temp and l!="aux":
                        temp.append(l)

    if len(temp)==0:
        temp=["aux"]
    new_transitions.append([start, sigma, temp])   #o introduc in new_transitions

    return new_states, new_transitions

#listele de stari au fost sortate inainte de a fi lipite, pentru a fi la fel in toate locurile in care se vor afla
#de exemplu sa nu fie '23' si '32', ci in ambele locuri sa fie '23'
def lipire_stari(states):
    for l in states:
        l[0]="".join(sorted(l[0]))
    return states

def lipire_trans(transitions):
    for l in transitions:
        l[0]="".join(sorted(l[0]))
        l[2]="".join(sorted(l[2]))
    return transitions

def nfa_dfa(states, transitions):
    new_states=[]    #la convertire, se modifica atat lista de stari, cat si cea de tranzitii
    new_transitions=[]

    for st in states:   #caut starea de start
        if st[1]==1:
            start=st[0]
            new_states.append(st)

    for trans in transitions:     #vad unde pot ajunge plecand din start
        if trans[0]==start:
            new_transitions.append(trans)

    i=0
    #plecand de la starile in care pot ajunge din starea initiala,
    #pas cu pas adaug la tranzitii pe acelea la care se poate ajunge
    #(si la starile folosite), astfel creandu-se dfa ul echivalent
    while i<len(new_transitions):
        if set(new_transitions[i][2])!=set(new_transitions[i][0]):      #daca starea de plecare e diferita de starea in care ajung
                                                                #inseamna ca pot ajunge si in alta stare, cautand dupa aceea
                                                                #tranzitiile care in cel cu acea stare
            ok=True
            for s in new_states:
                if set(new_transitions[i][2]) == set(s[0]):   #verific daca nu cumva am mai ajuns candva in acea stare
                                                     #daca am mai ajuns acolo, inseamna ca s-a salvat starea inn lista new_states
                    ok=False
            if new_transitions[i][2]==['aux']:
                ok=False
            if ok==True:
                start=new_transitions[i][2]        #daca este o stare noua gasita, caut tranzitiile care incep cu ea

                for sigma in l_sigma:
                    new_states, new_transitions=drum(start,sigma,new_states, new_transitions)
        i+=1

    new_states=lipire_stari(new_states)   #la final starile trebuie sa fie string, nu lista
    new_transitions=lipire_trans(new_transitions)

    return new_states, new_transitions

def dfa_file(filename):
    f = open(filename, "w")  # acum vreau sa scriu in fisier dfa-ul convertit din nfa
    f.write("Sigma:")  # pun alfabetul in fisier
    f.write("\n")
    for s in l_sigma:
        f.write(s)
        f.write("\n")

    f.write("States:")  # pun starile in fisier
    f.write("\n")
    for s in states:
        f.write(s[0])
        if s[1] == 1:
            f.write(",s")  # specific si care este starea initiala si cea finala
        if s[2] == 1:
            f.write(",f")
        f.write("\n")

    f.write("Transitions:")  # pun tranzitiile in fisier
    f.write("\n")
    for t in transitions:
        f.write(t[0])
        f.write("," + t[1])
        f.write("," + t[2])
        f.write("\n")
    f.close()


############################################################################################
#main
l_sigma, l_states, l_transitions, code=load_config_file(sys.argv[1])    #se genereaza NFA-ul si se verifica daca este valid
if code==0:
    print("valid config file")
else:
    print("config file", sys.argv[1], "is not valid err:", code)

    # code == 0: configurare valida
    # code == 1: nu exista una dintre cele 3 secvente
    # code == 2: cel putin o tranzitie nu este corecta


if code==0:   #se continua transformarea doar in cazul in care este valid
                #alfabetul ramane acelasi

    l_transitions=completare(l_transitions)  #daca dintr-o anumita stare nu sa pleaca folosindu-se de toate literele din alfabet.
                        # => in acest caz completez singura tranzitiile, punand pentru acele literele care nu sunt
                        #folositie ca merg intr-o stare nefolositoare, ndenumita "aux", ea nu va fi niciodata printre
                        #starile de plecare si nu se afla nici in lista starilor. Scopul ei este doar de a completa
                        #acele tranzitii care nu exista initial. Putem spune ca aux este multimea vida:
                        #aux reunit cu stari = acele stari. daca len(stari)=0 =>stari = aux

    transitions = nfa(l_transitions)   #am creat listele specifice NFA-ului pentru a putea mai apoi sa
                                                #le convertesc la DFA


    states, transitions = nfa_dfa(l_states, transitions)  #transformare din NFA in DFA
    #print(transitions)
    dfa_file("dfa.txt")


    input_string = "1001111111111111111001"
    accept_status = dfa_compute(input_string, l_sigma, states, transitions)
    print("string", input_string, "accept status is:", accept_status)
