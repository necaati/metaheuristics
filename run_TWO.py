from models.multiple_solution.physics_based.TWO import BaseTWO, OppoTWO, OTWO, LevyTWO, ITWO
from utils.FunctionUtil import *
import json
import os

function_list = [islo_uni_F1, islo_uni_F2, islo_uni_F3, islo_uni_F4, islo_uni_F5, islo_uni_F6, islo_uni_F7, islo_uni_F8,
                 islo_multi_F9, islo_multi_F10, islo_multi_F11, islo_multi_F12, islo_multi_F13, islo_multi_F14,
                 islo_multi_F15, islo_multi_F16, islo_hybrid_F17, islo_hybrid_F18, islo_hybrid_F19, islo_hybrid_F20,
                 islo_hybrid_F21, islo_hybrid_F22, islo_hybrid_F23, islo_compos_F24, islo_compos_F25, islo_compos_F26,
                 islo_compos_F27, islo_compos_F28, islo_compos_F29, islo_compos_F30]

# function_list = [islo_uni_F1]
dimensions = [50, 100]
SLnO_paras = {
        "epoch": 500,
        "pop_size": 100
    }
model_name = "TWO"
n_times = 20
epoch = SLnO_paras["epoch"]
results = []

for dim in dimensions:
    for func in function_list:
        ## Setting parameters`
        root_paras = {
            "problem_size": dim,
            "domain_range": [-100, 100],
            "print_train": False,
            "objective_func": func
        }

        ## Run model and save results
        function_name = func.__name__
        print("starting model {} with function {} running in {} dimension".format(model_name, function_name, dim))
        statistical_history_train_losses = np.zeros((n_times, epoch))
        statistical_final_optimal_values = np.zeros(n_times)

        for i in range(n_times):
            md = BaseTWO(root_algo_paras=root_paras, two_paras=SLnO_paras)
            gbest, train_loss = md._train__()
            statistical_history_train_losses[i] += np.asarray(train_loss)
            statistical_final_optimal_values[i] += train_loss[-1]
            print("{} of 20 times: result {}".format(i, train_loss[-1]))

        mean_history_train_loss = np.mean(statistical_history_train_losses, axis=0)
        mean_final_optimal_value = np.mean(statistical_final_optimal_values)
        std_final_optimal_value = np.std(statistical_final_optimal_values)

        result = {
            "dimension": dim,
            "function_name": function_name,
            "mean_history_train_loss": mean_history_train_loss.tolist(),
            "mean_final_optimal_value": format(mean_final_optimal_value, '.2e'),
            "std_final_optimal_value": format(std_final_optimal_value, '.2e')
        }
        results.append(result)
        print("***************************************************")

path = "results/"+model_name
if not os.path.exists(path):
    os.makedirs(path)
with open(path+'/'+model_name+'.json', 'w') as fp:
    json.dump(results, fp)

# root_paras = {
#     "problem_size": 50,
#     "domain_range": [-100, 100],
#     "print_train": True,
#     "objective_func": islo_compos_F24
# }
# two_paras = {
#     "epoch": 500,
#     "pop_size": 100,
# }
#
# ## Run model
# md = BaseTWO(root_algo_paras=root_paras, two_paras=two_paras)
# md._train__()
