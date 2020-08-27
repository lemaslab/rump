import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC

def svm_code(csv_file, output_fig):
    df_read = pd.read_csv(csv_file)
    #### NOC values #########
    sum_noc = []
    sum_noc2 = []
    sum_noc3 = []
    sum_noc4 = []
    sum_noc5 = []
    sum_noc6 = []
    sum_noc7 = []
    sum_noc8 = []

    for i in len(df_read):
        sum_1noc = df_read["QE2_sbs_11_11[27NOC].mzXML Peak height"].values[i]
        sum_2noc = df_read["QE2_sbs_11_15[29NOC].mzXML Peak height"].values[i]
        sum_3noc = df_read["QE2_sbs_11_12[30NOC].mzXML Peak height"].values[i]
        sum_4noc = df_read["QE2_sbs_11_23[28NOC].mzXML Peak height"].values[i]
        sum_5noc = df_read["QE2_sbs_11_36[31NOC].mzXML Peak height"].values[i]
        sum_6noc = df_read["QE2_sbs_11_22[26NOC].mzXML Peak height"].values[i]
        sum_7noc = df_read["QE2_sbs_11_33[25NOC].mzXML Peak height"].values[i]
        sum_8noc = df_read["QE2_sbs_11_41[32NOC].mzXML Peak height"].values[i]
        sum_noc.append(sum_1noc)
        sum_noc2.append(sum_2noc)
        sum_noc3.append(sum_3noc)
        sum_noc4.append(sum_4noc)
        sum_noc5.append(sum_5noc)
        sum_noc6.append(sum_6noc)
        sum_noc7.append(sum_7noc)
        sum_noc8.append(sum_8noc)

    sum_noc = np.array(sum_noc)
    sum_noc2 = np.array(sum_noc2)
    sum_noc3 = np.array(sum_noc3)
    sum_noc4 = np.array(sum_noc4)
    sum_noc5 = np.array(sum_noc5)
    sum_noc6 = np.array(sum_noc6)
    sum_noc7 = np.array(sum_noc7)
    sum_noc8 = np.array(sum_noc8)

    noc_av = np.vstack((sum_noc,
                        sum_noc2,
                        sum_noc3,
                        sum_noc4,
                        sum_noc5,
                        sum_noc6,
                        sum_noc7,
                        sum_noc8)).T

    av_calculated = np.mean(noc_av, axis=1)

    ############ Average N values #######################

    sum_n = []
    sum_n2 = []
    sum_n3 = []
    sum_n4 = []
    sum_n5 = []
    sum_n6 = []
    sum_n7 = []
    sum_n8 = []

    for i in len(df_read):
        sum_1n = df_read["QE2_sbs_11_19[16N].mzXML Peak height"].values[i]
        sum_2n = df_read["QE2_sbs_11_20[11N].mzXML Peak height"].values[i]
        sum_3n = df_read["QE2_sbs_11_32[15N].mzXML Peak height"].values[i]
        sum_4n = df_read["QE2_sbs_11_28[12N].mzXML Peak height"].values[i]
        sum_5n = df_read["QE2_sbs_11_46[14N].mzXML Peak height"].values[i]
        sum_6n = df_read["QE2_sbs_11_40[13N].mzXML Peak height"].values[i]
        sum_7n = df_read["QE2_sbs_11_8[9N].mzXML Peak height"].values[i]
        sum_8n = df_read["QE2_sbs_11_7[10N].mzXML Peak height"].values[i]
        sum_n.append(sum_1n)
        sum_n2.append(sum_2n)
        sum_n3.append(sum_3n)
        sum_n4.append(sum_4n)
        sum_n5.append(sum_5n)
        sum_n6.append(sum_6n)
        sum_n7.append(sum_7n)
        sum_n8.append(sum_8n)

    sum_n = np.array(sum_n)
    sum_n2 = np.array(sum_n2)
    sum_n3 = np.array(sum_n3)
    sum_n4 = np.array(sum_n4)
    sum_n5 = np.array(sum_n5)
    sum_n6 = np.array(sum_n6)
    sum_n7 = np.array(sum_n7)
    sum_n8 = np.array(sum_n8)

    av_n = np.vstack((sum_n,
                      sum_n2,
                      sum_n3,
                      sum_n4,
                      sum_n5,
                      sum_n6,
                      sum_n7,
                      sum_n8)).T
    av_ncalculated = np.mean(av_n, axis=1)

    ############### Combine N and NOC Arrays #################

    noc_new = []
    n_new = []

    for use1, use2 in zip(av_calculated, av_ncalculated):
        noc_new.append(use1)
        n_new.append(use2)

    noc_new = np.array(noc_new)
    n_new = np.array(n_new)

    av_total = np.vstack((noc_new, n_new))

    ######## Y Array #############

    y_array = [1, 0]

    ######### Feature Names ###########

    columns = ["row m/z", "row retention time", "row ID"]
    row_charge = []
    row_time = []
    df_read = pd.read_csv(csv_file, usecols=columns)

    value = df_read["row m/z"]
    #ROW_ID = df_read["row ID"]
    value_2 = df_read["row retention time"]
    for number in value:
        row_charge.append(number)
    row_chargeround = [round(num, 3) for num in row_charge]

    feature_names1 = []

    for number_1 in value_2:
        row_time.append(number_1)
    row_timeround = [round(num, 3) for num in row_time]

    for x_value, y_value in zip(row_chargeround, row_timeround):
        feature_names1.append("%s_%s"%(x_value, y_value))

    feature_names2 = np.array(feature_names1)

    ############ SVM ##########

    clf_value = LinearSVC(C=10, random_state=0, max_iter=1000)
    clf_value.fit(av_total, y_array)

    ######## Plot Feature Selection ###########

    def plot_coefficients(classifier, feature_names, top_features=10):
        coef = classifier.coef_.ravel()
        top_positive_coefficients = np.argsort(coef)[-top_features:]
        top_negative_coefficients = np.argsort(coef)[:top_features]
        top_coefficients = np.hstack([top_negative_coefficients, top_positive_coefficients])
        # create plot
        figure = plt.figure(figsize=(15, 5))
        colors = ['red' if c < 0 else 'blue' for c in coef[top_coefficients]]
        plt.bar(np.arange(2 * top_features), coef[top_coefficients], color=colors)
        plt.xlabel("Metabolite Identity")
        plt.suptitle("Top Positive and Negative Features")
        plt.ylabel("Relative Importance")
        feature_names = feature_names2
        plt.xticks(np.arange(1, 1 + 2 * top_features),
                   feature_names[top_coefficients],
                   rotation=60,
                   ha='right')
        figure.savefig(output_fig)
        plt.show()

    plot_coefficients(clf_value, feature_names2)

if __name__ == '__main__':

    import argparse

    PARSER_1 = argparse.ArgumentParser()
    PARSER_1.add_argument('-i',
                          '--input',
                          default="pos_data_after_blank_subtraction.csv",
                          help="input file")
    PARSER_1.add_argument('-o',
                          '--output',
                          default='SVM_feature_importance.png',
                          help="location of output figure")
    ARGS_1 = PARSER_1.parse_args()

    svm_code(ARGS_1.input, ARGS_1.output)
