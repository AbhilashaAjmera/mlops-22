from sklearn import datasets, svm, metrics,tree
import pdb

from utils import (
    preprocess_digits,
    train_dev_test_split,
    h_param_tuning,
    data_viz,
    pred_image_viz,
    get_all_h_param_comb_svm,
    get_all_h_param_comb_dec,
    tune_and_save,
    comparision_table
)
from joblib import dump, load
train_frac, dev_frac, test_frac = 0.8, 0.1, 0.1
assert train_frac + dev_frac + test_frac == 1.0
# hyper parameters
gamma_list = [0.01, 0.005, 0.001, 0.0005, 0.0001]
c_list = [0.1, 0.2, 0.5, 0.7, 1, 2, 5, 7, 10]

svm_params = {}
svm_params["gamma"] = gamma_list
svm_params["C"] = c_list
svm_h_param_comb = get_all_h_param_comb_svm(svm_params)
max_depth_list = [10,20,50,100]
dec_params = {}
dec_params["max_depth"] = max_depth_list
dec_h_param_comb = get_all_h_param_comb_dec(dec_params)
h_param_comb = {"svm":svm_h_param_comb, "decision_tree":dec_h_param_comb }

#Dataset
digits = datasets.load_digits()
data_viz(digits)
data, label = preprocess_digits(digits)

del digits
metric = metrics.accuracy_score
n_cv = 5
results = {}

for n in range(n_cv):    
    x_train, y_train, x_dev, y_dev, x_test, y_test = train_dev_test_split(data, label, train_frac, dev_frac)
    models_of_choice = {
        "svm":svm.SVC(), 
        "decision_tree":tree.DecisionTreeClassifier()
    }

    for clf_name in models_of_choice:
        clf = models_of_choice[clf_name]
        actual_model_path = tune_and_save(clf, x_train, y_train, x_dev, y_dev, metric, h_param_comb[clf_name], model_path=None)

        best_model = load(actual_model_path)
        predicted = best_model.predict(x_test)
        if not clf_name in results:
            results[clf_name]=[]

        results[clf_name].append(metric(y_pred=predicted, y_true=y_test))

        print(
            f"Classification report for classifier {clf}:\n"
            f"{metrics.classification_report(y_test, predicted)}\n"
        )

print(results)

new_df,mean_val,std_val = comparision_table(results,n_cv)
print("The comparision table with mean and standard deviation is:")
print(new_df.to_string(index=False))
