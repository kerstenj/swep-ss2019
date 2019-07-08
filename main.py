import pandas as pd
from prettytable import PrettyTable

import environment.datasets as ds
import fdca.fdca as fdca

DATASET_PATH = './datasets/'

def handle_manipulation(df):
    df = df.copy(True)
    # Convert date column to datetime if it exists
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])

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
            pt.add_row(['print', 'Prints the current dataframe'])
            pt.add_row(['dtypes', 'Prints the datatypes of all columns'])
            pt.add_row(['set_index {column}', 'Sets the given column as index'])
            pt.add_row(['del_column', 'Deletes the given columns'])
            pt.add_row(['del_column {column...}', 'Deletes the given columns'])
            pt.add_row(['filter_date {start} {end}', 'Filters the dataframe by the given time range. Input datetime as {year}-{month}-{day}-{hour}:{minute}:{second}'])
            pt.add_row(['to_dtype {column} {dtype}', 'Converts the given column to the given dtype.'])

            print(pt)
        elif command[0] == 'set_index':
            try:
                df = df.set_index(command[1])
            except KeyError:
                print('The given column doesn\'t exist')
        elif command[0] == 'del_column':
            try:
                df = df.drop(command[1:], axis=1)
            except:
                print('One of the given columns doesn\'t exist')
        elif command[0] == 'filter_date':
            if 'date' not in df.columns:
                print('This dataframe doesn\'t have a \'date\' column')
                continue
            try:
                df = df[(df['date'] >= command[1]) & (df['date'] <= command[2])]
            except:
                print('Something went wrong during filtering')
        elif command[0] == 'dtypes':
            print(df.dtypes)
        elif command[0] == 'print':
            print(df)
        elif command[0] == 'to_dtype':
            try:
                df[command[1]] = df[command[1]].astype(command[2])
            except:
                print('Something went wrong during conversion')
        elif command[0] == 'end':
            return df
        else:
            print('Invalid command!')


if __name__ == '__main__':
    print('Loading all available datasets...',flush=True)
    datasets = ds.DatasetManager(DATASET_PATH)
    datasets.info()

    dataset = None
    while dataset is None:
        name = input('Name of the dataset: ')
        dataset = datasets.get_by_name(name)

    df = handle_manipulation(dataset.frame)

    parameters = []
    print('Setup parameter types. Type 0 for numeric and 1 for categorical data.')
    col_index = 0
    while col_index < len(df.columns):
        option = int(input(f'{df.columns[col_index]}: '))
        if option in [0,1]:
            parameters.append(option)
            col_index += 1
        else:
            print('Invalid option. Please try again.')
    
    try_dc = float(input('Type the dc value to use: '))

    print('Executing FDCA...', flush=True)
    # TODO: Handle output
    clusters = fdca.execute(df, parameters, try_dc)
    z = fdca.calculate_z(df, parameters)
    print('Success')

    print(clusters)
    print(z)
