# -*- coding: utf-8 -*-
"""
    #### Install
        cd myutil 
        cd utilmy/webapi/asearch/
        pip install -r pip/py39_full.txt
        pip install fastembed==0.2.6 loguru --no-deps


    #### ENV variables
        export HF_TOKEN=
]

    ##### Usage : 
            cd utilmy/webapi/asearch/
            mkdir -p ./ztmp

            python data.py run_convert --name "ag_news"  --diroot  "./ztmp/hf_datasets/"   


    #### Folder structure
       cd aseearch
       mkdir -p ztmp/hf_dataset/      ### already in gitignore, never be commited. 

      ztmp/hf_dataset/
            data/ ashraq_financial_news_articles / df_50k.parquet

            meta/ 
               ashraq_financial_news_articles.json
               agnews.json

            



    ##### Flow
        HFace Or Kaggle --> dataset in RAM--> parquet (ie same columns)  -->  parquet new columns (final)
        Example :   
             huggingface.co/datasets/valurank/News_Articles_Categorization
             {name}-{dataset_name}

              ### MetaData JSON saved here
                       ---> ztmp/hf_data/meta/valurank-News_Articles_Categorization.json"

              ### Data saved here:
                       ---> ztmp/hf_data/data/valurank-News_Articles_Categorization/train/df.parquet"
                       ---> ztmp/hf_data/data/valurank-News_Articles_Categorization/test/df.parquet"



       Target Schema is  SCHEMA_GLOBAL_v1 



    #### Dataset TODO:

        https://huggingface.co/datasets/ashraq/financial-news-articles

        https://huggingface.co/datasets/big_patent

        https://huggingface.co/datasets/cnn_dailymail



    ### Dataset Done
        https://huggingface.co/datasets/ag_news


    #### Dataset Done in Google Drtice
       https://drive.google.com/drive/folders/1Ggzl--7v8xUhxr8a8zpRtgh2fI9EXxoG?usp=sharing



    ##### Infos
        https://huggingface.co/datasets/big_patent/tree/refs%2Fconvert%2Fparquet/a/partial-train

        https://zenn.dev/kun432/scraps/1356729a3608d6



    ### Tools: Annotation tool
        https://doccano.github.io/doccano/

        https://github.com/argilla-io/argilla   


        https://diffgram.readme.io/docs/conversational-annotation

        Prodigy: A scriptable annotation tool from the creators of spaCy, designed for efficient, active learning-based annotation. It supports various data types including text, images, and audio 2.
        brat (Browser-Based Rapid Annotation Tool): A free, web-based tool for collaborative text annotation, supporting complex configurations and integration with external resources 2.
        tagtog: An easy-to-use, web-based text annotation tool that supports manual and automatic annotation, with features for training models and importing/exporting annotated data 2.
        LightTag: Offers a browser-based platform with AI-driven suggestions for text labeling and features for managing annotation projects and quality control 2.
        TagEditor: A desktop application that integrates with spaCy for annotating text, supporting various annotation types and data export options for model training 2.



"""
import warnings
warnings.filterwarnings("ignore")
import os, pathlib, uuid, time, traceback, copy, json
from box import (Box, BoxList,  )
from typing import Any, Callable, Dict, List, Optional, Sequence, Union
import pandas as pd, numpy as np, torch
import mmh3

import datasets

from utilmy import (pd_read_file, os_makedirs, pd_to_file, date_now, glob_glob,
       json_load, json_save)
from utilmy import log, log2


######################################################################################
#### All dataset has normalized columns : simplify training
SCHEMA_GLOBAL_v1 = [
    ("id_global",  "int64", "global unique ID"),
    ("id_dataset", "int64", "global unique ID of the dataset"),

    ("id_local", "int64", "local ID"),
    ("dt", "float64", "Unix timestamps"),

    ("title", "str", " Title "),
    ("summary", "str", " Summary "),
    ("body", "str", " Summary "),
    ("info_json", "str", " Extra info in JSON string format "),

    ("cat1", "str", " Category 1 or label "),
    ("cat2", "str", " Category 2 or label "),
    ("cat3", "str", " Category 3 or label "),
    ("cat4", "str", " Category 4 or label "),
    ("cat5", "str", " Category 5 or label "),
]



