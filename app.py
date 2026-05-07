import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

data = pd.read_csv("data.csv")

X = data[['traffic']]
y = data['attack']

model = LogisticRegression()
model.fit(X,y)

pickle.dump(model, open("model.pkl","wb"))

print("Model Created Successfully")