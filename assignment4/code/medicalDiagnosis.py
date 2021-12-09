#from bnetbase_solved import *
from bnetbase import *

bmi = Variable("BMI", ['~18.5', '~24.0', '~28.0', '<18.5'])
F1 = Factor("P(bmi)", [bmi])
F1.add_values(
    [['~18.5', 0.373],
     ['~24.0', 0.406],
     ['~28.0', 0.204],
     ['<18.5', 0.017]])

co = Variable("Central_Obesity", ['YES', 'NO'])
F2 = Factor("P(co|bmi)", [co, bmi])
F2.add_values(
    [['YES', '~18.5', 0.411],
     ['YES', '~24.0', 0.774],
     ['YES', '~28.0', 0.972],
     ['YES', '<18.5', 0.012],
     ['NO', '~18.5', 0.589],
     ['NO', '~24.0', 0.226],
     ['NO', '~28.0', 0.028],
     ['NO', '<18.5', 0.988]])

ht = Variable("Hypertension", ['YES', 'NO'])
F3 = Factor("P(ht|co,bmi)", [ht,co,bmi])
F3.add_values(
    [['YES', 'YES', '~18.5', 0.373],
     ['YES', 'YES', '~24.0', 0.452],
     ['YES', 'YES', '~28.0', 0.845],
     ['YES', 'YES', '<18.5', 0.126],
     ['YES', 'NO', '~18.5', 0.347],
     ['YES', 'NO', '~24.0', 0.409],
     ['YES', 'NO', '~28.0', 0.731],
     ['YES', 'NO', '<18.5', 0.045],
     ['NO', 'YES', '~18.5', 0.627],
     ['NO', 'YES', '~24.0', 0.548],
     ['NO', 'YES', '~28.0', 0.155],
     ['NO', 'YES', '<18.5', 0.874],
     ['NO', 'NO', '~18.5', 0.653],
     ['NO', 'NO', '~24.0', 0.591],
     ['NO', 'NO', '~28.0', 0.269],
     ['NO', 'NO', '<18.5', 0.955]])

hl = Variable("Hyperlipidemia", ['YES', 'NO'])
F4 = Factor("P(hl|co,bmi)", [hl,co,bmi])
F4.add_values(
    [['YES', 'YES', '~18.5', 0.248],
     ['YES', 'YES', '~24.0', 0.481],
     ['YES', 'YES', '~28.0', 0.655],
     ['YES', 'YES', '<18.5', 0.152],
     ['YES', 'NO', '~18.5', 0.193],
     ['YES', 'NO', '~24.0', 0.426],
     ['YES', 'NO', '~28.0', 0.534],
     ['YES', 'NO', '<18.5', 0.087],
     ['NO', 'YES', '~18.5', 0.752],
     ['NO', 'YES', '~24.0', 0.519],
     ['NO', 'YES', '~28.0', 0.345],
     ['NO', 'YES', '<18.5', 0.848],
     ['NO', 'NO', '~18.5', 0.807],
     ['NO', 'NO', '~24.0', 0.574],
     ['NO', 'NO', '~28.0', 0.466],
     ['NO', 'NO', '<18.5', 0.913]])

vg = Variable("Vegetables", ['<400g/d', '400-500g/d', '>500g/d'])
F5 = Factor("P(vg|hl)", [vg, hl])
F5.add_values(
    [['<400g/d', 'YES', 0.579],
     ['<400g/d', 'NO', 0.283],
     ['400-500g/d', 'YES', 0.284],
     ['400-500g/d', 'NO', 0.324],
     ['>500g/d', 'YES', 0.137],
     ['>500g/d', 'NO', 0.393]])

gd = Variable("Gender", ['Male', 'Female'])
F6 = Factor("P(gd|hl)", [gd, hl])
F6.add_values(
    [['Male', 'YES', 0.571],
     ['Male', 'NO', 0.494],
     ['Female', 'YES', 0.429],
     ['Female', 'NO', 0.506]])

