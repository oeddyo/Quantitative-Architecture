
def work():
    for k in range(0,10):
        print k
        de = 0.3**k*0.7**(10-k) + 0.7**k*0.3**(10-k) + 0.95**k*0.05**(10-k)
        n1 = 0.3**k*0.7**(10-k)*1/3.0
        n2 = 0.7**k*0.3**(10-k)*1/3.0
        n3 = 0.95**k*0.05**(10-k)*1/3.0
        print n1/de,n2/de,n3/de

print work()
