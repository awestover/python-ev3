def arr_mult(arr, scalar):
	out = []
	for el in arr:
		out.append(el*scalar)
	return out

def add_point_wise(arr1, arr2):
	out = []
	for i in range(0, len(arr1)):
		out.append(arr1[i] + arr2[i])
	return out
