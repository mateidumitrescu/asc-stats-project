import pandas as pd
from app import webserver

def calculate_states_mean(csv_data: list, data: dict):
    """Helper function to calculate the mean of each state (/api/states_mean)"""
    states_values = {} # location: [sum, count]
    for row in csv_data:
        if row['Question'] == data['question']:
            if row['LocationDesc'] not in states_values:
                states_values[row['LocationDesc']] = []
                # position 0 will store sum of values
                states_values[row['LocationDesc']].append(float(row['Data_Value']))
                states_values[row['LocationDesc']].append(1) # position 1 will store count of values
            else:
                states_values[row['LocationDesc']][0] += float(row['Data_Value'])
                states_values[row['LocationDesc']][1] += 1

    # creating a dictionary with the mean of each state
    states_mean = {}
    for state, values in states_values.items():
        states_mean[state] = values[0] / values[1]

    # sorting in ascending order based on the mean
    states_mean = dict(sorted(states_mean.items(), key=lambda item: item[1]))

    return states_mean

def calculate_state_mean(csv_data: list, data: dict):
    """Helper function to calculate the mean of a specific state (/api/state_mean)"""

    state_mean = 0
    count = 0
    for row in csv_data:
        if row['LocationDesc'] == data['state'] and row['Question'] == data['question']:
            state_mean += float(row['Data_Value'])
            count += 1

    if count == 0:
        return {data['state']: 0}
    result = {data['state']: state_mean / count}
    return result

def calculate_best5(csv_data: list, data: dict):
    """Helper function to calculate the best 5 or worst 5 states (/api/best5)"""
    states_values = {} # location: [sum, count]
    # checking which type of question it is
    if data['question'] in webserver.data_ingestor.questions_best_is_min:
        last5 = True
    else:
        last5 = False
    for row in csv_data:
        if row['Question'] == data['question']:
            if row['LocationDesc'] not in states_values:
                states_values[row['LocationDesc']] = []
                # position 0 will store sum of values
                states_values[row['LocationDesc']].append(float(row['Data_Value']))
                states_values[row['LocationDesc']].append(1) # position 1 will store count of values
            else:
                states_values[row['LocationDesc']][0] += float(row['Data_Value'])
                states_values[row['LocationDesc']][1] += 1

    states_mean = {}
    for state, values in states_values.items():
        states_mean[state] = values[0] / values[1]

    # creating a dictionary with the mean of each state
    states_mean = dict(sorted(states_mean.items(), key=lambda item: item[1]))
    if last5:
        # getting best 5 from the beginning
        result = {k: v for k, v in list(states_mean.items())[:5]}
    else:
        # getting best 5 from the end
        result = {k: v for k, v in list(states_mean.items())[-5:]}

    return result

def calculate_worst5(csv_data: list, data: dict):
    """Helper function to calculate the worst 5 states (/api/worst5)"""
    states_values = {} # location: [sum, count]
    # checking which type of question it is
    if data['question'] in webserver.data_ingestor.questions_best_is_max:
        last5 = True
    else:
        last5 = False
    for row in csv_data:
        if row['Question'] == data['question']:
            if row['LocationDesc'] not in states_values:
                states_values[row['LocationDesc']] = []
                # position 0 will store sum of values
                states_values[row['LocationDesc']].append(float(row['Data_Value']))
                states_values[row['LocationDesc']].append(1) # position 1 will store count of values
            else:
                states_values[row['LocationDesc']][0] += float(row['Data_Value'])
                states_values[row['LocationDesc']][1] += 1

    states_mean = {}
    for state, values in states_values.items():
        states_mean[state] = values[0] / values[1]

    # creating a dictionary with the mean of each state
    states_mean = dict(sorted(states_mean.items(), key=lambda item: item[1]))
    if last5:
        # getting best 5 from the beginning
        result = {k: v for k, v in list(states_mean.items())[:5]}
    else:
        # getting best 5 from the end
        result = {k: v for k, v in list(states_mean.items())[-5:]}

    return result

