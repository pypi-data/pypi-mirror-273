# Libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix
from sklearn import metrics
import random
import copy
import re
import os
import time
import warnings


def bevfs_algorithm(data_path, branches_generate = 3, branches_to_consider = 36,top_branches_to_select = 9):
    
    # Suppress the specific warning
    warnings.filterwarnings("ignore", message="libc not found")

    pd.options.mode.chained_assignment = None  # default is 'warn'

    # Enter the file path of the dataset
    #file_path = "/Users/mohammedbilalshakeel/Desktop/hbku/Feature selection/bev/BEV Feature Selection/simulations/srbct/samples_data_modi.txt"
    file_path = data_path
    start_time = time.time()

    ##### Functions ######

    def generating_feat_equi_random_array(n):
        # n is number of features. It should be even number so that it could easily
        # divide into 2 digits pair

        # Initially Generating Random Binary Digits Array for all the features
        random_array = np.random.randint(0, 2, n)

        # Splitting the data into couple arrays
        splitted_arrays = np.split(random_array, len(random_array)/2)

        return splitted_arrays


    def Initializing_couple_value(array):
        # Assigning random binary digits pair to couples c1,c2,....
        couple_arrays = {}
        for i, a in enumerate(array):
            couple_arrays["c{}".format(i)] = a

        return couple_arrays


    def initializing_arrays_probability(array):
        # Equal Probability is provided to every possible pair i.e, 0.25 in this case
        ## Array_probabilities = {"p00":0.25, "p01":0.25, "p10":0.25, "p11":0.25,}

        possible_pairs_str = ['00', '01', '10', '11']
        probab_distri = pd.DataFrame(
            0.25, index=possible_pairs_str, columns=possible_pairs_str)
        probab_distri

        couple_proba = {}
        for i in range(len(array)):
            couple_proba["c{}".format(i)] = probab_distri

        return couple_proba


    def knn_classifier(dataset, couple_arrays, flag):
        # Combining couples pair to form one single list to apply on the dataset
        # keeping Dataset having '1' while dropping dataset having '0'
        # Couples_arrays is a dictionary

        array_list = []
        for a in couple_arrays.values():
            array_list.append(a)

        # Converting couples pair back to simple list
        # for performing feature selection on the dataset
        array_list = np.hstack(array_list).tolist()

        # Feature Selection on the dataset (Dropping columns)
        up_data_df = dataset.iloc[:, 1:]
        reference_df = dataset.iloc[:, 1:]

        # Assigning labels
        y = dataset.iloc[:, 0]  # Labels

        # Initializing counter
        dropping_columns_counter = 0
        for i, m in enumerate(array_list):

            if m == 0:
                # If binary digit is 0, the column is dropped.
                # If '1', the column will remain in the dataset.
                up_data_df = up_data_df.drop(reference_df.columns[i], axis=1)
                dropping_columns_counter += 1

            else:
                pass

        number_of_features = (len(dataset.columns)-1) - dropping_columns_counter
        print("Number of features = ", number_of_features)

        # Assigning features
        x = up_data_df  # Training Data

        # Dividing dataset into training & testing data along with labels
        # Splitting Data Into training and testing data
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.10, shuffle=False)

        # Fitting the data on KNN classifier and print the results

        # Create KNN Classifier
        knn = KNeighborsClassifier(n_neighbors=5)

        # Train the model using the training sets
        knn.fit(x_train, y_train)

        # Predict the response for test dataset
        y_pred = knn.predict(x_test)

        # printing confusion matrix
        cnfusion_matrix = confusion_matrix(y_test, y_pred)
        class_acc = cnfusion_matrix.diagonal()/cnfusion_matrix.sum(axis=1)

        #print("The class_acc = ", class_acc)
        print("Accuracy = ", metrics.accuracy_score(y_test, y_pred)*100, ' %')

        return metrics.accuracy_score(y_test, y_pred), number_of_features, flag


    def generate_rand_val_first_branches():
        # Generating random value between 0 to 1 and selecting reward winner couple
        random_value = round(random.uniform(0, 1), 2)

        if random_value <= 0.25:
            # 'p00'
            new_random_array = [0, 0]

        elif 0.25 < random_value <= 0.5:
            # 'p01'
            new_random_array = [0, 1]
        elif 0.5 < random_value <= 0.75:
            # 'p10'
            new_random_array = [1, 0]
        else:
            # 'p11'
            new_random_array = [1, 1]

        return new_random_array, random_value


    def pair_array_to_name(array_pair):
        if array_pair == [0, 0]:
            pair_name = 'p00'

        elif array_pair == [0, 1]:
            pair_name = 'p01'

        elif array_pair == [1, 0]:
            pair_name = 'p10'

        else:
            pair_name = 'p11'

        return pair_name


    def second_lvl_branches(proba_list):
        temp_proba_list = proba_list
        checkpoints = []
        prev_checkpoint = 0

        for nbr, element in enumerate(temp_proba_list):
            checkpoints.append(temp_proba_list[element].tolist()[
                               0] + prev_checkpoint)
            prev_checkpoint = temp_proba_list[element].tolist()[
                0] + prev_checkpoint

        # Generating random value between 0 to 1 and selecting reward winner couple
        random_value = round(random.uniform(0, 1), 2)

        if random_value <= checkpoints[0]:
            # 'p00'
            new_random_array = [0, 0]

        elif checkpoints[0] < random_value <= checkpoints[1]:
            # 'p01'
            new_random_array = [0, 1]
        elif checkpoints[1] < random_value <= checkpoints[2]:
            # 'p10'
            new_random_array = [1, 0]
        else:
            # 'p11'
            new_random_array = [1, 1]

        return new_random_array, random_value


    def second_level_onward_branches(parent_couple_array, parent_couple_proba, flag, parent_couple_name, covered_nbr_branches=0):

        #print("\nparent_couple_probab_distribution = ",
        #      list(parent_couple_proba.items())[:1])
        #array_limit = 3
        for f in range(array_limit):
            # Array_limit is the number of random generated arrays in the first iteration

            # New_couple_number is the number of new arrays created so far
            new_couple_number = covered_nbr_branches + f + 1
            to_be_process_branches.append(new_couple_number)

            # Assigning New names for new branches
            couple_name = "couple_array_{}".format(new_couple_number)
            couple_proba = "couple_proba_{}".format(new_couple_number)

            locals()[couple_name] = {}
            locals()[couple_proba] = copy.deepcopy(parent_couple_proba)

            print("\n############################################")
            print("New subset of features : array ", couple_name.split('_')[-1])

            ########### S T A R T  G E N E R A T I N G  N E W  R A N D O M   A R R A Y ##############
            counter = 0
            for couple_number in parent_couple_array:
                pair_name = pair_array_to_name(
                    parent_couple_array[couple_number])[1:]
                proba_list = parent_couple_proba[couple_number].loc[[pair_name]]

                # Generating random value between 0 to 1 and selecting reward winner couple
                new_random_array, random_value = second_lvl_branches(proba_list)

                if counter < 4: # to print upto 4 first couples probability
                    counter += 1

                locals()[couple_name][couple_number] = new_random_array

            ########### E N D  G E N E R A T I N G  N E W  R A N D O M   A R R A Y ##############

            couples_arrays_dict[couple_name] = copy.deepcopy(locals()[couple_name])

            # Running Knn classifier on new random array values
            new_accuracy, number_of_features, flag = knn_classifier(
                data_df, locals()[couple_name], flag)

            if flag == 1:# abandoned function
                flag = 0

            arrays_acc[couple_name] = new_accuracy
            all_nbr_of_feat[couple_name] = number_of_features

            # defining eps
            eps = 0.2*np.tanh(abs(new_accuracy-prev_accuracy))

            # Comparing New accuracy vs previous accuracy
            if new_accuracy >= prev_accuracy:
                # Since New Accuracy is greater than previous accuracy
                # Therefore Giving Reward to the unique pair

                #print("parent_couple_proba = \n", list(parent_couple_proba.items())[:1])
                for local_key, local_value in parent_couple_proba.items():

                    row_update = pair_array_to_name(list(parent_couple_array[local_key]))[
                        1:]  # Parent array couple
                    column_update = pair_array_to_name(list(locals()[couple_name][local_key]))[
                        1:]  # branch array couple

                    # Using temporary_distribution to avoid nested dictionaries errors
                    temporary_distribution = copy.deepcopy(
                        locals()[couple_proba][local_key])

                    local_break_flag = 0
                    temp_proba_store = []
                    for couple in possible_pairs_str:
                        if column_update == couple:
                            if (temporary_distribution[couple][row_update]+(eps)) < 1:
                                temporary_distribution[couple][row_update] += eps
                            else:
                                local_break_flag = 1
                                temporary_distribution[couple][row_update] = 1

                        else:
                            if (temporary_distribution[couple][row_update]-(eps/3)) > 0:
                                temporary_distribution[couple][row_update] -= (
                                    eps/3)

                            else:
                                local_break_flag = 1
                                temporary_distribution[couple][row_update] = 0

                        locals()[couple_proba][local_key] = copy.deepcopy(
                            temporary_distribution)
                        temp_proba_store.append(
                            temporary_distribution[couple][row_update])

                    if local_break_flag == 1:
                        normalized_val = sum(temp_proba_store)
                        local_temp_proba_store = []
                        for couple in possible_pairs_str:
                            temporary_distribution[couple][row_update] = (
                                temporary_distribution[couple][row_update]/normalized_val)
                            local_temp_proba_store.append(
                                temporary_distribution[couple][row_update])
                        locals()[couple_proba][local_key] = copy.deepcopy(
                            temporary_distribution)

            else:
                # Since New Accuracy is less than previous accuracy
                # Therefore Giving Punishment to the unique pair

                for local_key, local_value in parent_couple_proba.items():
                    row_update = pair_array_to_name(list(parent_couple_array[local_key]))[
                        1:]  # Parent array couple
                    column_update = pair_array_to_name(list(locals()[couple_name][local_key]))[
                        1:]  # branch array couple

                    # Using temporary_distribution to avoid nested dictionaries errors
                    temporary_distribution = copy.deepcopy(
                        locals()[couple_proba][local_key])

                    local_break_flag = 0
                    temp_proba_store = []
                    for couple in possible_pairs_str:

                        if column_update == couple:
                            if temporary_distribution[couple][row_update]-eps > 0:
                                temporary_distribution[couple][row_update] -= eps
                            else:
                                local_break_flag = 1
                                temporary_distribution[couple][row_update] = 0

                        else:
                            if (temporary_distribution[couple][row_update]+(eps/3)) < 1:
                                temporary_distribution[couple][row_update] += eps/3
                            else:
                                local_break_flag = 1
                                temporary_distribution[couple][row_update] = 1

                        locals()[couple_proba][local_key] = copy.deepcopy(
                            temporary_distribution)
                        temp_proba_store.append(
                            temporary_distribution[couple][row_update])

                    if local_break_flag == 1:
                        normalized_val = sum(temp_proba_store)
                        local_temp_proba_store = []

                        for couple in possible_pairs_str:
                            temporary_distribution[couple][row_update] = (
                                temporary_distribution[couple][row_update]/normalized_val)

                        locals()[couple_proba][local_key] = copy.deepcopy(
                            temporary_distribution)

            #print(couple_name, "probability update for 1 couple = ")
            #print(list(locals()[couple_proba].items())[:1])
            couples_arrays_proba_dict[couple_proba] = locals()[couple_proba]

        covered_nbr_branches += array_limit
        return covered_nbr_branches, flag


    def saving_best_features(dataset, couple_arrays, prev_acc, prev_feat,temp_best_csv_path, temp_best_data):
        # Combining couples pair to form one single list to apply on the dataset
        # keeping Dataset having '1' while dropping dataset having '0'
        # Couples_arrays is a dictionary

        array_list = []
        for a in couple_arrays.values():
            array_list.append(a)

        # Converting couples pair back to simple list
        # for performing feature selection on the dataset
        array_list = np.hstack(array_list).tolist()

        # Feature Selection on the dataset (Dropping columns)
        up_data_df = dataset.iloc[:, 1:]
        reference_df = dataset.iloc[:, 1:]

        # Assigning labels
        y = dataset.iloc[:, 0]  # Labels

        # Initializing counter
        dropping_columns_counter = 0
        for i, m in enumerate(array_list):

            if m == 0:
                # If binary digit is 0, the column is dropped.
                # If '1', the column will remain in the dataset.
                up_data_df = up_data_df.drop(reference_df.columns[i], axis=1)
                dropping_columns_counter += 1

            else:
                pass

        number_of_features = (len(dataset.columns)-1) - dropping_columns_counter

        # Assigning features
        x = up_data_df  # Training Data

        # Splitting Data Into training and testing data
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.10, shuffle=False)

        # Now fitting the data on KNN classifier and print the results

        # Create KNN Classifier
        knn = KNeighborsClassifier(n_neighbors=5)

        # Train the model using the training sets
        knn.fit(x_train, y_train)

        # Predict the response for test dataset
        y_pred = knn.predict(x_test)

        # inserting lables columns in the updated features list
        x.insert(loc=0, column='output', value=y)

        new_acc = metrics.accuracy_score(y_test, y_pred)

        if new_acc >= prev_acc and number_of_features <= prev_feat:
            prev_acc = new_acc
            prev_feat = number_of_features

            # create 'best features' folder if it doesn't exist
            best_feat_folder = os.path.join(dir_path, 'best features')
            if not os.path.exists(best_feat_folder):
                os.makedirs(best_feat_folder)

            temp_best_csv_path = "{}/data_exp_{}_stage_{}_acc_{}_feat_{}.txt".format(
                best_feat_folder, repeat_experiment, stage, round(metrics.accuracy_score(y_test, y_pred), 2), number_of_features)

            # Saving Changes to data file
            #x.to_csv(best_feat_file_name, index=False)
            temp_best_data = x.copy()

        return prev_acc, prev_feat, temp_best_csv_path, temp_best_data


    # Get the directory path from the file path
    dir_path = os.path.dirname(file_path)

    # Get the file name without the directory path
    base_file_name = os.path.basename(file_path)

    # Split the file name to get the base name and extension
    base_name, file_extension = os.path.splitext(base_file_name)

    # Setting parameters
    max_experiments = 1         # Number of times the experiment will be repeated
    m = branches_to_consider    # after 'm' branches, selecting top 'x' branches
    x = top_branches_to_select  # selecting top best 'x' branches
    j = 5                       # Number of time new level branches executes

    ## initiating necessary parameters
    repeat_experiment = 0       # Current experiment number

    # store top couple performers accuracy throughout all experiments
    top_acc_all_experiments = {}
    # store 'nbr of features' for top couple performers accuracy
    number_of_feat_all_exp = {}

    stage_limit = 50
    while repeat_experiment < max_experiments:
        data = pd.read_csv(file_path)
        data_df = pd.DataFrame(data)

        # Dictionary containing Classes and number of each class samples
        classes = dict(data_df.iloc[:, 0].value_counts())

        # Saving Changes to data file
        data_df.to_csv("{}/samples_data2.txt".format(dir_path),
                       index=False)


        print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
        #print("Experiment Number = ", repeat_experiment)
        stage = 0
        top_acc_all_stages = {}       # Storing top best accuracies among stages
        prev_acc = 0              # tracking beat accuracy
        prev_feat = float('inf')  # tracking beat features

        # Define variables to store the temporary best CSV file path and its data
        temp_best_csv_path = None
        temp_best_data = None
    
        # Storing Best accuracies' number of features among stages
        number_of_feat_all_stages = {}
        try:
            while stage < stage_limit:
                flag = 1
                print("\nStage Number = ", stage)

                # Reading Data from file (dataset)
                data = pd.read_csv(
                    "{}/samples_data2.txt".format(dir_path))
                data_df = pd.DataFrame(data)

                # Number of features (excluding class)
                nbr_of_feat = len(data_df.columns)-1

                # Making sure that number of features are even
                if nbr_of_feat % 2 > 0:
                    #"odd number of features"
                    # Get the name of the column being duplicated
                    column_name = str(data_df.columns[-3]) + '_2'

                    # Adding 2nd last duplcate column
                    try:
                        data_df.insert(nbr_of_feat - 1, column_name, data_df.iloc[:, -3])
                    except ValueError:
                        suffix = 2
                        while True:
                            new_name = f"{column_name}_{suffix}"
                            if new_name not in data_df.columns:
                                data_df.insert(nbr_of_feat - 1, new_name, data_df.iloc[:, -3])
                                break
                            suffix += 1

                    #print("data_df before 2nd 2 = ", data_df)
                    data_df.to_csv(
                        "{}/samples_data2.txt".format(dir_path), index=False)
                    data = pd.read_csv(
                        "{}/samples_data2.txt".format(dir_path))
                    data_df = pd.DataFrame(data)
                    nbr_of_feat += 1
                else:
                    #"even number of features"
                    pass

                # Setting Parameters
                covered_nbr_branches = 0  # Number of cycles already processed
                k = 0                     # initiating k to compare it with number of times loop executed
                array_limit = branches_generate #3           # Number of branches created out of parent branch

                # Initiating Dictionaries
                couples_acc = {}               # It will store accuracies of different couple arrays
                store_couple_proba_names = {}  # Storing names of couples probability dictionary
                arrays_dict = {}               # Store all arrays until best feature selection
                couples_arrays_dict = {}       # Store arrays numbering as keys and arrays as values

                # Store arrays numbering as keys and probability distribution as values
                couples_arrays_proba_dict = {}
                arrays_acc = {}                # Store arrays numbering as keys and accuracy as values

                # store arrays numbers from which 3 branches will be generated
                to_be_process_branches = []
                all_nbr_of_feat = {}

                # Initially Generating Random Binary Digits equivalent to number of features
                random_features_array = generating_feat_equi_random_array(
                    nbr_of_feat)

                # Making pair for random generated binary digits
                couple_array_0 = Initializing_couple_value(random_features_array)

                # Initializing equal probability to every pair
                couple_proba_0 = initializing_arrays_probability(couple_array_0)

                # Accuracy without applying feature selection technique
                prev_accuracy, number_of_features, flag = knn_classifier(
                    data_df, couple_array_0, flag)

                if flag == 1: # abandoned function
                    flag = 0

                # Possoble pairs list
                possible_pairs_str = ['00', '01', '10', '11']

                for f in range(array_limit):
                    # Array_limit is the number of random generated arrays in the first iteration
                    # New_couple_number is the number of new arrays created so far
                    new_couple_number = covered_nbr_branches + f + 1
                    to_be_process_branches.append(new_couple_number)
                    # Assigning New names for new branches
                    couple_name = "couple_array_{}".format(new_couple_number)
                    couple_proba = "couple_proba_{}".format(new_couple_number)
                    locals()[couple_name] = {}
                    locals()[couple_proba] = copy.deepcopy(couple_proba_0)

                    print("\n############################################")
                    print("New subset of features : array ", couple_name.split('_')[-1])

                    ##################### S T A R T  G E N E R A T I N G  N E W  R A N D O M   A R R A Y #######################
                    counter = 0  # initiating counter for printing output
                    for couple_number in couple_array_0:

                        # Generating random value between 0 to 1 and selecting reward winner couple
                        new_random_array, random_value = generate_rand_val_first_branches()
                        locals()[couple_name][couple_number] = new_random_array
                        # printing only first 4 couples as output
                        if counter < 4:
                            counter += 1
                    ######################## E N D  G E N E R A T I N G  N E W  R A N D O M   A R R A Y ############################

                    # Storing data in a dictionary
                    couples_arrays_dict[couple_name] = copy.deepcopy(
                        locals()[couple_name])

                    # Running Knn classifier on new random array values
                    new_accuracy, number_of_features, flag = knn_classifier(
                        data_df, locals()[couple_name], flag)
                    if flag == 1:
                        flag = 0

                    # Storing accuracy of every generated array
                    arrays_acc[couple_name] = new_accuracy
                    all_nbr_of_feat[couple_name] = number_of_features

                    # defining eps
                    eps = 0.2*np.tanh(abs(new_accuracy-prev_accuracy))

                    ###### Comparing New & previous accuracy ######
                    if new_accuracy >= prev_accuracy:
                        # Since New Accuracy is greater than previous accuracy
                        # Therefore Giving Reward to the unique pair
                        for local_key, local_value in couple_proba_0.items():
                            row_update = pair_array_to_name(list(couple_array_0[local_key]))[
                                1:]  # Parent array couple
                            column_update = pair_array_to_name(list(locals()[couple_name][local_key]))[
                                1:]  # branch array couple
                            # Using temporary_distribution to avoid nested dictionaries errors
                            temporary_distribution = copy.deepcopy(
                                locals()[couple_proba][local_key])
                            for couple in possible_pairs_str:

                                # Giving reward to unique pair
                                if column_update == couple:
                                    temporary_distribution[couple][row_update] += eps
                                # Giving punishment to remaining pairs
                                else:
                                    temporary_distribution[couple][row_update] -= eps/3
                                locals()[couple_proba][local_key] = copy.deepcopy(
                                    temporary_distribution)
                        #print(couple_name, " = ", list(
                        #    locals()[couple_proba].items())[:4])
                    else:
                        # Since New Accuracy is less than previous accuracy
                        # Therefore Giving Punishment to the unique pair
                        for local_key, local_value in couple_proba_0.items():
                            row_update = pair_array_to_name(list(couple_array_0[local_key]))[
                                1:]  # Parent array couple
                            column_update = pair_array_to_name(list(locals()[couple_name][local_key]))[
                                1:]  # branch array couple
                            # Using temporary_distribution to avoid nested dictionaries errors
                            temporary_distribution = copy.deepcopy(
                                locals()[couple_proba][local_key])
                            for couple in possible_pairs_str:

                                # Giving punishment to unique pair
                                if column_update == couple:
                                    temporary_distribution[couple][row_update] -= eps
                                # Giving little reward to remaining pairs
                                else:
                                    temporary_distribution[couple][row_update] += eps/3
                                locals()[couple_proba][local_key] = copy.deepcopy(
                                    temporary_distribution)
                        #print(couple_name, " = ", list(
                        #    locals()[couple_proba].items())[:4])
                    couples_arrays_proba_dict[couple_proba] = locals()[
                        couple_proba]
                # Keeping track of covered branches
                covered_nbr_branches += array_limit

                ####### Exceuting Second level branches and onwards #######
                while k < j:
                
                    # Making temporary copied list so that changes can be done to main list
                    temp_to_be_process_brances = copy.deepcopy(
                        to_be_process_branches)

                    for n in temp_to_be_process_brances:
                        #print("Parent couple = ", 'couple_array_{}'.format(n))
                        # calling function which executes 2nd level onwards branches
                        branches_covered, flag = second_level_onward_branches(couples_arrays_dict['couple_array_{}'.format(
                            n)], couples_arrays_proba_dict['couple_proba_{}'.format(n)], flag, 'couple_array_{}'.format(n), covered_nbr_branches)
                        covered_nbr_branches = branches_covered
                        # removing already executed branches
                        to_be_process_branches.remove(n)

                    # if number of generated branches exceeds 'm', then select top 'x' branches
                    if len(couples_arrays_dict.keys()) >= m:
                        best_features = []
                        to_be_process_branches = []  # emptying list
                        x_temp = len(list(arrays_acc.items()))
                        temp_sorted_couples_acc = (
                            sorted(arrays_acc.items(), key=lambda x_temp: x_temp[1], reverse=True))[:x_temp]

                        # Sorting arrays  in such a way that arrays having same accuracy and
                        # are latest generated are selected first
                        sorting_couple_acc_counter = 0
                        for index, tuple_element in enumerate(temp_sorted_couples_acc):
                            first_val = tuple_element[0]
                            second_val = tuple_element[1]
                            if sorting_couple_acc_counter == 0:
                                previous_acc = second_val
                                previous_index = index
                                checkpoint_index = index
                            else:
                                if second_val == previous_acc:
                                    temp_sorted_couples_acc.insert(
                                        checkpoint_index, (first_val, second_val))
                                    temp_sorted_couples_acc.pop(index+1)
                                else:
                                    checkpoint_index = index
                                    previous_acc = second_val
                            sorting_couple_acc_counter += 1
                        sorted_couples_acc = temp_sorted_couples_acc[:x]

                        # Sorting couples_acc dictionary in descending order
                        #print(" sorted_couples_acc = ",  sorted_couples_acc)
                        print("\nTop {} best performing selected features = ".format(x),
                              sorted_couples_acc)
                        counter_nbr_save = 0

                        for element in sorted_couples_acc:
                            counter_nbr_save += 1
                            best_features.append(element[0])
                            temp_couples_arrays_dict = copy.deepcopy(
                                couples_arrays_dict)
                            if counter_nbr_save <= 1:
                                prev_acc, prev_feat, temp_best_csv_path, temp_best_data = saving_best_features(
                                    data_df, temp_couples_arrays_dict[element[0]], prev_acc, prev_feat, temp_best_csv_path, temp_best_data)
                                # Saving best 0s and 1s combination in a txt file
                        temp_couples_arrays_dict = copy.deepcopy(
                            couples_arrays_dict)

                        for array_nbr in temp_couples_arrays_dict.keys():
                            if (array_nbr in best_features):

                                # extracting numbers from string
                                array_int = int(re.findall(
                                    r'[0-9]+', array_nbr)[0])
                                to_be_process_branches.append(array_int)
                            else:
                                # Deleting extra arrays
                                del couples_arrays_dict[array_nbr]
                                del arrays_acc[array_nbr]
                                array_int = int(re.findall(
                                    r'[0-9]+', array_nbr)[0])
                                del couples_arrays_proba_dict["couple_proba_{}".format(
                                    array_int)]
                    k += 1

                # sorting arrays on accuracies
                sorted_couples_acc = (
                    sorted(arrays_acc.items(), key=lambda x: x[1], reverse=True))[:x]
                couples_arrays_dict[sorted_couples_acc[0][0]].values()

                # Initiating empty list to store couples arrays as a sngle list
                array_list = []
                for a in couples_arrays_dict[sorted_couples_acc[0][0]].values():
                    array_list.append(a)
                # Converting couples pair back to simple list for performing feature selection on the dataset
                array_list = np.hstack(array_list).tolist()

                ########## Keeping the best features and updating input data file ##########
                data = pd.read_csv(
                    "{}/samples_data2.txt".format(dir_path))

                labels = data.iloc[:, 0]
                features = data.iloc[:, 1:]
                nbr_of_feat = len(features.columns)

                # Using counter to update dataframe after deleting coloumns
                counter = 0
                for n, digit in enumerate(array_list):
                    # digit = 1 means keeping column
                    if digit == 1:
                        pass

                    else:
                        n = n-counter
                        # Dropping features
                        features.drop(features.iloc[:, [n]], axis=1, inplace=True)
                        counter += 1

                # inserting lables columns in the updated features list
                features.insert(loc=0, column='output', value=labels)

                # Saving Changes to data file
                features.to_csv(
                    "{}/samples_data2.txt".format(dir_path), index=False)
                top_acc_all_stages["Stage_{}".format(
                    stage)] = sorted_couples_acc[0]
                number_of_feat_all_stages["Stage_{}".format(
                    stage)] = all_nbr_of_feat[sorted_couples_acc[0][0]]
                stage += 1

        except ValueError:


            print("\n------------------------------------------------------------------------")
            print("------------------------------ R E S U L T -----------------------------")
            print("------------------------------------------------------------------------")
            print("\nSimulation complete !")

            # Save the temporary best CSV file if it exists
            if temp_best_csv_path is not None:
                temp_best_data.to_csv(temp_best_csv_path, index=False)

            # After every experiment, accuracies and nbr of features are stored in global dictionaries
            top_acc_all_experiments["Experiment_Number_{}".format(
                repeat_experiment)] = top_acc_all_stages
            number_of_feat_all_exp["Experiment_Number_{}".format(
                repeat_experiment)] = number_of_feat_all_stages
            #print("\nError occurs at stage = ", stage)
            print("\nThe Best accuracy in each stage = \n", top_acc_all_stages)
            print("\nSelected features for corresponding best accuracies = \n",
                  number_of_feat_all_stages)
            end_time = time.time()
            elapsed_time = end_time - start_time

            print("\nTotal Time in minutes = ", elapsed_time/60)
            print("\nThe best subset of features have been saved to 'best features' folder ")
            print("\n------------------------------------------------------------------------")
            print("------------------------------ E N D -----------------------------------")
            print("------------------------------------------------------------------------")

        except IndexError:
            # After every experiment, accuracies and nbr of features are stored in global dictionaries
            top_acc_all_experiments["Experiment_Number_{}".format(
                repeat_experiment)] = top_acc_all_stages
            number_of_feat_all_exp["Experiment_Number_{}".format(
                repeat_experiment)] = number_of_feat_all_stages
            print("\nError occurs at stage = ", stage)
            print("Top Accuracies over all stage = ", top_acc_all_stages)
            print("Number of features for best accuracies = ",
                  number_of_feat_all_stages)
        repeat_experiment += 1


