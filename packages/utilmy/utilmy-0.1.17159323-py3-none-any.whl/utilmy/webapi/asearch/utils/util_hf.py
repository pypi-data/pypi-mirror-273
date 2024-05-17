# -*- coding: utf-8 -*-
""" Hugging Face utilities
    #### Install
        cd myutil 
        cd utilmy/webapi/asearch/
        pip install -r pip/py39_full.txt
        pip install fastembed==0.2.6 loguru --no-deps


    #### ENV variables
        export HF_TOKEN=


"""
import warnings
warnings.filterwarnings("ignore")
import os, pathlib, uuid, time, traceback, copy, json
from box import (Box, BoxList,  )
from typing import Any, Callable, Dict, List, Optional, Sequence, Union
import pandas as pd, numpy as np, torch
import mmh3, xxhash

import datasets
from datasets import Dataset, DatasetDict

from utilmy import (pd_read_file, os_makedirs, pd_to_file, date_now, glob_glob,
       json_load, json_save)
from utilmy import log, log2


#######################################################################################
def test_hf_dataset_to_parquet():
    """test function for converting Hugging Face datasets to Parquet files"""
    name = "ag_news"
    splits = ["train", "test"]
    dirtmp = "./ztmp/details/"
    ds_to_file(name, dirout=dirtmp, splits=splits)
    # read  parquet files
    for split in splits:
        assert os.path.exists(f"{dirtmp}/{name}_{split}.parquet")
        # pd = pd_read_file(f"hf_datasets/{dataset_name}_{split}.parquet")
        # print(pd.columns)



#######################################################################################
def ds_to_file(ds:DatasetDict, dirout:str, fmt="json", show:int=0)->None:
   """Writes  datasets to files in  specified directory after creating subdirectories for each key in  dataset. 

   Args:
       ds (dict): A dictionary containing  dataset.
       dirout (str):  output directory path.
       show (int): Flag to indicate whether to show additional information. Defaults to 0.

   Returns:
       None
   """
   for key in ds.keys():  ### "train", "test"
       dirout1 = f"{dirout}/{key}/" 
       os_makedirs(dirout1) 
       log(dirout1)
       ds[key].info.write_to_directory(f"{dirout1}/", )

       if fmt == "parquet":
          ds[key].to_parquet(f"{dirout1}/df.{fmt}", )


def ds_read_file(dirin:str, fmt="parquet")->DatasetDict:
    """Reads files from a specified directory,returns a DatasetDict.
    dsdict = ds_read_file(dirout +"/ztest")

    Args:
        dirin (str):  input directory path.
        format (str):  file format to read. Defaults to "parquet".

    Returns:
        DatasetDict: A dictionary containing datasets processed from  input files.
    """

    dirin= dirin[:-1] if dirin[-1] == "/" else dirin
    dirin= dirin.replace("//","/") if ":" not in dirin else dirin 

    dsdict = DatasetDict()

    from utilmy import glob_glob
    fpaths = glob_glob(f"{dirin}/*" )

    for fp in fpaths:     
       key = fp.split("/")[-1]
       if "." in key : continue  #### Path of a file

       flist = glob_glob(fp + f"/*.{fmt}")
       if flist is None or len(flist)<1:
           continue 
       log(flist[-1], len(flist))
       dsdict[key] = Dataset.from_parquet(flist)

    return dsdict




#######################################################################################
def hf_ds_to_parquet(name="ag_news", dirout: str = ".ztmp/hf_online/", splits: list = None, 
     cols_mapping: dict = None
):
    """Converts a Hugging Face dataset to a Parquet file.
    Args:
        dataset_name (str):  name of  dataset.
        dirout (str):  output directory.
        mapping (dict):  mapping of  column names. Defaults to None.
    """
    dataset = datasets.load_dataset(name)
    # print(dataset)
    if splits is None:
        splits = dataset.keys()

    for key in splits:
        df = pd.DataFrame(dataset[key])
        log(df.shape)
        if cols_mapping is not None:
            df = df.rename(columns=cols_mapping)

        dirfile = f"{dirout}/{name}/{key}/df.parquet"
        pd_to_file(df, dirfile)


