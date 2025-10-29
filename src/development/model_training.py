import sys
import warnings
import numpy as np
import pandas as pd
from time import time
from pathlib import Path
from lightgbm import LGBMClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.calibration import cross_val_predict
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.model_selection import GridSearchCV, PredefinedSplit, train_test_split

warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", message="X does not have valid feature names")

# Helper function to print markdown-style headers
def print_md_header(text: str, max_len: int = 33, symbol: str = "═"):
    text = text.strip()
    text_len = len(text)
    pad_total = max_len - text_len - 2  # 2 spaces around text
    if pad_total < 0:
        pad_total = 0
    left = pad_total // 2
    right = pad_total - left
    line = f"\n{symbol * left} {text} {symbol * right}"
    print(line)

def main(path, from_raw=True):
    # Load dataset
    df = pd.read_csv(path)
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    # Feature extraction
    ROOT = Path(__file__).resolve().parent.parent
    sys.path.append(str(ROOT))

    from features_2d import Extract2DFeatures

    if from_raw:
        feature_extractor = Extract2DFeatures.from_raw(X)
    else:
        feature_extractor = Extract2DFeatures(X)

    X = feature_extractor.extract_features()

    # Split dataset
    X_train, X_val, y_train, y_val = train_test_split(X.iloc[:, 1:], y, test_size=0.2, random_state=42, stratify=y)

    # Scale features
    scaler = MinMaxScaler().fit(X_train)
    X_train = scaler.transform(X_train)
    X_val = scaler.transform(X_val)

    # K-Best feature selection
    kbest = SelectKBest(score_func=f_classif, k=150).fit(X_train, y_train)
    feature_names = kbest.get_support(indices=True)
    X_train = kbest.transform(X_train)
    X_val = kbest.transform(X_val)

    Feature = []

    for i in feature_names:
        Feature.append(X.columns[i+1])

    # Stratified 5-fold CV
    def custom_cv(y, nr_fold):
        ix = []
        for i in range(0, len(y)):
            ix.append(i)
        ix = np.array(ix)
        return PredefinedSplit(ix%nr_fold)

    # CV function to compute metrics
    def cv(clf, X, y, nr_fold):
        abc = cross_val_predict(clf,X,y,cv=custom_cv(y, nr_fold),method="predict_proba")[:,1]
        p =  np.round(abc)
        TP=0
        FP=0
        TN=0
        FN=0
        for i, j in zip(y.index, range(p.shape[0])):
            if y[i]==0 and p[j]==0:
                TN+= 1
            elif y[i]==0 and p[j]==1:
                FP+= 1
            elif y[i]==1 and p[j]==0:
                FN+= 1
            elif y[i]==1 and p[j]==1:
                TP+= 1
        ACC = (TP+TN)/(TP+FP+TN+FN)
        SENS = TP/(TP+FN)
        SPEC = TN/(TN+FP)
        det = np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
        if (det == 0):
            MCC = 0
        else:
            MCC = ((TP*TN)-(FP*FN))/det
        F1 = TP/(TP+(0.5*(FP+FN)))
        return [ACC, SENS, SPEC, MCC, F1]
    
    # Test scoring functions
    def test(clf,X,y,Xt, yt):
        clf.fit(X,y)
        abc = clf.predict_proba(Xt)[:,1]
        p =  np.round(abc)
        TP=0
        FP=0
        TN=0
        FN=0
        for i, j in zip(yt.index,range(p.shape[0])):
            if yt[i]==0 and p[j]==0:
                TN+= 1
            elif yt[i]==0 and p[j]==1:
                FP+= 1
            elif yt[i]==1 and p[j]==0:
                FN+= 1
            elif yt[i]==1 and p[j]==1:
                TP+= 1
        ACC = (TP+TN)/(TP+FP+TN+FN)
        SENS = TP/(TP+FN)
        SPEC = TN/(TN+FP)
        det = np.sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))
        if (det == 0):
            MCC = 0
        else:
            MCC = ((TP*TN)-(FP*FN))/det
        F1 = TP/(TP+(0.5*(FP+FN)))
        return [ACC, SENS, SPEC, MCC, F1]
    

    # Set hyperparameter grid
    param = [20, 50, 100, 200]

    # Grid Search CV
    model = LGBMClassifier(random_state=0, verbose=-1)
    search = GridSearchCV(model, param_grid={'n_estimators': param }, cv=custom_cv(y_train, 10), n_jobs=-1, verbose=1)
    search.fit(X_train, y_train)
    best_model = search.best_estimator_

    # CV model performance (ACC, PREC, REC, F1, MCC)
    print_md_header("Cross-Validation Metrics")
    ACC, SENS, SPEC, MCC, F1 = cv(best_model, X_train, y_train, 10)
    print(f"ACC  : {ACC:.4f}")
    print(f"SENS : {SENS:.4f}")
    print(f"SPEC : {SPEC:.4f}")
    print(f"F1   : {F1:.4f}")
    print(f"MCC  : {MCC:.4f}")

    print(f"\nBest param: {search.best_params_}")

    # Top 15 Important Features
    feature_importances = best_model.feature_importances_
    indices = np.argsort(feature_importances)[::-1][:15]
    feature_importances_df = pd.DataFrame({
        'Feature': [Feature[i] for i in indices],
        'Importance': feature_importances[indices]
    })
    feature_importances_df = feature_importances_df.sort_values(by='Importance', ascending=False)
    print_md_header("Top 15 Important Features")
    print(feature_importances_df)

    # Validate model
    print_md_header("Validation Metrics")
    ACC, SENS, SPEC, MCC, F1 = test(best_model, X_train, y_train, X_val, y_val)
    print(f"ACC  : {ACC:.4f}")
    print(f"SENS : {SENS:.4f}")
    print(f"SPEC : {SPEC:.4f}")
    print(f"F1   : {F1:.4f}")
    print(f"MCC  : {MCC:.4f}")


if __name__ == "__main__":
    start_time = time()
    main("../../dataset/train_dataset.csv",from_raw=True)
    print_md_header("Completed Running")
    print(f"Run time: {time() - start_time:.2f} sec.")