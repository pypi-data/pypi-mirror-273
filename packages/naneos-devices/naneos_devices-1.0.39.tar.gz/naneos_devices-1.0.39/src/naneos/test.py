import pandas as pd

test_ser = pd.Series([1, 2, 3, 4, 5], index=["a", "b", "c", "d", "e"])


index_exists = all([test_ser.index.isin(["x", "a"]).any()])
print(index_exists)

print([test_ser.index.isin(["x", "a"])])
# print(test_ser)
