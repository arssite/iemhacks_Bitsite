import numpy as np
import pandas as pd
import warnings
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import pickle
warnings.filterwarnings('ignore')
df = pd.read_csv("Fertilizer.csv")
plt.figure(figsize=(16,8))
sns.countplot(x='Fertilizer Name', data = df)
X = df.drop(columns=['Fertilizer Name'])
y = df['Fertilizer Name']
X_train,X_test,y_train,y_test = train_test_split(X,y,train_size=0.7,shuffle=True,random_state=42)
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
X_train[0]
from sklearn.ensemble import RandomForestClassifier
classifier = RandomForestClassifier(n_estimators=100,criterion = 'gini', random_state=42)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)
from sklearn.metrics import confusion_matrix,accuracy_score
cm = confusion_matrix(y_test,y_pred)
print(cm)
accuracy_score(y_test,y_pred)
from sklearn.preprocessing import LabelEncoder
encode_ferti = LabelEncoder()
df['Fertilizer Name']=encode_ferti.fit_transform(df['Fertilizer Name'])
#creating the dataframe
Fertilizer = pd.DataFrame(zip(encode_ferti.classes_,encode_ferti.transform(encode_ferti.classes_)),columns=['original','Encoded'])
Fertilizer = Fertilizer.set_index('original')
#Fertilizer
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(df.drop(columns=['Fertilizer Name']),df['Fertilizer Name'],test_size=0.2,random_state=1)
print('Shape of Splitting :')
print('x_train = {}, y_train = {}, x_test = {}, y_test = {}'.format(x_train.shape,y_train.shape,x_test.shape,y_test.shape))

x_train.info()
rand = RandomForestClassifier(random_state = 42)
rand.fit(x_train,y_train)
pred_rand = rand.predict(x_test)
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report

params = {
    'n_estimators':[300,400,500],
    'max_depth':[5,6,7],
    'min_samples_split':[2,5,8]
}
grid_rand = GridSearchCV(rand,params,cv=3,verbose=3,n_jobs=-1)

grid_rand.fit(x_train,y_train)

pred_rand = grid_rand.predict(x_test)

print(classification_report(y_test,pred_rand))

print('Best score : ',grid_rand.best_score_)
print('Best params : ',grid_rand.best_params_)

pickle_out = open('classifier1.pkl', 'wb')
pickle.dump(grid_rand,pickle_out)
pickle_out.close()
model = pickle.load(open('classifier1.pkl', 'rb'))
ans = model.predict([[12,10,13]])
if ans[0] == 0:
    print("TEN-TWENTY SIX-TWENTY SIX")
elif ans[0] == 1:
    print("Fourteen-Thirty Five-Fourteen")
elif ans[0] == 2:
    print("Seventeen-Seventeen-Seventeen")   
elif ans[0] == 3:
    print("TWENTY-TWENTY")
elif ans[0] == 4:
    print("TWENTY EIGHT-TWENTY EIGHT")
elif ans[0] == 5:
    print("DAP")
else:
    print("UREA")