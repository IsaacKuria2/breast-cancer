import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def load_data(filepath="breast-cancer.csv"):
    df = pd.read_csv(filepath)
    df.drop(columns=["id"], inplace=True)
    df.drop(columns=[c for c in df.columns if "Unnamed" in c], inplace=True)
    df["diagnosis"] = df["diagnosis"].map({"M": 1, "B": 0})
    return df

def get_features_and_target(df):
    X = df.drop("diagnosis", axis=1)
    y = df["diagnosis"]
    return X, y

def split_and_scale(X, y, test_size=0.2, random_state=42):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    return X_train_scaled, X_test_scaled, y_train, y_test, scaler