rg = Variable("Region", ['Countryside', 'City'])
F7 = Factor("P(rg|ht,hl)", [rg,ht,hl])
F7.add_values(
    [['Countryside', 'YES', 'YES', 0.416],
     ['Countryside', 'YES', 'NO', 0.371],
     ['Countryside', 'NO', 'YES', 0.598],
     ['Countryside', 'NO', 'NO', 0.543],
     ['City', 'YES', 'YES', 0.584],
     ['City', 'YES', 'NO', 0.629],
     ['City', 'NO', 'YES', 0.402],
     ['City', 'NO', 'NO', 0.457]])

db = Variable("Diabetes", ['YES', 'NO'])
F8 = Factor("P(db|ht,hl)", [db,ht,hl])
F8.add_values(
    [['YES', 'YES', 'YES', 0.693],
     ['YES', 'YES', 'NO', 0.596],
     ['YES', 'NO', 'YES', 0.587],
     ['YES', 'NO', 'NO', 0.221],
     ['NO', 'YES', 'YES', 0.307],
     ['NO', 'YES', 'NO', 0.404],
     ['NO', 'NO', 'YES', 0.413],
     ['NO', 'NO', 'NO', 0.779]])

ag = Variable("Age", ['~60', '~40', '<40'])
F9 = Factor("P(ag|ht,hl)", [ag,ht,hl])
F9.add_values(
    [['~60', 'YES', 'YES', 0.412],
     ['~60', 'YES', 'NO', 0.395],
     ['~60', 'NO', 'YES', 0.375],
     ['~60', 'NO', 'NO', 0.221],
     ['~40', 'YES', 'YES', 0.367],
     ['~40', 'YES', 'NO', 0.334],
     ['~40', 'NO', 'YES', 0.341],
     ['~40', 'NO', 'NO', 0.314],
     ['<40', 'YES', 'YES', 0.221],
     ['<40', 'YES', 'NO', 0.271],
     ['<40', 'NO', 'YES', 0.284],
     ['<40', 'NO', 'NO', 0.465]])

ac = Variable("Activity", ['Insufficient', 'Normal', 'Sufficient'])
F10 = Factor("P(ac|gd,hl,ag)", [ac,gd,hl,ag])
F10.add_values(
    [['Insufficient', 'Male', 'YES', '~60', 0.461],
     ['Insufficient', 'Male', 'YES', '~40', 0.413],
     ['Insufficient', 'Male', 'YES', '<40', 0.386],
     ['Insufficient', 'Male', 'NO', '~60', 0.393],
     ['Insufficient', 'Male', 'NO', '~40', 0.381],
     ['Insufficient', 'Male', 'NO', '<40', 0.291],
     ['Insufficient', 'Female', 'YES', '~60', 0.482],
     ['Insufficient', 'Female', 'YES', '~40', 0.431],
     ['Insufficient', 'Female', 'YES', '<40', 0.416],
     ['Insufficient', 'Female', 'NO', '~60', 0.412],
     ['Insufficient', 'Female', 'NO', '~40', 0.413],
     ['Insufficient', 'Female', 'NO', '<40', 0.312],
     ['Normal', 'Male', 'YES', '~60', 0.294],
     ['Normal', 'Male', 'YES', '~40', 0.335],
     ['Normal', 'Male', 'YES', '<40', 0.360],
     ['Normal', 'Male', 'NO', '~60', 0.298],
     ['Normal', 'Male', 'NO', '~40', 0.336],
     ['Normal', 'Male', 'NO', '<40', 0.371],
     ['Normal', 'Female', 'YES', '~60', 0.295],
     ['Normal', 'Female', 'YES', '~40', 0.331],
     ['Normal', 'Female', 'YES', '<40', 0.363],
     ['Normal', 'Female', 'NO', '~60', 0.299],
     ['Normal', 'Female', 'NO', '~40', 0.338],
     ['Normal', 'Female', 'NO', '<40', 0.378],
     ['Sufficient', 'Male', 'YES', '~60', 0.245],
     ['Sufficient', 'Male', 'YES', '~40', 0.252],
     ['Sufficient', 'Male', 'YES', '<40', 0.254],
     ['Sufficient', 'Male', 'NO', '~60', 0.309],
     ['Sufficient', 'Male', 'NO', '~40', 0.283],
     ['Sufficient', 'Male', 'NO', '<40', 0.338],
     ['Sufficient', 'Female', 'YES', '~60', 0.223],
     ['Sufficient', 'Female', 'YES', '~40', 0.238],
     ['Sufficient', 'Female', 'YES', '<40', 0.221],
     ['Sufficient', 'Female', 'NO', '~60', 0.289],
     ['Sufficient', 'Female', 'NO', '~40', 0.249],
     ['Sufficient', 'Female', 'NO', '<40', 0.310]])

