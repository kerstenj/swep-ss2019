from pluginbase import PluginBase
import datasets

DATASET_PATH = '../datasets/'
ALGORITHM_PATH = 'algorithms/'

if __name__ == '__main__':
    print('Loading all available datasets...', end='', flush=True)
    ds_manager = datasets.DatasetManager(DATASET_PATH)
    print('Success')

    print('Loading all available algorithms...', end='', flush=True)
    algorithm_base = PluginBase(package='testenv.algorithms')
    algorithm_source = algorithm_base.make_plugin_source(search_path=[ALGORITHM_PATH])

    algorithms={}

    for algorithm in algorithm_source.list_plugins():
        print(algorithm)

    print('Success')

    import code; code.interact(local=locals())
