# import math
# tX=34.02118064
# tY=-118.2890211
# a=0.005
# i=0
# while i<2*math.pi:
#     x=(2*a*math.cos(i)+a*math.cos(2*i))+tX
#     y=(2*a*math.sin(i)-a*math.sin(2*i))+tY
#     print(str(y)+","+str(x)+",17")
#     i+=.1
#
#

def powerset(s):
    n = len(s)
    result=[]
    masks = [1<<j for j in range(n)]
    print(masks)
    for i in range(1,2**n):
        resultlist=[]
        for j in range(n):
            check=masks[j] & i
            print("check",check)
            if (masks[j] & i):
                resultlist.append(str(s[j]))
        resultstring="".join(resultlist)
        result.append(resultstring)
    print(result)

x=powerset("abc")
print(x)
