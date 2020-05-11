def ca_step(caT1, rule):
    caT2 = list(caT1) # copy ca1 and convert to list for item assignment
    for j in range(1, len(caT2)-1): # leave first and last element unchanged
        caT2[j] = rule[caT1[j-1:j+2]] # slicing on strings is allowed...
    return "".join(caT2) # return as string


def evolution(ca, rule, n = 30, ca_step_func = ca_step):
    for i in range(n+1):
        print(f"#{i:2}|{ca}|", sep="")
        ca = ca_step_func(ca, rule)



ca1 = list(" " * 71)
ca1[34] = "*"
ca1 = "".join(ca1)

headsep = f"\n\n\n{'#'*31} NICE PATTERN {'#'*31}"

def elementary1():
    ca_rule1 = {
    "   ": " ", 
    "*  ": "*",
    " * ": " ", 
    "  *": " ",
    "** ": " ",
    " **": " ",
    "* *": " ",
    "***": " "
    }
    print(headsep)
    evolution(ca1, ca_rule1)
        

def elementary2():
    ca_rule2 = {
    "   ": " ", 
    "*  ": "*",
    " * ": "*", 
    "  *": "*",
    "** ": " ",
    " **": " ",
    "* *": " ",
    "***": " "
    }
    print(headsep)
    evolution(ca1, ca_rule2)

def elementary3():
    ca_rule3 = {
    "   ": "*", 
    "*  ": " ",
    " * ": " ", 
    "  *": " ",
    "** ": " ",
    " **": " ",
    "* *": " ",
    "***": "*"
    }
    print(headsep)
    evolution(ca1, ca_rule3)
        
def elementary4():
    ca_rule4 = {
    "   ": "*", 
    "*  ": "*",
    " * ": " ", 
    "  *": " ",
    "** ": " ",
    " **": " ",
    "* *": "*",
    "***": " "
    }
    print(headsep)
    evolution(ca1, ca_rule4)


# Man kann 8 = 2^3 Regeln aufbauen. Allgemein: (Anzahl an Zuständen) ^ (Feldgröße des Keys)
elementary1()
elementary2()
elementary3()
elementary4()


from time import sleep


def ping_pong(fps = 24):
    ca_pp = " #       o-   # "
    ca_rule_pp = {
        # empty fields
        "   ": " ", 

        # area next to walls when no ball nearby
        "#  ": " ",
        "  #": " ",

        # Walls remain walls in any case
        " # ": "#", 
        " #o": "#",
        " #-": "#",
        "o# ": "#",
        "-# ": "#",

        # ball flying left to right
        "o  ": "o",
        "-o ": "-",
        " -o": " ",
        "  -": " ",

        # ball flying right to left
        "  o": "o",
        " o-": "-",
        "o- ": " ",
        "-  ": " ",

        # bounce left wall
        "# o": "o",
        "#o-": "o",
        "#o ": "-",
        "o  ": "o",
        "#-o": " ",
        "# -": " ",

        #bounce right wall
        "o #": "o",
        "-o#": "o",
        " o#": "-",
        "o  ": "o",
        "o-#": " ",
        "- #": " "
    }

    i = 0
    while 1:
        print(f"#{i:10}|{ca_pp}|", sep="")
        ca_pp = ca_step(ca_pp, ca_rule_pp)
        i += 1
        sleep(1/fps)


ping_pong(fps = 144) # Challenge your fancy gaming display!  
ping_pong()