medical = BN('Medical Diagnosis',
         [bmi, co, ht, hl, vg, gd, rg, db, ag, ac],
         [F1, F2, F3, F4, F5, F6, F7, F8, F9, F10])

def printQ2a():
    print("Show: Given HL, VG and BMI are independent, but without HL, VG and BMI are dependent\n\n")

    print("******************** Show P(VG | BMI) != P(VG) * P(BMI) and  Show P(BMI | VG) != P(VG) * P(BMI) ********************")

    for i in vg.domain():
        for j in bmi.domain():
            vg.set_evidence(i)
            bmi.set_evidence(j)

            test1 = VE(medical, vg, [bmi])
            test1_other_way = VE(medical, bmi, [vg])
            test2 = VE(medical, vg, [])
            test3 = VE(medical, bmi, [])

            combined = [x * y for x, y in zip(test2, test3)]

            #print(test1, combined)

            if test1 != combined and test1_other_way != combined:
                print("Correct!")
            else:
                print("INCORRECT")


    print("********************************* Show P(VG | HL, BMI) = P(VG| HL) *********************************")
    for i in vg.domain():
        for j in hl.domain():
            for k in bmi.domain():
                vg.set_evidence(i)
                hl.set_evidence(j)
                bmi.set_evidence(k)

                test1 = VE(medical, vg, [hl, bmi])
                test2 = VE(medical, vg, [hl])

                #print(test1, test2)

                if abs(test1[0] - test2[0]) < 0.0001 and abs(test1[1] - test2[1]) < 0.0001 and abs(test1[2] - test2[2]) < 0.0001:
                    print("Correct!")
                else:
                    print("INCORRECT")
    
    print("********************************* Show P(BMI | HL, VG) = P(BMI| HL) *********************************")
    for i in bmi.domain():
        for j in hl.domain():
            for k in vg.domain():
                bmi.set_evidence(i)
                hl.set_evidence(j)
                vg.set_evidence(k)

                test1 = VE(medical, bmi, [hl, vg])
                test2 = VE(medical, bmi, [hl])

                #print(test1, test2)

                if abs(test1[0] - test2[0]) < 0.0001 and abs(test1[1] - test2[1]) < 0.0001 and abs(test1[2] - test2[2]) < 0.0001 and abs(test1[3] - test2[3]) < 0.0001:
                    print("Correct!")
                else:
                    print("INCORRECT")

