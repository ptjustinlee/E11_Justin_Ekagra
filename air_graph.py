import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('data/air.csv')
plt.figure(figsize=(12, 6))
plt.hist(data['par05'], bins = 4)
plt.show()

print(data.head())