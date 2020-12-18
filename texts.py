import os
import re
from pathlib import Path
from Text_Simi import *

currentpath = os.getcwd()                                        # Returns current path 
# Path to 
sample_paths_gen = Path(currentpath).rglob('sample-texts/*.txt') # Generates paths to any '*.txt' file in given directory
sample_paths     = [str(path) for path in sample_paths_gen]      # Creates the file path for each path from sample_paths_gen
    
test_paths_gen   = Path(currentpath).rglob('text-to-check/*.txt')
test_paths       = [str(path) for path in test_paths_gen]


def Sample_texts():
    return sample_paths

def Check_texts():
    return test_paths

def get_filenames_from_paths(paths, multiple = True):
    filenames = []
    if (multiple):
        for path in paths:
            filenames.append(re.findall("[\w\.]*$", path)[0])
        return filenames
    else:
        return re.findall("[\w\.]*$", paths)[0]

def get_sample_from_index(index):
    f = open(sample_paths[index], 'r', encoding='utf-8', errors='ignore')
    text = f.read()
    f.close()
    return text

def get_text_from_file_name(filename, check=True):
    if check:   # If check is true, that means it's a text 
        f = open(str(Path(currentpath))+'\\text-to-check\\'+filename, 'r', encoding='utf-8', errors='ignore')
    else:
        f = open(str(Path(currentpath))+'\\sample-texts\\'+filename, 'r', encoding='utf-8', errors='ignore')
    text = f.read()
    f.close()
    return text

def get_check_from_index(index):
    f = open(test_paths[index], 'r', encoding='utf-8', errors='ignore')
    text = f.read()
    f.close()
    return text

def getMatchesText(file_text, samples_corpus):
    matches = getMatches(file_text, samples_corpus) 
    matches_text = []
    for i in range(10):
        file_name = get_filenames_from_paths(str(matches[i][1]), multiple = False)
        matches_text.append([matches[i][0], file_name, get_text_from_file_name(file_name, False)])
    return matches_text

Samples_Corpus = sample_corpus_from_path(Sample_texts())   