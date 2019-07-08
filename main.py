import pandas as pd
from prettytable import PrettyTable

import environment.datasets as ds
import fdca.fdca as fdca
import fdca.visualisation_new as vi

DATASET_PATH = './datasets/'

def handle_manipulation(df):
    result = df.copy(True)
    # Convert date column to datetime if it exists
    if 'date' in result.columns:
        result['date'] = pd.to_datetime(result['date'])

    print('\nNow you can manipulate the dataframe before applying the FDCA to it.\nType help for available commands.')
    command = None
    while True:
        command = input('> ').split()

        if command[0] == 'help':
            pt = PrettyTable(['Command', 'Description'])
            pt.align['Command'] = 'l'
            pt.align['Description'] = 'l'

            pt.add_row(['end', 'Ends the manipulation step'])
            pt.add_row(['help', 'Prints all available commands'])
            pt.add_row(['reload', 'Reloads the dataframe'])
            pt.add_row(['print {object}', 'Prints the given object. Available objects: df, head, tail, dtypes, columns'])
            pt.add_row(['set_index {column}', 'Sets the given column as index'])
            pt.add_row(['del_column {column...}', 'Deletes the given columns'])
            pt.add_row(['filter_date {start} {end}', 'Filters the dataframe by the given time range. Input datetime as {year}-{month}-{day}-{hour}:{minute}:{second}'])
            pt.add_row(['to_dtype {column} {dtype}', 'Converts the given column to the given dtype.'])

            print(pt)
        elif command[0] == 'set_index':
            try:
                result = result.set_index(command[1])
            except KeyError:
                print('The given column doesn\'t exist')
        elif command[0] == 'del_column':
            try:
                result = result.drop(command[1:], axis=1)
            except:
                print('One of the given columns doesn\'t exist')
        elif command[0] == 'filter_date':
            if 'date' not in result.columns:
                print('This dataframe doesn\'t have a \'date\' column')
                continue
            try:
                result = result[(result['date'] >= command[1]) & (result['date'] <= command[2])]
            except:
                print('Something went wrong during filtering')
        elif command[0] == 'print':
            if len(command) < 2:
                print('Available objects to print:  df, head, tail, dtypes, columns')
                continue

            if command[1] == 'head':
                print(result.head())
            elif command[1] == 'tail':
                print(result.tail())
            elif command[1] == 'dtypes':
                print(result.dtypes)
            elif command[1] == 'columns':
                print(result.columns)
            else:
                print(result)
        elif command[0] == 'to_dtype':
            try:
                result[command[1]] = result[command[1]].astype(command[2])
            except:
                print('Something went wrong during conversion')
        elif command[0] == 'reload':
            result = df.copy(True)
            if 'date' in result.columns:
                result['date'] = pd.to_datetime(result['date'])
        elif command[0] == 'end':
            return result
        else:
            print('Invalid command!')


def get_test_df(df):
    result = df.copy(True)
    result['date'] = pd.to_datetime(result['date'])

    result = result.drop(['cluster', 'lex_source', 'lex_info_class', 'lex_informativeness'], axis=1)
    result = result[(result['date'] >= '2018-09-13') & (result['date'] <= '2018-09-17')]
    result['date'] = result['date'].astype('int64')
    result = result.reset_index(drop=True)

    return result

if __name__ == '__main__':
    print('Loading all available datasets...',flush=True)
    datasets = ds.DatasetManager(DATASET_PATH)
    datasets.info()

    # dataset = None
    # while dataset is None:
    #     name = input('Name of the dataset: ')
    #     dataset = datasets.get_by_name(name)
    dataset = datasets.get_by_name('twitter')

    #df = handle_manipulation(dataset.frame)
    df = get_test_df(dataset.frame)
    print(df)

    tweet_ids = df['tweet_id'].copy(True)
    df = df.drop(['tweet_id'], axis=1)

    parameters = [0,0,0,1]
    # print('Setup parameter types. Type 0 for numeric and 1 for categorical data.')
    # col_index = 0
    # while col_index < len(df.columns):
    #     option = int(input(f'{df.columns[col_index]}: '))
    #     if option in [0,1]:
    #         parameters.append(option)
    #         col_index += 1
    #     else:
    #         print('Invalid option. Please try again.')
    
    try_dc = float(input('Type the dc value to use: '))

    print('Executing FDCA...', flush=True)
    # TODO: Handle output
    result_df, result_centers = fdca.execute(df, parameters, try_dc)
    result_df['date'] = result_df['date'].astype('datetime64[ns]')
    result_df['tweet_id'] = tweet_ids

    result_df.to_csv('fdca_twitter.csv')

    # Plots the data
    vi.plot_3d(result_df, result_centers, "latitude", "longitude", "date")

    # z = fdca.calculate_z(df, parameters, dc_high=0.026)
    print('Success')