#### JSON saved on in  dirdata_meta/
meta_json =Box({
  "name"             : "str",
  "name_unique"      : "str",
  "url"              : "str",
  "nrows"            : "int64",
  "columns"          : "list",
  "columns_computed" : "list",  ### Computed columns from original
  "lang"             : "list",  ## list of languages
  "description_full" : "str",
  "description_short": "str",
  "tasks"            : "list",  ## List of tasks
  "info_json"        : "str",   ## JSON String to store more infos
  "dt_update"        : "int64", ## unix

})


####################################################################################
def run_convert(name="ag_news", diroot: str = "./ztmp/hf_datasets", 
                splits: list = None, schema_fun: str = None,
                batch_size: int = 50000,
                kmax:int=1
):
    """Converts a Hugging Face dataset to a Parquet file + JSON File
        Args:
            dataset_name (str):  name of  dataset.
            dirout (str):  output directory.

        python data.py run_convert --name "ag_news"  --diroot  "./ztmp/hf_datasets/"   

        DatasetDict({
            train: Dataset({
                features: ['text', 'label'],
                num_rows: 120000
            })
            test: Dataset({
                features: ['text', 'label'],
                num_rows: 7600
            })
        })

        100 dataset

        if ...


    """
    cc = Box( copy.deepcopy(meta_json))
    name2 = name.replace("/","_").replace("-","_")
    cc.name        = name
    cc.name_unique = name2


    ### "ashraq/financial-news-articles"  -->  "ashraq_financial_news_articles"
    log("\n##### Schema function loader ") 
    if schema_fun is None: 
        schema_fun_name  = f"schema_{name2}"
    
    convert_fun = globals()[ schema_fun_name ]  #load_function_uri(f"data.py:{schema_fun}")
    log(convert_fun) ### check
    
  
    log("\n###### Loading dataset ")
    version = None
    if name == "cnn_dailymail":  version =  "3.0.0"


    dataset = datasets.load_dataset(name, version,  streaming=False) 
    splits      = [ key for key in dataset.keys() ] 
    cc.metadata = hf_dataset_meta_todict(dataset)

    log("\n###### Convert dataset into ", diroot)
    nrows=0
    
    for key in splits:
        len_df  = len(dataset[key])
        n_batch = (len_df + batch_size - 1) // batch_size  
        
        for k in range(0, n_batch):
            if k > kmax : break
            data_k = dataset[key][k * batch_size: (k + 1) * batch_size]
            
            dfk = pd.DataFrame(data_k)
            dfk = convert_fun(dfk, meta_dict=cc)  # Assuming convert_fun is defined elsewhere

            log(list(dfk.columns), dfk.shape)
            nrows += len(dfk)
            dirout = f"{diroot}/data/{name2}/{key}/df_{k}.parquet"
            pd_to_file(dfk, dirout, show=1) 

    log("\n##### meta.json  ")
    cc.dt_update = date_now(fmt="%Y%m%d %H:%M:%S",  returnval="str")
    cc.url       = f"https://huggingface.co/datasets/{name}"
    cc.nrows     = nrows
    cc.columns   = list(dfk.columns)
    cc2 = box_to_dict(cc)
    log(cc2)
    json_save(cc2, f"{diroot}/meta/{name2}.json")



