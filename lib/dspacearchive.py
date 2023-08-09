"""
This class handles the creation of a DSpace simple archive suitable for import into a dspace repository. 

See: http://www.dspace.org/1_6_2Documentation/ch08.html#N15B5D for more information about the DSpace 
Simple Archive format. 
"""

import os
import pandas as pd
from .itemfactory import ItemFactory
from shutil import copy

class DspaceArchive:

    """
    Constructor:

    The constructor takes a path to a csv file. 
    It then parses the file, creates items, and adds the items to the archive.  
    """
    def __init__(self, input_path):
        self.items = []
        
        self.input_path = input_path
        self.input_base_path = os.path.dirname(input_path)

        df_csv = pd.read_csv(self.input_path, sep=';', encoding="utf-8", dtype=str)
        self.groups = df_csv['lote_load'].to_list()
        df_csv.drop('lote_load', axis=1, inplace=True)

        item_factory = ItemFactory(df_csv.columns.tolist())
        for index in range(len(df_csv)):
            item = item_factory.newItem(df_csv.iloc[index].to_list())
            self.addItem(item)

    """
    Add an item to the archive. 
    """
    def addItem(self, item):
        self.items.append(item)

    """
    Get an item from the archive.
    """
    def getItem(self, index):
        return self.items[index]
    
    """
    Get groups from the archive.
    """
    def getGroups(self):
        return self.groups

    """
    Write the archie to disk in the format specified by the DSpace Simple Archive format.
    See: http://www.dspace.org/1_6_2Documentation/ch08.html#N15B5D
    """
    def write(self, items, dir = "."):

        self.create_directory(dir)
        for index, item in enumerate(items):
            #item directory
            name = str(int(index) + 1)
            item_path = os.path.join(dir, name)
            self.create_directory(item_path)

            #contents file
            self.writeContentsFile(item, item_path)

            #content files (aka bitstreams)
            self.copyFiles(item, item_path)

            #Metadata file
            self.writeMetadata(item, item_path)

    """
    Create a zip file of the archive. 
    """
    def zip(self, dir = None):
        pass

    """
    Create a directory if it doesn't already exist.
    """
    def create_directory(self, path):
        if not os.path.isdir(path):
            os.makedirs(path)

    """
    Create a contents file that contains a lits of bitstreams, one per line. 
    """
    def writeContentsFile(self, item, item_path):
        contents_file = open(os.path.join(item_path, 'contents'), "w")

        files = item.getFiles()
        for index, file_name in enumerate(files):
            contents_file.write(file_name)
            if index < len(files):
                contents_file.write("\n")

        contents_file.close()

    """
    Copy the files that are referenced by an item to the item directory in the DSPace simple archive. 
    """
    def copyFiles(self, item, item_path):
        files = item.getFilePaths()
        for index, file_name in enumerate(files):
            copy(os.path.join(self.input_base_path, file_name), item_path)

    def writeMetadata(self, item, item_path):
        xml = item.toXML()

        metadata_file = open(os.path.join(item_path, 'dublin_core.xml'), "w", encoding="utf-8")
        metadata_file.write(xml)
        metadata_file.close()