def printQ2b():
    ######################## Part b) ########################
    # HT and HL independent given CO and BMI, but become dependent given AGE
    
    print("Show: Given CO and BMI, HT and HL are independent, but given AG, CO, and BMI HT and HL become dependent\n\n")

    print("********************************* Show P(HT | CO, BMI) = P(HT| HL, CO, BMI) *********************************")
    for i in ht.domain():
        for j in co.domain():
            for k in bmi.domain():
                ht.set_evidence(i)
                co.set_evidence(j)
                bmi.set_evidence(k)
                Q2a = VE(medical, hl, [co, bmi])
                Q2b = VE(medical, hl, [ht, co, bmi])

                for num in [0, 1]:
                    factor1 = Q2a[num]
                    factor2 = Q2b[num]

                    if abs(factor1 - factor2) < 0.000001:
                        print("Correct!")
                    else:
                        print("INCORRECT")

                    #print("Without HL: {}, With HL: {}".format(factor1, factor2))

    print("\n********************************* Show P(HL | CO, BMI) = P(HL| HT, CO, BMI) *********************************")
    for i in hl.domain():
        for j in co.domain():
            for k in bmi.domain():
                hl.set_evidence(i)
                co.set_evidence(j)
                bmi.set_evidence(k)
                Q2a = VE(medical, ht, [co, bmi])
                Q2b = VE(medical, ht, [hl, co, bmi])

                for num in [0, 1]:
                    factor1 = Q2a[num]
                    factor2 = Q2b[num]

                    if abs(factor1 - factor2) < 0.000001:
                        print("Correct!")
                    else:
                        print("INCORRECT")

                    #print("Without HT: {}, With HT: {}".format(factor1, factor2))
    
    print("\n*********************************Show P(HT | CO, BMI, AG) != P(HT| HL, CO, BMI, AG) *********************************")
    for i in ht.domain():
        for j in co.domain():
            for k in bmi.domain():
                for l in ag.domain():
                    ht.set_evidence(i)
                    co.set_evidence(j)
                    bmi.set_evidence(k)
                    ag.set_evidence(l)
                    Q2a = VE(medical, hl, [co, bmi, ag])
                    Q2b = VE(medical, hl, [ht, co, bmi, ag])

                    for num in [0, 1]:
                        factor1 = Q2a[num]
                        factor2 = Q2b[num]

                        if factor1 != factor2:
                            print("Correct!")
                        else:
                            print("INCORRECT")

                        #print("Without HL: {}, With HL: {}".format(factor1, factor2))

    print("\n********************************* Show P(HL | CO, BMI, AG) != P(HL| HT, CO, BMI, AG) *********************************")
    for i in hl.domain():
        for j in co.domain():
            for k in bmi.domain():
                for l in ag.domain():
                    hl.set_evidence(i)
                    co.set_evidence(j)
                    bmi.set_evidence(k)
                    ag.set_evidence(l)
                    Q2a = VE(medical, ht, [co, bmi, ag])
                    Q2b = VE(medical, ht, [hl, co, bmi, ag])

                    for num in [0, 1]:
                        factor1 = Q2a[num]
                        factor2 = Q2b[num]

                        if factor1 != factor2:
                            print("Correct!")
                        else:
                            print("INCORRECT")

                        #print("Without HT: {}, With HT: {}".format(factor1, factor2))
    
    return

def printQ2c():
    ######################## Part c) ########################
    # P(AC) increases given accumulated evidence items AGE, DB, RE, GD, HT
    print("Find: Sequence of accumulated evidence items wuch that each additional evidence item increases the probability that V = d for a var V and a value d in V.domain()")
    print("V = AC | V1 = HT, V2 = GD, V3 = RG, V4 = DB, V5 = AG\n\n")
    vars = [bmi, co, vg, hl, ht, gd, rg, db, ag, ac]
    V0 = vars[9]
    V5 = vars[8]
    V4 = vars[7]
    V3 = vars[6]
    V2 = vars[5]
    V1 = vars[4]

    values_of_evidence = []
    probs = []
    increasing = True

    #for i in V0.domain():
    for j in V1.domain():
        for k in V2.domain():
            for l in V3.domain():
                for m in V4.domain():
                    for n in V5.domain():
                        V1.set_evidence(j)
                        V2.set_evidence(k)
                        V3.set_evidence(l)
                        V4.set_evidence(m)
                        V5.set_evidence(n)

                        prob_one = VE(medical, V0, [V5])
                        prob_two = VE(medical, V0, [V5, V4])
                        prob_three = VE(medical, V0, [V5, V4, V3])
                        prob_four = VE(medical, V0, [V5, V4, V3, V2])
                        prob_five = VE(medical, V0, [V5, V4, V3, V2, V1])

                        for item_one, item_two, item_three, item_four, item_five in zip(prob_one, prob_two, prob_three, prob_four, prob_five):
                            if item_five >= item_four and item_four >= item_three and item_three >= item_two and item_two >= item_one:
                                temp_tuple = (j, k, l, m, n)
                                values_of_evidence.append(temp_tuple)

                                prob_tuple = (item_one, item_two, item_three, item_four, item_five)
                                probs.append(prob_tuple)

    for assignment, prob in zip(values_of_evidence, probs):
        print("Assignment: {}".format(assignment))
        print("Probabilities: {}\n".format(prob))
    
    return