def run_convert_bigdata(name="ag_news", version:str=None, diroot: str = "./ztmp/hf_datasets", 
                splits: list = None, schema_fun: str = None,
                batch_size: int = 50000,
                kmax:int=1
):
    """Converts a Hugging Face dataset to a Parquet file + JSON File
    Args:
        dataset_name (str):  name of  dataset.
        dirout (str):  output directory.

        # Replace 'dataset_name' with the name of the dataset you want to download
dataset = load_dataset('dataset_name', download_mode='force_redownload')

     python data.py run_convert --name "ag_news"  --diroot  "./ztmp/hf_datasets/"   

    DatasetDict({
        train: Dataset({
            features: ['text', 'label'],
            num_rows: 120000
        })
        test: Dataset({
            features: ['text', 'label'],
            num_rows: 7600
        })
    })

    """
    cc = Box( copy.deepcopy(meta_json))
    ### "ashraq/financial-news-articles"  -->  "ashraq_financial_news_articles"
    name2 = name.replace("/","_").replace("-","_")
    cc.name        = name
    cc.name_unique = name2


    log("#### Schema function loader ") 
    if schema_fun is None: 
        schema_fun_name  = f"schema_{name2}"
    
    convert_fun = globals()[ schema_fun_name ]  #load_function_uri(f"data.py:{schema_fun}")
    log(convert_fun) ### check
    
  
    log("###### Loading dataset ")
    version = None
    if name == "cnn_dailymail":  version =  "3.0.0"
    
    metadata = datasets.load_dataset(name, version, split=None, streaming=True)
    print(metadata)

    splits      = [ key for key in metadata.keys() ] 
    # cc.metadata = hf_dataset_meta_todict(dataset)
    # cc.metadata = metadata

    log("###### Convert dataset into ", diroot)
    nrows=0
    
    for key in splits:
        dataset = datasets.load_dataset(name, split=key,  streaming=True) 

        data_k = []; nitem = 0; k = 0
        for item in dataset:
            if k > kmax : break
            if nitem == batch_size:
                dfk = pd.DataFrame(data_k)
                dfk = convert_fun(dfk, meta_dict=cc)  # Assuming convert_fun is defined elsewhere

                log(list(dfk.columns), dfk.shape)
                nrows += len(dfk)
                dirout = f"{diroot}/data/{name2}/{key}/df_{k}.parquet"
                pd_to_file(dfk, dirout, show=1) 
                data_k = []; k = k + 1; nitem = 0
            data_k.append(item)
            nitem = nitem + 1

    log("##### meta.json  ")
    cc.dt_update = date_now(fmt="%Y%m%d %H:%M:%S",  returnval="str")
    cc.url       = f"https://huggingface.co/datasets/{name}"
    cc.nrows     = nrows
    cc.columns   = list(dfk.columns)
    cc2 = box_to_dict(cc)
    log(cc2)
    json_save(cc2, f"{diroot}/meta/{name2}.json")



