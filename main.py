import environment.datasets as ds
import fdca.fdca as fdca

DATASET_PATH = './datasets/'

if __name__ == '__main__':
    print('Loading all available datasets...',flush=True)
    datasets = ds.DatasetManager(DATASET_PATH)
    datasets.info()

    name = input('Name of dataset: ')
    dataset = datasets.get_by_name(name)

    parameters = []
    df = dataset.frame.copy(True)
    for column in df.columns:
        option = int(input(f'{column}: '))

        if option in [0,1]:
            parameters.append(option)
        elif option == 2:
            del df[column]

    try_dc = float(input('Use dc: '))

    print('Executing FDCA algorithms...', end='', flush=True)
    clusters = fdca.execute(df, parameters, try_dc)
    z = fdca.calculate_z(df, parameters)
    print('Success')

    print(clusters)
    print(z)