def hf_ds_meta(dataset:Dataset=None, meta=None, dirout:str=None):
   """Generates metadata for a dataset based on  input dataset, metadata, and output directory.
   Args:
       dataset (Dataset, optional):  input dataset. Defaults to None.
       meta (dict):  metadata to be updated. If not provided, a new one with an empty "split" key is created. Defaults to None.
       dirout (str):  output directory to save  metadata JSON file. Defaults to None.

   Returns:
       dict:  updated metadata with information about each split and a list of splits.

   """
   meta = { "split": [] }  if meta is None else meta
   for split in dataset.keys():  ### Train
      meta[split] = dict( dataset[split].info)
      meta["split"].append(split    )

   if isinstance(dirout, str):
     json_save(meta, dirout + "/meta.json")

   return meta



def hf_ds_meta_todict_v2(dataset=None, metadata=None):
   metadata = { "split": [] } 
   for split in dataset.keys():  ### Train
      ##### Convert metadata to dictionary
      mdict = {key: value for key, value in dataset[split].info.__dict__.items()}
      metadata[split] = mdict
      metadata["split"].append(split)

   return metadata   




def hf_dataset_search():
    from huggingface_hub import HfApi, DatasetFilter
    api = HfApi()

    # Create a filter for English text classification datasets
    filter = DatasetFilter(
        task_categories=["text-classification"],
        languages=["en"]
    )

    # List datasets based on  filter
    datasets = api.list_datasets(filter=filter)
    print(datasets)





#######################################################################################
######## utils  #######################################################################
def hash_textid(xstr:str, n_chars=1000, seed=123)->int:
  """ Computes  xxhash value: Unique ID of a text.
  
  Args:
      xstr (str):  input string.
      n_chars (int): Maximum number of characters to consider for hashing. Defaults to 1000.
      seed (int): Seed value for xxhash. Defaults to 123.
  
  Returns:
      int:  xxhash value calculated based on  input string.
  """
  import xxhash  
  return xxhash.xxh64_intdigest(str(xstr)[:n_chars], seed=seed) - len(xstr)



