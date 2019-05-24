import pandas as pd
from prettytable import PrettyTable
import os

import help

class Dataset:

    def __init__(self, name, frame, filepath=None):
        self.name = name
        self.frame = frame
        self.filepath = filepath

    @classmethod
    def from_file(cls, filepath):
        name = os.path.splitext(os.path.basename(filepath))[0]
        frame = pd.read_csv(filepath)

        return cls(name, frame, filepath)


class DatasetManager:

    def __init__(self, path):
        self.datasets = {}

        files = help.locate_files_rec(path, 'data')
        self.load_datasets(files)

    def __str__(self):
        pt = PrettyTable(['Name', 'Entries', 'Size in Memory', 'File'])

        pt.align['Name'] = 'l'
        pt.align['Entries'] = 'r'
        pt.align['Size in Memory'] = 'r'
        pt.align['File'] = 'l'

        for _, ds in self.datasets.items():
            pt.add_row([
                ds.name,
                str( len(ds.frame.index) ),
                help.format_size(ds.frame.memory_usage(deep=True).sum()),
                ds.filepath or ''
            ])

        return pt.get_string()

    def __getitem__(self, name):
        return self.get_by_name(name)

    '''
    Returns a list of all Datasets with additional information.
    '''
    def info(self):
        print(self)

    '''
    Returns the dataset with the given name.
    None if it doesn't exist.
    '''
    def get_by_name(self, name):
        return self.datasets.get(name)

    '''
    Returns the dataset associated with the given file.
    None if it doesn't exist.
    '''
    def get_by_file(self, filepath):
        for _, ds in self.datasets.items():
            if ds.file == os.path.realpath(filepath):
                return ds
        return None

    '''
    Loads all given files into this DatasetManager.
    Overrides entries with similar names.
    '''
    def load_datasets(self, files):
        for filepath in files:
            ds = Dataset.from_file(filepath)
            self.datasets[ds.name] = ds

