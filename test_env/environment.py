import datasets

DATASET_PATH = '..\\datasets\\'
ALGORITHM_PATH = '..\\algorithms\\'

if __name__ == '__main__':
    print('Loading all datasets from given directory...', end='')
    ds_manager = datasets.DatasetManager(DATASET_PATH)
    print('Success')
    import code; code.interact(local=locals())