def hash_text_minhash(text:str, sep=" ", ksize:int=None, n_hashes:int=4)->np.array:
    """Computes  MinHash hash values for  given text using  specified ksize and number of hashes.
       Args:
          text (str):  input text to hash.
          ksize (int):  size of  k-mer to use for hashing, defaults to 4.
          n_hashes (int):  number of hashes to use, defaults to 2.

    Example:
       hash_text_minhash("my very long string text ", n_hashes=4)
       ### array([1136865025,  675357709,  253868148, 1471015800]

       hash_text_minhash("my very very small string text almost equal "
       ### [594334164, 675357709, 253868148, 921427594], dtype=uint64)

    """
    from datasketch import MinHash
    m = MinHash(num_perm=n_hashes)

    if ksize is None :
        for token in text.split(sep):
            m.update(token.encode('utf8'))
    else:
        for k in range(0,  1+ len(text)// ksize ):
            m.update(text[k*ksize: (k+1)*ksize ].encode('utf8'))

    return m.hashvalues


def hash_mmh64(xstr: str) -> int:
    # pylint: disable=E1136
    return mmh3.hash64(str(xstr), signed=False)[0]


def uuid_int64():
    """## 64 bits integer UUID : global unique"""
    return uuid.uuid4().int & ((1 << 64) - 1)


###################################################################################
def box_to_dict(box_obj):

    from box import (Box, BoxList,  )
    if isinstance(box_obj, Box):
        box_obj = {k: box_to_dict(v) for k, v in box_obj.items()}

    elif isinstance(box_obj, dict):
        return {k: box_to_dict(v) for k, v in box_obj.items()}
    elif isinstance(box_obj, list):
        return [box_to_dict(v) for v in box_obj]

    return str(box_obj) 


def np_str(v):
    return np.array([str(xi) for xi in v])

def np_jaccard_sim(hashes1, hashes2):
    set2 = set(hashes2)
    intersection = 0
    union        = len(hashes1)
    for x in hashes1:
        if x in set2:
            intersection += 1
        else : 
            union += 1
            
    return intersection / union


###################################################################################
###################################################################################
def dataset_kaggle_to_parquet(name, dirout: str = "./ztmp/kaggle/", 
     mapping: dict = None, overwrite=False):
    """Converts a Kaggle dataset to a Parquet file.
    Args:
        dataset_name (str):  name of  dataset.
        dirout (str):  output directory.
        mapping (dict):  mapping of  column names. Defaults to None.
        overwrite (bool, optional):  whether to overwrite existing files. Defaults to False.
    """
    import kaggle
    # download dataset and decompress
    kaggle.api.dataset_download_files(name, path=dirout, unzip=True)

    df = pd_read_file(dirout + "/**/*.csv", npool=4)
    if mapping is not None:
        df = df.rename(columns=mapping)

    pd_to_file(df, dirout + f"/{name}/parquet/df.parquet")




##########################################################################
def pd_to_file_split(df, dirout, ksize=1000):
    kmax = int(len(df) // ksize) + 1
    for k in range(0, kmax):
        log(k, ksize)
        dirout = f"{dirout}/df_{k}.parquet"
        pd_to_file(df.iloc[k * ksize : (k + 1) * ksize, :], dirout, show=0)



def pd_check_ram_usage(df):
    # Determine  proper batch size
    min_batch_size = 1000
    max_batch_size = 100000
    test_df = df.iloc[:10, :]
    test_memory_mb = test_df.memory_usage(deep=True).sum() / (1024 * 1024)
    log("first 10 rows memory size: ", test_memory_mb)
    batch_size = min (max( int(1024 * 10 // test_memory_mb // 1000 * 1000 ), min_batch_size ), max_batch_size)


def pd_fake_data(nrows=1000, dirout=None, overwrite=False, reuse=True) -> pd.DataFrame:
    from faker import Faker

    if os.path.exists(str(dirout)) and reuse:
        log("Loading from disk")
        df = pd_read_file(dirout)
        return df

    fake = Faker()
    dtunix = date_now(returnval="unix")
    df = pd.DataFrame()

    ##### id is integer64bits
    df["id"] = [uuid_int64() for i in range(nrows)]
    df["dt"] = [int(dtunix) for i in range(nrows)]

    df["title"] = [fake.name() for i in range(nrows)]
    df["body"] = [fake.text() for i in range(nrows)]
    df["cat1"] = np_str(np.random.randint(0, 10, nrows))
    df["cat2"] = np_str(np.random.randint(0, 50, nrows))
    df["cat3"] = np_str(np.random.randint(0, 100, nrows))
    df["cat4"] = np_str(np.random.randint(0, 200, nrows))
    df["cat5"] = np_str(np.random.randint(0, 500, nrows))

    if dirout is not None:
        if not os.path.exists(dirout) or overwrite:
            pd_to_file(df, dirout, show=1)

    log(df.head(1), df.shape)
    return df


def pd_fake_data_batch(nrows=1000, dirout=None, nfile=1, overwrite=False) -> None:
    """Generate a batch of fake data and save it to Parquet files.

    python engine.py  pd_fake_data_batch --nrows 100000  dirout='ztmp/files/'  --nfile 10

    """

    for i in range(0, nfile):
        dirouti = f"{dirout}/df_text_{i}.parquet"
        pd_fake_data(nrows=nrows, dirout=dirouti, overwrite=overwrite)


###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()



