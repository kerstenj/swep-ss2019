from pluginbase import PluginBase
import datasets as ds

DATASET_PATH = '../datasets/'
ALGORITHM_PATH = 'algorithms/'

if __name__ == '__main__':
    print('Loading all available datasets...', end='', flush=True)
    datasets = ds.DatasetManager(DATASET_PATH)
    print('Success')

    print('Loading all available algorithms...', end='', flush=True)
    algorithm_base = PluginBase(package='algorithms')
    algorithm_source = algorithm_base.make_plugin_source(searchpath=[ALGORITHM_PATH], persist=True)

    algorithms = {}
    for algorithm in algorithm_source.list_plugins():
        algorithms[algorithm] = algorithm_source.load_plugin(algorithm)
    print('Success')

    print(f'Executing algorithm: "kmeans_naive"')
    algorithms['kmeans_naive'].execute(
        datasets['iris'].frame,
        3
    )
    #import code; code.interact(local=locals())
