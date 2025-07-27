import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import librosa
import numpy as np

def extract_features(path):
    y, sr = librosa.load(path, sr=22050)
    y, _ = librosa.effects.trim(y)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    return np.mean(mfcc.T, axis=0)  # 13-dim vector

df = pd.read_csv("/Users/yoshi/Desktop/ISP/Data/data.csv")

X = []
y = []

for i, row in df.iterrows():
    features = extract_features(f"static/sounds/{row['filename']}")
    X.append(features)
    y.append(row['label'])

# Train model
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)

print("Accuracy:", accuracy_score(y_test, model.predict(X_test)))

new_sound = extract_features("static/sounds/test_thunder.mp3")
predicted = model.predict([new_sound])
print("Suggested onomatopoeia:", predicted[0])
