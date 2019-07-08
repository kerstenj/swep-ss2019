import pandas as pd
from prettytable import PrettyTable

import environment.datasets as ds
import fdca.fdca as fdca
import fdca.visualisation as vi

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
                result = result.reset_index(drop=True)
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
    result = result[(result['date'] >= '2018-09-13') & (result['date'] <= '2018-09-14')]
    result['date'] = result['date'].astype('int64')
    result = result.reset_index(drop=True)

    return result


def find_dc_with_graph(df, parameters):
    repeat = True
    while repeat:
        print('\nWhich parameters should be used to find the dc? Leave input empty to use default value.')
        dc_low = input("start value (default: 0): ")
        dc_high = input("end value (default: 0.2): ")
        step_count = input("number of iterations (default: 200): ")

        if dc_low == '':
            dc_low = 0

        if dc_high == '':
            dc_high = 0.2

        if step_count == '':
            step_count = 200

        print('\nExecuting FDCA...', flush=True)

        dc_z_map = fdca.calculate_z(df, parameters, dc_low=float(dc_low), dc_high=float(dc_high), step_count=int(step_count))
        vi.plot_line(dc_z_map)

        print('Success\n')

        while True:
            prompt = input('Do you want to try other parameters? [y/n] ')

            if prompt == 'y':
                break
            elif prompt == 'n':
                repeat = False
                break
            else:
                print('Invalid input!')


def use_dc_for_clustering(df, parameters):
    try_dc = float(input('Type the dc value to use: '))

    print('\nExecuting FDCA...', flush=True)
    # TODO: Handle output
    result_df, result_centers = fdca.execute(df, parameters, try_dc)
    result_df['date'] = result_df['date'].astype('datetime64[ns]')
    result_df['tweet_id'] = tweet_ids

    result_df.to_csv('fdca_twitter.csv')

    print('Success')

    repeat = True
    while repeat:
        print('\nHow do you want to plot your data?')

        pt = PrettyTable(['Method', 'Description'])
        pt.align['Method'] = 'l'
        pt.align['Description'] = 'l'

        pt.add_row(['0', 'Plots all data points in a two-dimensional coordinate system and colors them by cluster.'])
        pt.add_row(['1', 'Work in progress. Do not use!'])
        pt.add_row(['2', 'Plots all data points in a three-dimensional coordinate system and colors them by cluster.'])
        pt.add_row(['3', 'Can be used to show the number of tweet in the clusters over time.\nPlots only the cluster centers in a three-dimensional coordinate system and resizes them depending on the number of tweets in that cluster.\nThe values get split in intervals on the z-axis.'])
        pt.add_row(['4', 'Plots a bar chart with one bar per cluster center and colored parts for different classes/categories.'])

        print(pt)

        command = None
        while True:
            command = input('> ')

            if command == '0':
                print('\nWhich parameters should be used for the plot?')
                xaxis = input("x-axis: ")
                yaxis = input("y-axis: ")

                try:
                    vi.plot_2d(result_df, result_centers, xaxis, yaxis)
                except:
                    print('\nSomething went wrong during plotting.')

                break
            elif command == "1":
                print('Invalid command!')
            elif command == "2":
                print('\nWhich parameters should be used for the plot?')
                xaxis = input("x-axis: ")
                yaxis = input("y-axis: ")
                zaxis = input("z-axis: ")

                try:
                    vi.plot_3d(result_df, result_centers, xaxis, yaxis, zaxis)
                except:
                    print('\nSomething went wrong during plotting.')

                break
            elif command == "3":
                print('\nWhich parameters should be used for the plot? Leave input empty to use default value.')
                xaxis = input("x-axis: ")
                yaxis = input("y-axis: ")
                zaxis = input("z-axis: ")
                steps = input("number of intervalls (default: 200): ")

                try:
                    if steps != '':
                        vi.plot_x_y_date(result_df, result_centers, xaxis, yaxis, zaxis, int(steps))
                    else:
                        vi.plot_x_y_date(result_df, result_centers, xaxis, yaxis, zaxis)
                except:
                    print('\nSomething went wrong during plotting.')

                break
            elif command == "4":
                print('\nWhich parameters should be used for the plot?')
                class_column = input("class column (e.g. lex_info_class): ")

                try:
                    vi.plot_class_bars(result_df, result_centers, class_column)
                except:
                    print('\nSomething went wrong during plotting.')

                break
            else:
                print('Invalid command!')

        while True:
            prompt = input('\nDo you want to do another plot? [y/n] ')

            if prompt == 'y':
                break
            elif prompt == 'n':
                repeat = False
                break
            else:
                print('Invalid input!')


if __name__ == '__main__':
    print('Loading all available datasets...',flush=True)
    datasets = ds.DatasetManager(DATASET_PATH)
    datasets.info()

    dataset = None
    while dataset is None:
        name = input('Name of the dataset: ')
        dataset = datasets.get_by_name(name)
    # dataset = datasets.get_by_name('twitter')

    df = handle_manipulation(dataset.frame)
    # df = get_test_df(dataset.frame)
    # print(df)

    tweet_ids = df['tweet_id'].copy(True)
    df = df.drop(['tweet_id'], axis=1)

    # parameters = [0,0,0,1]
    print('Setup parameter types. Type 0 for numeric and 1 for categorical data.')
    parameters = []
    col_index = 0
    while col_index < len(df.columns):
        option = int(input(f'{df.columns[col_index]}: '))
        if option in [0,1]:
            parameters.append(option)
            col_index += 1
        else:
            print('Invalid option. Please try again.')

    # Ask user if he wants to cluster with a fixed dc or find the dc with z
    print("\nWhat do you want to do?")

    pt = PrettyTable(['Utility', 'Description'])
    pt.align['Utility'] = 'l'
    pt.align['Description'] = 'l'

    pt.add_row(['find_dc', 'Use a diagramm of different z and dc values to find the best dc.'])
    pt.add_row(['use_dc', 'Use a specific dc value to cluster the data and plot the clustered points.'])

    print(pt)

    command = None
    while(True):
        command = input('> ')

        if command == 'find_dc':
            find_dc_with_graph(df, parameters)
            break
        elif command == "use_dc":
            use_dc_for_clustering(df, parameters)
            break
        else:
            print('Invalid command!')
