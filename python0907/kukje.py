def DotProduct(U,V):
    #U와 V Shape 확인
    if(U.shape[1] != 1 or V.shape[1] != 1): # 벡터가 아니면
        print("내적은 열 벡터만 연산할수 있어요")
        return
    #V의 shape 확인
    if(U.shape[0] != V.shape[0]): #두개의 벡터의 길이가 같지 않으면
        print("두 열벡터의 길이가 달라요")
        return
    n= U.shape[0]
    product=0
    for i in range(n):
        product += U[i,0] * V[i,0]
    return product

def f(i):
    print(i)