def pd_check_ram_usage(df):
    # Determine the proper batch size
    min_batch_size = 1000
    max_batch_size = 100000
    test_df = df.iloc[:10, :]
    test_memory_mb = test_df.memory_usage(deep=True).sum() / (1024 * 1024)
    log("first 10 rows memory size: ", test_memory_mb)
    batch_size = min (max( int(1024 * 10 // test_memory_mb // 1000 * 1000 ), min_batch_size ), max_batch_size)



def box_to_dict(box_obj):

    from box import (Box, BoxList,  )
    if isinstance(box_obj, Box):
        box_obj = {k: box_to_dict(v) for k, v in box_obj.items()}

    elif isinstance(box_obj, dict):
        return {k: box_to_dict(v) for k, v in box_obj.items()}
    elif isinstance(box_obj, list):
        return [box_to_dict(v) for v in box_obj]

    return str(box_obj) 


def hf_dataset_meta_todict(dataset=None, metadata=None):
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

    # List datasets based on the filter
    datasets = api.list_datasets(filter=filter)
    print(datasets)





#######################################################################################
######## Custom Schema ################################################################

def schema_cnn_dailymail(df:pd.DataFrame, meta_dict:dict=None) -> pd.DataFrame:
    """ Convert  cnn_dailymail
    Docs:

        https://huggingface.co/datasets/cnn_dailymail

    
        rows: 312k , size: 2.5 GB
        article:  str, article
        highlights: str, highlights
        id: str, id
    
    """
    cols0 = ["article", "highlights", "id"]
    log(df[cols0].shape)

    #### Taget columns
    n     = len(df)
    dtymd = date_now(fmt="%Y%M%D",  returnval="str")
    url   = meta_dict["url"]

    df["id_global"]  = [uuid_int64() for i in range(n)]
    df["id_dataset"] = url
    df["dt"]         = dtymd
    df["id_local"]   = -1


    ###### Custom mapping ###########################
    df["title"]     = df["article"].apply(lambda x: " ".join(x.split(" ")[:15]) )
    df["summary"]   = df["highlights"]; del df["highlights"]
    df["body"]      = df["article"]  ; del df["article"]

    ### Other data columns not includeds
    df["info_json"] = df.apply(lambda x: json.dumps({"id": x["id"]}), axis=1)
    df["cat1"]      = ""
    df["cat2"]      = ""
    df["cat3"]      = ""
    df["cat4"]      = ""
    df["cat5"]      = ""

    cols1 = [x[0] for x in  SCHEMA_GLOBAL_v1 ] 
    df = df[cols1]
    return df


def schema_big_patent(df:pd.DataFrame, meta_dict:dict=None) -> pd.DataFrame:
    """ Convert  big_patent
    Docs:

        https://huggingface.co/datasets/big_patent

    
        rows: 173k , size: 17.9 GB
        description:  str, description
        abstract: str, abstract
    
    """
    cols0 = ["description", "abstract"]
    log(df[cols0].shape)

    #### Taget columns
    n     = len(df)
    dtymd = date_now(fmt="%Y%M%D",  returnval="str")
    url   = meta_dict["url"]

    df["id_global"]  = [uuid_int64() for i in range(n)]
    df["id_dataset"] = url
    df["dt"]         = dtymd
    df["id_local"]   = -1

    ###### Custom mapping ###########################
    df["title"]     = df["description"].apply(lambda x: " ".join(x.split(" ")[:15]) )
    df["summary"]   = df["abstract"];      del df["abstract"]
    df["body"]      = df["description"]  ; del df["description"]
    
    ### Other data columns not includeds
    df["info_json"] = df.apply(lambda x: json.dumps({}), axis=1)
    df["cat1"]      = ""
    df["cat2"]      = ""
    df["cat3"]      = ""
    df["cat4"]      = ""
    df["cat5"]      = ""

    cols1 = [x[0] for x in  SCHEMA_GLOBAL_v1 ] 
    df = df[cols1]
    return df


def schema_ashraq_financial_news_articles(df:pd.DataFrame, meta_dict:dict=None) -> pd.DataFrame:

    """ Convert  ashraq/financial-news-articles 
    Docs:

        https://huggingface.co/datasets/ashraq/financial-news-articles

    
        rows: 306k , size: 492 MB
        title:  str, title
        text: str, text
        url: str, url
    
    """
    cols0 = ["title", "text", "url"]
    log(df[cols0].shape)

    #### Taget columns
    n     = len(df)
    dtymd = date_now(fmt="%Y%M%D",  returnval="str")
    url   = meta_dict["url"]

    df["id_global"]  = [uuid_int64() for i in range(n)]
    df["id_dataset"] = url
    df["dt"]         = dtymd
    df["id_local"]   = -1


    ###### Custom mapping ###########################
    df["title"]     = df["title"]
    df["summary"]   = ""
    df["body"]      = df["text"]  ; del df["text"]

    ### Other data columns not includeds
    df["info_json"] = df.apply(lambda x: json.dumps({"url": x["url"]}), axis=1)
    df["cat1"]      = ""
    df["cat2"]      = ""
    df["cat3"]      = ""
    df["cat4"]      = ""
    df["cat5"]      = ""

    cols1 = [x[0] for x in  SCHEMA_GLOBAL_v1 ] 
    df = df[cols1]
    return df


def schema_ag_news(df:pd.DataFrame, meta_dict:dict=None) -> pd.DataFrame:
    """ Convert  ag_news 
    Docs:

        https://huggingface.co/datasets/ag_news

    
        rows: 127k , size: 20 MB
        text:  str, text
        label: str, class label
    
    """
    cols0 = ["text", "label"]
    log(df[cols0].shape)


    #### Taget columns
    n     = len(df)
    dtymd = date_now(fmt="%Y%M%D",  returnval="str")
    url   = meta_dict["url"]

    df["id_global"]  = [uuid_int64() for i in range(n)]
    df["id_dataset"] = url  ### easier to understand
    df["dt"]         = dtymd ### YMD date
    df["id_local"]   = -1


    ###### Custom mapping ###########################
    
    df["title"]     = df["text"].apply(lambda x: " ".join(x.split(" ")[:15]) )
    df["summary"]   = ""
    df["body"]      = df["text"]  ; del df["text"]
    df["info_json"] = df.apply(lambda x: json.dumps({}), axis=1)
    df["cat1"]      = df["label"] ; del df["label"]
    df["cat2"]      = ""
    df["cat3"]      = ""
    df["cat4"]      = ""
    df["cat5"]      = ""

    cols1 = [x[0] for x in  SCHEMA_GLOBAL_v1 ] 
    df = df[cols1]
    return df















#######################################################################################
######## utils  #######################################################################
def hash_mmh64(xstr: str) -> int:
    # pylint: disable=E1136
    return mmh3.hash64(str(xstr), signed=False)[0]



def pd_text_normalize_clean(df: pd.DataFrame) -> pd.DataFrame:
    # Combine title and text columns
    df['content'] = df['title'] + " " + df['text']

    # Remove special characters, punctuation, and extra whitespaces
    df['content'] = df['content'].apply(lambda x: re.sub(r'\s+', ' ', x))  # Remove extra whitespaces
    df['content'] = df['content'].apply(lambda x: re.sub(r'[^\w\s]', '', x))  # Remove special characters
    df['content'] = df['content'].apply(lambda x: x.lower())  # Convert text to lowercase

    # Drop unnecessary columns
    #df.drop(columns=['title', 'text', 'url'], inplace=True)

    return df















#######################################################################################
def test_hf_dataset_to_parquet():
    """test function for converting Hugging Face datasets to Parquet files"""
    name = "ag_news"
    splits = ["train", "test"]
    dataset_hf_to_parquet(name, dirout="hf_datasets", splits=splits)
    # read the parquet files
    for split in splits:
        assert os.path.exists(f"hf_datasets/{name}_{split}.parquet")
        # pd = pd_read_file(f"hf_datasets/{dataset_name}_{split}.parquet")
        # print(pd.columns)


###################################################################################
###################################################################################
def dataset_hf_to_parquet(
    name, dirout: str = "hf_datasets", splits: list = None, mapping: dict = None
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
        splits = ["train", "test"]

    for key in splits:
        split_dataset = dataset[key]
        output_file = f"{dirout}/{name}/{key}.parquet"
        df = pd.DataFrame(split_dataset)
        log(df.shape)
        if mapping is not None:
            df = df.rename(columns=mapping)

        # Raw dataset in parquet
        pd_to_file(df, output_file)


def dataset_kaggle_to_parquet(
    name, dirout: str = "kaggle_datasets", mapping: dict = None, overwrite=False
):
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


def dataset_agnews_schema_v1(
    dirin="./**/*.parquet", dirout="./norm/", batch_size=1000
) -> None:
    """Standardize schema od a dataset"""
    flist = glob_glob(dirin)

    cols0 = ["text", "label"]

    for ii, fi in enumerate(flist):
        df = pd_read_file(fi, npool=1)
        log(ii, df[cols0].shape)

        #### New columns
        ### Schame : [ "id", "dt", ]
        n = len(df)
        dtunix = date_now(returnval="unix")
        df["id"] = [uuid_int64() for i in range(n)]
        df["dt"] = [int(dtunix) for i in range(n)]

        df["body"] = df["text"]
        del df["text"]

        df["title"] = df["body"].apply(lambda x: x[:50])
        df["cat1"] = df["label"]
        del df["label"]
        df["cat2"] = ""
        df["cat3"] = ""
        df["cat4"] = ""
        df["cat5"] = ""
        df["cat6"] = ""
        df["cat7"] = ""
        df["cat8"] = ""
        df["extra_json"] = ""

        fname = fi.split("/")[-1]
        fout = fname.split(".")[0]  # derive target folder from source filename

        dirouti = f"{dirout}/{fout}"
        pd_to_file_split(df, dirouti, ksize=batch_size)


def pd_to_file_split(df, dirout, ksize=1000):
    kmax = int(len(df) // ksize) + 1
    for k in range(0, kmax):
        log(k, ksize)
        dirout = f"{dirout}/df_{k}.parquet"
        pd_to_file(df.iloc[k * ksize : (k + 1) * ksize, :], dirout, show=0)



##########################################################################
def np_str(v):
    return np.array([str(xi) for xi in v])


def uuid_int64():
    """## 64 bits integer UUID : global unique"""
    return uuid.uuid4().int & ((1 << 64) - 1)


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



