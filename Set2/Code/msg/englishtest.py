#!/usr/bin/python3.4m


def englishtest(result, etaoin_shrdlu=[12.02,9.1,8.12,7.68,7.31,6.95,6.28,6.02,5.92,4.32,3.98,2.88]):
    """ This should return a list of possible english text
        result = msg from decrypt to test
        etaoin_shrdlu = averages used for character test"""
    
    a = len(result)
    single = []
    for i in range(12):
        single.append(9999)
    total = 0
    single[0]= result.count(b'e') + result.count(b'E')
    single[1]= result.count(b't') + result.count(b'T')
    single[2]= result.count(b'a') + result.count(b'A')
    single[3]= result.count(b'o') + result.count(b'O')
    single[4]= result.count(b'i') + result.count(b'I')
    single[5]= result.count(b'n') + result.count(b'N')
    single[6]= result.count(b's') + result.count(b'S')
    single[7]= result.count(b'h') + result.count(b'H')
    single[8]= result.count(b'r') + result.count(b'R')
    single[9]= result.count(b'd') + result.count(b'D')
    single[10]= result.count(b'l') + result.count(b'L')
    single[11]= result.count(b'u') + result.count(b'U')

    for i in range(12):
        if single[i] == 0:
            single[i] =100
        else:
            single[i] = single[i]/a
    for i in single:
        total = total + i
   
    return total, single