def new_printQ2c():
    ######################## Part c) ########################
    # P(AC) increases given accumulated evidence items AGE, DB, RE, GD, HT
    print("Find: Sequence of accumulated evidence items wuch that each additional evidence item increases the probability that V = d for a var V and a value d in V.domain()")
    print("V0 = BMI d0 = ~28 | V1 = CO d1 = YES, V2 = HT d2 = YES, V3 = HL d3 = YES, V4 = VG d4 = <400g/d, V5 = GD d5 = Male\n")
    vars = [bmi, co, vg, hl, ht, gd, rg, db, ag, ac]
    V0 = vars[0] # bmi
    V5 = vars[5] # gd
    V4 = vars[2] # vg
    V3 = vars[3] # hl
    V2 = vars[4] #ht
    V1 = vars[1] #co

    V1.set_evidence('YES')
    V2.set_evidence('YES')
    V3.set_evidence('YES')
    V4.set_evidence('<400g/d')
    V5.set_evidence('Male')

    prob_one = VE(medical, V0, [V5])
    prob_two = VE(medical, V0, [V5, V4])
    prob_three = VE(medical, V0, [V5, V4, V3])
    prob_four = VE(medical, V0, [V5, V4, V3, V2])
    prob_five = VE(medical, V0, [V5, V4, V3, V2, V1])

    print("Probability given V5: {}".format(prob_one))
    print("Probability given V5 and V4: {}".format(prob_two))
    print("Probability given V5 and V4 and V3: {}".format(prob_three))
    print("Probability given V5 and V4 and V3 and V2: {}".format(prob_four))
    print("Probability given V5 and V4 and V3 and V2 and V1: {}".format(prob_five))
    
    if prob_one[2] < prob_two[2]:
        if prob_two[2] < prob_three[2]:
            if prob_three[2] < prob_four[2]:
                if prob_four[2] < prob_five[2]:
                    print("Question 2c correct!")
                else:
                    print("INCORRECT")
            else:
                print("INCORRECT")
        else:
            print("INCORRECT")
    else:
        print("INCORRECT")
    return



def printQ2d():
    ######################## Part d) ########################
    # P(AC) decreases given accumulated evidence items AGE, DB, RE, GD, HT
    print("Find: Sequence of accumulated evidence items wuch that each additional evidence item increases the probability that V = d for a var V and a value d in V.domain()")
    print("V = AC | V1 = HT, V2 = GD, V3 = RG, V4 = DB, V5 = AG\n\n")
    vars = [bmi, co, vg, hl, ht, gd, rg, db, ag, ac]
    V0 = vars[9]
    V5 = vars[8]
    V4 = vars[7]
    V3 = vars[6]
    V2 = vars[5]
    V1 = vars[4]

    values_of_evidence = []
    probs = []
    increasing = True

    #for i in V0.domain():
    for j in V1.domain():
        for k in V2.domain():
            for l in V3.domain():
                for m in V4.domain():
                    for n in V5.domain():
                        V1.set_evidence(j)
                        V2.set_evidence(k)
                        V3.set_evidence(l)
                        V4.set_evidence(m)
                        V5.set_evidence(n)

                        prob_one = VE(medical, V0, [V5])
                        prob_two = VE(medical, V0, [V5, V4])
                        prob_three = VE(medical, V0, [V5, V4, V3])
                        prob_four = VE(medical, V0, [V5, V4, V3, V2])
                        prob_five = VE(medical, V0, [V5, V4, V3, V2, V1])

                        for item_one, item_two, item_three, item_four, item_five in zip(prob_one, prob_two, prob_three, prob_four, prob_five):
                            if item_five <= item_four and item_four <= item_three and item_three <= item_two and item_two <= item_one:
                                temp_tuple = (j, k, l, m, n)
                                values_of_evidence.append(temp_tuple)

                                prob_tuple = (item_one, item_two, item_three, item_four, item_five)
                                probs.append(prob_tuple)

    for assignment, prob in zip(values_of_evidence, probs):
        print("Assignment: {}".format(assignment))
        print("Probabilities: {}\n".format(prob))
    
    return