def calculate_global_mean(csv_data: list, data: dict):
    """Helper function to calculate the global mean (/api/global_mean)"""
    global_mean = 0
    count = 0
    for row in csv_data:
        if row['Question'] == data['question']:
            global_mean += float(row['Data_Value'])
            count += 1

    if count == 0:
        return {"global_mean": 0}
    result = {"global_mean": global_mean / count}
    return result

def calculate_diff_from_mean(csv_data: list, data: dict):
    """Helper function to calculate the difference of each state from the global mean (/api/diff_from_mean)"""
    states_mean = calculate_states_mean(csv_data, data)
    global_mean = calculate_global_mean(csv_data, data)

    diff_from_mean = {}
    for state, mean in states_mean.items():
        diff_from_mean[state] = global_mean['global_mean'] - mean

    return diff_from_mean

def calculate_state_diff_from_mean(csv_data: list, data: dict):
    """Helper function to calculate the difference of a specific state from the global mean (/api/state_diff_from_mean)"""

    global_mean = calculate_global_mean(csv_data, data)
    state_mean = calculate_state_mean(csv_data, data)

    diff_from_from_mean = {data['state']: global_mean['global_mean'] - state_mean[data['state']]}

    return diff_from_from_mean

def calculate_mean_by_category(csv_data: list, data: dict):
    """Helper function to calculate the mean of each category (/api/mean_by_category)"""

    # converting data to a pandas dataframe for easier manipulation
    dataframe = pd.DataFrame(csv_data)
    # keeping only data that is relevant to the question (copying it to avoid modifying the original dataframe)
    filtered_dataframe = dataframe[dataframe['Question'] == data['question']].copy()

    # converting the data value to float
    filtered_dataframe['Data_Value'] = pd.to_numeric(filtered_dataframe['Data_Value'], errors='coerce')

    # calculating the mean of each category
    mean_values = filtered_dataframe.groupby(['LocationDesc', 'StratificationCategory1',\
        'Stratification1'])['Data_Value'].mean().reset_index(name='MeanDataValue')

    result = {}
    for _, row in mean_values.iterrows():
        if row['LocationDesc'] != '' and \
            row['StratificationCategory1'] != '' and \
                row['Stratification1'] != '':
            key = str((row['LocationDesc'], row['StratificationCategory1'], row['Stratification1']))
            value = row['MeanDataValue']
            result[key] = value

    return result

def get_jobs_helper():
    """Helper function to get running jobs and done jobs (/api/jobs)"""
    result = {}
    for job_id, status in webserver.tasks_runner.jobs.items():
        result[job_id] = status['status']

    result['status'] = 'done'

    return result

def calculate_state_mean_by_category(csv_data: list, data: dict):
    """Helper function to calculate the mean of each category for a specific state (/api/state_mean_by_category)"""

    # converting data to a pandas dataframe for easier manipulation
    dataframe = pd.DataFrame(csv_data)
    # keeping only data that is relevant to the question (copying it to avoid modifying the original dataframe)
    filtered_dataframe = dataframe[(dataframe['Question'] == data['question'])\
                                & (dataframe['LocationDesc'] == data['state'])].copy()

    # case when the state is not found
    if filtered_dataframe.empty:
        return {data['state']: 0}

    # converting the data value to float
    filtered_dataframe['Data_Value'] = pd.to_numeric(\
        filtered_dataframe['Data_Value'], errors='coerce')

    # calculating the mean of each category
    mean_values = filtered_dataframe.groupby(['LocationDesc',\
        'StratificationCategory1',\
            'Stratification1'])['Data_Value'].mean().\
                reset_index(name='MeanDataValue')

    result = {}
    dict_to_add = {}
    # creating a dictionary with the mean of each category
    for _, row in mean_values.iterrows():
        if row['LocationDesc'] != '' and \
            row['StratificationCategory1'] != '' and \
                row['Stratification1'] != '':
            key = str((row['StratificationCategory1'], row['Stratification1']))
            value = row['MeanDataValue']
            dict_to_add[key] = value
    result[row['LocationDesc']] = dict_to_add
    return result
