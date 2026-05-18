import pickle
import os
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from utils.data_loader import load_data, get_features_and_target, split_and_scale

def train_and_save_models():
    df = load_data()
    X, y = get_features_and_target(df)
    X_train, X_test, y_train, y_test, scaler = split_and_scale(X, y)

    models = {
        "logistic_regression": LogisticRegression(max_iter=10000, random_state=42),
        "knn": KNeighborsClassifier(n_neighbors=5),
        "svm": SVC(kernel="linear", C=1, probability=True, random_state=42),
    }

    os.makedirs("models", exist_ok=True)

    for name, model in models.items():
        model.fit(X_train, y_train)
        with open(f"models/{name}.pkl", "wb") as f:
            pickle.dump(model, f)
        print(f"✅ {name} saved — test accuracy: {model.score(X_test, y_test):.4f}")

    with open("models/scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    print("✅ scaler saved")

if __name__ == "__main__":
    train_and_save_models()