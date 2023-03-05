import numpy as np

#넘파이는 벡터 연산.
#즉 , 곱하거나 나누거나 Bool 연산을 해도 병렬로 처리 된다
b = np.array([10,10,11])
# --넘파이의 불린 연산--
# print((a==2)&(b==10))

arr = np.array([[[1,2,3,4],
                [5,6,7,8],
                [9,10,11,12]],
                [[1,2,3,4],
                [5,6,7,8],
                [9,10,11,12]]]
               )
arr *= 10
# 3차원 배열의 크기..
# 가장큰 뭉태기  중간 뭉태기     작은 뭉태기
# print(len(arr),len(arr[0]),len(arr[0][0]))
# method ->    arr.ndim ,   arr.shape
# print(arr.ndim)
# print(arr.shape)

# 배열 인덱싱 은 리스트 인덱싱과 비슷
m = np.array([[ 0,  1,  2,  3,  4],
            [ 5,  6,  7,  8,  9],
            [10, 11, 12, 13, 14]])
#
# 이 행렬에서 값 7 을 인덱싱한다.
# 이 행렬에서 값 14 을 인덱싱한다.
# 이 행렬에서 배열 [6, 7] 을 슬라이싱한다.
# 이 행렬에서 배열 [7, 12] 을 슬라이싱한다.
# 이 행렬에서 배열 [[3, 4], [8, 9]] 을 슬라이싱한다.
# print(m[1][2])
# print(m[-1][-1])
# print(m[1][1:3])
# print(m[1:,2])
# print(m[:2,3:])

a = np.array(list(range(0,10)))
idx = np.array([True, False, True, False, True,
               False, True, False, True, False])

x = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
             11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
print(x[(x % 3 == 0) & (x % 4 == 1)])
# a = np.zeros((3,3),dtype='int')
#
# ones_like , zeros_like 은 다른 ndarray 크기와 같게 복사해줌 ㅇㅇ
# b = np.ones_like(a,dtype='f')
# print(b)

# g = np.empty((4,3))
# print(g)

# 파이썬 range와 유사함
a = np.arange(10)
# linspace 와 logspace의 step인자는 step이 아닌 개수. 즉 step 개수로 나눈다
a = np.linspace(0,100,7)
a = np.linspace(0.1,1,10)
a = np.array([[1,2,3],[4,5,6]])
a = a.T
# reshape 뒤의 인자 -1로 가능
a = np.array([[ 0,  1,  2,  3],
       [ 4,  5,  6,  7],
       [ 8,  9, 10, 11]])
a = np.zeros((3,3))
b = np.ones((3,2))
c = np.hstack([a,b])
d = np.arange(10,51,10)
e = d+50
f = e+50

print(np.tile(np.vstack([c,d,e,f]),(2,1)))