def new_printQ2d():
    ######################## Part d) ########################
    # P(AC) increases given accumulated evidence items AGE, DB, RE, GD, HT
    print("Find: Sequence of accumulated evidence items wuch that each additional evidence item decreases the probability that V = d for a var V and a value d in V.domain()")
    print("V0 = HT, d0 = NO | V1 = CO d1 = YES, V2 = BMI d2 = ~28.0, V3 = AG d3 = ~60, V4 = VG d4 = <400g/d, V5 = AC d5 = Insufficient\n")
    vars = [bmi, co, vg, hl, ht, gd, rg, db, ag, ac]
    V0 = vars[4] # ht
    V5 = vars[9] # ac
    V4 = vars[2] # vg
    V3 = vars[8] # ag
    V2 = vars[0] # bmi
    V1 = vars[1] #co

    V1.set_evidence('YES')
    V2.set_evidence('~28.0')
    V3.set_evidence('~60')
    V4.set_evidence('<400g/d')
    V5.set_evidence('Insufficient')

    prob_one = VE(medical, V0, [V5])
    prob_two = VE(medical, V0, [V5, V4])
    prob_three = VE(medical, V0, [V5, V4, V3])
    prob_four = VE(medical, V0, [V5, V4, V3, V2])
    prob_five = VE(medical, V0, [V5, V4, V3, V2, V1])

    print("Probability given V5: {}".format(prob_one))
    print("Probability given V5 and V4: {}".format(prob_two))
    print("Probability given V5 and V4 and V3: {}".format(prob_three))
    print("Probability given V5 and V4 and V3 and V2: {}".format(prob_four))
    print("Probability given V5 and V4 and V3 and V2 and V1: {}".format(prob_five))

    if prob_one[1] > prob_two[1]:
        if prob_two[1] > prob_three[1]:
            if prob_three[1] > prob_four[1]:
                if prob_four[1] > prob_five[1]:
                    print("Question 2d correct!")
                else:
                    print("INCORRECT")
            else:
                print("INCORRECT")
        else:
            print("INCORRECT")
    else:
        print("INCORRECT")
    
    return

if __name__ == '__main__':
    print("\n********************************* Problem 2a *********************************")
    printQ2a()

    print("\n********************************* Problem 2b *********************************")
    printQ2b()

    print("\n********************************* Problem 2c *********************************")
    new_printQ2c()

    print("\n********************************* Problem 2d *********************************")
    new_printQ2d()

    """ for v in [bmi, co, ht, hl, vg, gd, rg, db, ag, ac]:
        print("Variable:", v.name)
        probs = VE(medical, v, [])
        doms = v.domain()
        for i in range(len(probs)):
            print("P({0:} = {1:}) = {2:0.1f}".format(v.name, doms[i], 100*probs[i]))
        print()

    print('**********************')

    v = bmi
    for t in [ht, hl, vg, gd, rg, db, ag, ac]:
        print("Variable:", t.name)
        probs = VE(medical, v, [t, ht])
        probs1 = VE(medical, v, [ht])
        print(probs1)
        print(probs)
        doms = v.domain()
        for i in range(len(probs)):
            for j in range(len(probs)):
                #print("P({0:} = {1:}|{0:} = {1:}) = {2:0.1f}".format(v.name, t.name, doms[i], int(100*probs[i])))
                print("P({} = {}|{} = {}) = {}".format(v.name, doms[i], t.name, doms[i], 100*probs[i]))
        print() """

    """ test = ac
    probs = [
        VE(medical, test, [ht, ag, gd]), VE(medical, test, [ag, gd]), VE(medical, test, [ht, ag, gd, co]),
        VE(medical, test, [ag, gd, co]), VE(medical, test, [bmi, ag, gd, hl]), VE(medical, test, [ag, gd, hl])
    ]
    for p in probs:
        print(p) """