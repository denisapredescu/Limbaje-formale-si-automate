#aceasta este problema pe care ne-ati dat-o sa o facem la laborator cu Machine Turing.
#Functioneaza: verifica configurarea fisierului .txt si transforma un input dat
#din pacate nu este comentat codul. 
import sys

def get_section(name, l_gen):

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
        if len(line) > 0:
            l_gen.append(line)
    l_states = get_section("states", l_gen)
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
        is_reject_state=0
        for entry in tmp[1:]:
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

    trans_ok = 0
    #print( l_states)
    #print()

    for trans in l_transitions:
        tmp = trans.split()
        if tmp[0] not in l_states or tmp[1] not in l_states or tmp[2] not in l_tape:  #verific daca sunt corecte tranzitiile
            trans_ok = 2  #cod pt nu este corecta tranzitia
        else:
            if tmp[4] != "r" and tmp[4] != "l":
                trans_ok = 3  #cod pentru invalid left/right
    #print(l_states)
    #print(l_sigma)
    #print(l_transitions)

    if len(l_input) == 0 or len(l_tape)==0 or len(l_states) == 0 or len(l_transitions) == 0:
        trans_ok=1

    return l_states_ex, l_input, l_tape,  l_transitions, trans_ok

#--------------------------------------------------------------------------------
def dfa_compute(input_string, l_input, l_states, l_transitions):

    #print(l_input, input_string)
    for v in input_string[:-1]:
        if v not in l_input:
            return -1
    poz = 0
    l_transitions_ex=[]

    for trans in l_transitions:
        l=trans.split()
        l_transitions_ex.append(l)
    l_transitions=l_transitions_ex


    for state in l_states:
        if state[1]==1:    #caut starea de start
            start=state[0]

    string_nou=[x for x in input_string]

    while poz < len(string_nou):
        for trans in l_transitions:
            if trans[0]==start and trans[2]==string_nou[poz]:
                start=trans[1]
                if trans[3]!="e":
                    string_nou[poz]=trans[3]

                if trans[4]=="r":
                    poz+=1
                elif trans[4]=="l":
                    if poz!=0:
                        poz-=1
                break


    ok=0
    for state in l_states:
        if state[2] == 1 and state[0] == start:
            ok=1
    if ok==0:
          print("stringul nu este acceptat")
    return ok, "".join(string_nou)


l_states, l_input, l_tape, l_transitions, code=load_config_file(sys.argv[1])
if code==0:
    print("valid config file")

    input_string = "0000_"

    accept_status, input_string = dfa_compute(input_string, l_input, l_states, l_transitions)

    print("string", "devine", input_string, "accept status is:",
          accept_status)  # accept_status: 0/1  - respins/acceptat
else:
    print("config file", sys.argv[1], "is not valid err:", code)





