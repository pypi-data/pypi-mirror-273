"""
    #### Install
        # NEbula installation
        Option 0 for machines with Docker: `curl -fsSL nebula-up.siwei.io/install.sh | bash`
        Option 1 for Desktop: NebulaGraph Docker Extension https://hub.docker.com/extensions/weygu/nebulagraph-dd-ext

    #### USAGE:
        alias pykg="python3 -u engine_kg.py  "

        # Create test data
        pykg test_create_test_data --dirout ztmp/kg/testraw.csv
        
        # Create schema
        pykg kg_db_create_schema  --space_name kg_relation
        
        # save triplets to file
        pykg  kg_model_extract --dirin myraw.csv --model_id Babelscape/rebel-large -- dirout ztmp/kg/data/kg_relation.csv
        
        # insert triplets to database
        pykg  kg_db_insert_triplet_file --dirin ztmp/kg/data/kg_relation.csv   --space_name kg_relation

        # insert agnews data to database  ( need large to prevent empty triplet....)
        pykg  kg_model_extract --model_id Babelscape/rebel-large --dirout ztmp/kg/data/agnews_kg_relation_test.csv --coltxt body --nrows 1000000 --batch_size 25 --dirin ztmp/bench/norm/ag_news/test/df_*.parquet

        # search kg
        pykg kg_db_query --space_name "agnews_kg_relation" --query "What is the capital of mexico ?"

        # generate test queries
        pykg kg_generate_questions_from_triplets --dirin ztmp/kg/data/agnews_kg_relation.csv --dirout ztmp/kg/data/agnews_kg_questions.csv --batch_size 20

        # benchmark queries
        pykg kg_benchmark_queries --dirin ztmp/kg/data/agnews_kg_questions.csv --dirout ztmp/kg/data/agnews_kg_benchmark.csv --queries=1000


   ### TODO :
      We want to fetch some documents ID, related to the triplet of the initial Question.

        Current with LllamaIndex :
             Natural Query --> NebulaGraph Cypher query --> Response in triplet --> Converted back in Natural questions (hallucination)


        ----> Use KG as Document Retriever (instead)
        What we to do (ie integrate with other engine)
             Natural Query --> NebulaGraph Cypher query --> Response in triplet 
                    --> Add the document related to triplets. ????

               (triplet:  (Person, president, Country) ) ---> List of Doc_id per triplet. (list)

                Check in Nebula to find doc_id related to triplet

                    Or we do external storage (ie parquet or sqlmy, duckdb like sqlite).


   ### Insert agnews, create some test queries

       "what is the capital of mexico ?"

        Method 1:
            ---> Go by the triple extractor,  ---> get some triplet --> query directly the triple


        def kg_query_...


        Method 2:
            ---> Extract keyword :
                    capital, mexico






    #### Goal to small proptopye of KG retrieval

    A) Indexer :  Extract Triplet (A, relation, B) from raw text --> store in database/NebulaGraph
                Alot of connected keyword. : normalize keywords, extra triplets


    B) query  :
        query --> extract keyword from query --> search in KG datas using keyword and relation around keyword
                --> hybrid with emebdding  -->

    ####
    Groq Engine : Cloud service Host llama3, 
        very fast very cheap,  500 token/seconds,  Alternative to GPT 3.5  (cheaper/faster)

        



    ######################################################################################################
    #### Entity Extractor :

    https://github.com/zjunlp/DeepKE

    https://github.com/thunlp/OpenNRE

    https://github.com/zjunlp/KnowLM

    https://maartengr.github.io/BERTopic/getting_started/representation/representation.html#maximalmarginalrelevance

    
    
    1)
    Llamax -- use LLM + Prompt

    2) BERt like model to extract.(faster/cheaper) 
    https://medium.com/nlplanet/building-a-knowledge-base-from-texts-a-full-practical-example-8dbbffb912fa

    pre-trained model.  --> with huggingFae directlyt.
        https://huggingface.co/Babelscape/mrebel-large


    3) ... NER extraction...


    
    Llama Index --> Nebula Graph




    without LLM, one way:
    https://medium.com/nlplanet/building-a-knowledge-base-from-texts-a-full-practical-example-8dbbffb912fa


    ####Groq is cheap/Fast for Llama3 Enitry extraction
        https://towardsdatascience.com/relation-extraction-with-llama3-models-f8bc41858b9e



    #### Questions Pairs
        https://huggingface.co/datasets/databricks/databricks-dolly-15k



    REBEL model

    https://huggingface.co/Babelscape/mrebel-large




    Building  KG graph index is  trickier part....

    https://github.com/wenqiglantz/llamaindex_nebulagraph_phillies/tree/main

    https://towardsdatascience.com/12-rag-pain-points-and-proposed-solutions-43709939a28c



    hacked  coedium engine to access by CLI (ie auto generate  docstring)


"""
import os, pathlib, uuid, time, traceback, warnings, logging, sys

warnings.filterwarnings("ignore")
from typing import Any, Callable, Dict, List, Optional, Sequence, Union
from box import Box  ## use dot notation as pseudo class

import json, warnings, spacy, pandas as pd, numpy as np, torch

### KG
from nebula3.Config import Config
from nebula3.gclient.net import ConnectionPool
from nebula3.common import *

from transformers import (AutoTokenizer, AutoModelForMaskedLM, pipeline)

############################################
from utilmy.webapi.asearch.query import llm_get_answer
from utilmy.webapi.asearch import spacy_component

from utilmy.webapi.asearch.utils import torch_getdevice, pd_append

## Uncomment this section for llamaindex llm call logs
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
import llama_index.core
llama_index.core.set_global_handler("simple")

############################################
from utilmy import pd_read_file, os_makedirs, pd_to_file, date_now, glob_glob
from utilmy import log, log2


################################################################################
def test_create_test_data(dirout="./ztmp/testdata/myraw.csv"):
    """
    usage: pythpn3 -u enging_kg test_create_test_data --dirout myraw.csv
    """
    from llama_index.readers.wikipedia import WikipediaReader
    loader = WikipediaReader()
    documents = loader.load_data(
        pages=["Guardians of  Galaxy Vol. 3"], auto_suggest=False
    )
    text_list = documents[0].text.split("\n")
    # remove short lines
    text_list = [text for text in text_list if len(text) > 20]
    text_df = pd.DataFrame(text_list, columns=["text"], dtype=str)
    pd_to_file(text_df, dirout, show=1)


def test0():
    triplet_extractor = pipeline('translation_xx_to_yy', model='Babelscape/mrebel-base',
                                 tokenizer='Babelscape/mrebel-base')

    # We need to use  tokenizer manually since we need special tokens.
    msg = " Red Hot Chili Peppers were formed in Los Angeles by Kiedis, Flea"
    extracted_text = triplet_extractor.tokenizer.batch_decode([triplet_extractor(msg,
                                                                                 src_lang="en", return_tensors=True,
                                                                                 return_text=False)[0][
                                                                   "translation_token_ids"]])  # change __en__ for  language of  source.
    print(extracted_text[0])


################################################################################
class TripletExtractorModel:
    def __init__(self, model_id='Babelscape/rebel-large', model_type="mrebel"):
        """Initializes  TripletExtractorModel with  specified model_id and model_type.
         Args:
            model_id (str):  ID of  model to be used. Default is 'Babelscape/rebel-large'.
            model_type (str):  type of  model. Default is "mrebel".

        """
        self.model_id = model_id
        self.model_type = model_type

        if model_type == "mrebel":
            s_time = time.time()
            device = torch_getdevice()
            self.pipeline = pipeline('text2text-generation', model=model_id,
                                     tokenizer=model_id, device=device)
            log(f"Model loaded in {time.time() - s_time:.2f} seconds")
        else:
            raise ValueError(f"Invalid model type: {model_type}")

    def extract_triplets(self, text) -> list:
        """Extracts triplets from  given text.

        Args:
            text (str):  text from which to extract triplets.

        Returns:
            list: A list of dictionaries representing  extracted triplets. 
            Each dictionary contains  keys 'head', 'type', and 'tail', representing  subject, predicate, and object of  triplet.

        """
        triplets = []
        relation, subject, relation, object_ = '', '', '', ''
        text = text.strip()
        current = 'x'
        for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").split():
            if token == "<triplet>":
                current = 't'
                if relation != '':
                    triplets.append({'head': subject.strip(), 'type': relation.strip(), 'tail': object_.strip()})
                    relation = ''
                subject = ''
            elif token == "<subj>":
                current = 's'
                if relation != '':
                    triplets.append({'head': subject.strip(), 'type': relation.strip(), 'tail': object_.strip()})
                object_ = ''
            elif token == "<obj>":
                current = 'o'
                relation = ''
            else:
                if current == 't':
                    subject += ' ' + token
                elif current == 's':
                    object_ += ' ' + token
                elif current == 'o':
                    relation += ' ' + token
        if subject != '' and relation != '' and object_ != '':
            triplets.append({'head': subject.strip(), 'type': relation.strip(), 'tail': object_.strip()})
        return triplets

    def extract(self, text_list: list) -> list:
        """Extracts information from a list of texts and returns a list of extracted triplets.
        
         Args:
            text_list (list): A list of texts for which information needs to be extracted.
        
        Returns:
            list: A list of extracted triplets containing  head, type, and tail of each triplet.
        """

        result = []
        from datasets import Dataset
        data = {
            'id': list(range(len(text_list))),
            'text': text_list
        }
        dataset = Dataset.from_dict(data)
        # print(dataset)
        extracted_text = self.pipeline.tokenizer.batch_decode([self.pipeline(
            dataset["text"],
            return_tensors=True, return_text=False)[0]["generated_token_ids"]])
        # print(f"extracted_text: {extracted_text}")
        triplet = self.extract_triplets(extracted_text[0])
        result.extend(triplet)
        print(len(result))
        return result
        # return triplet


class SpacyTripletExtractorModel:

    def __init__(self, model_id='Babelscape/rebel-large'):
        self.model_id = model_id
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe("rebel", after="senter", config={
            'device': -1,  # Number of the GPU, -1 if want to use CPU
            'model_name': model_id}  # Model used, will default to 'Babelscape/rebel-large' if not given
                          )

    def post_process(self, extracted_triplets):
        post_processed = []
        for triplet in extracted_triplets:
            p_triplet = {}
            p_triplet['head'] = triplet['head_span'].lemma_  # span => lemmatized str
            p_triplet['tail'] = triplet['tail_span'].lemma_  # span => lemmatized str
            p_triplet['type'] = triplet['relation']  # already str
            post_processed.append(p_triplet)
        return post_processed

    def extract(self, text_list: list) -> list:
        result = []
        docs = self.nlp.pipe(text_list)
        for doc in docs:
            for value, rel_dict in doc._.rel.items():
                result.append(rel_dict)

        result = self.post_process(result)
        return result


def kg_model_extract(dirin="myraw.csv", model_id="Babelscape/rebel-large", dirout="data/kg_relation.csv", nrows=100000,
                     coltxt="text"):
    """
    usage: pykg kg_model_extract --dirin myraw.csv --model_id Babelscape/rebel-large -- dirout data/kg_relation.csv
    Processed docs/Time taken:
    10/5.56 seconds
    20/9.66 seconds
    30/14.06 seconds
    """
    dfraw = pd_read_file(dirin)
    print(dfraw.columns)
    assert coltxt in dfraw.columns
    print(f"nrows: {nrows}")
    # pick nrows rows from df
    dfraw = dfraw[:nrows]
    print(type(dfraw[coltxt].values.tolist()))
    txt_list = dfraw[coltxt].values.tolist()
    print(f"len(txt_list): {len(txt_list)}")
    extractor = TripletExtractorModel(model_id=model_id, model_type="mrebel")
    # extractor = SpacyTripletExtractorModel(model_id=model_id)
    extracted_triplets = extractor.extract(txt_list)
    # log(f"len(extracted_triplets): {len(extracted_triplets)}")
    kg_relation_save(extracted_triplets, dirout=dirout)


def kg_relation_save(extracted_triplets, dirout="data/kg_relation.csv"):
    if os.path.exists(dirout):
        df = pd_read_file(dirout)
        df = df[['head', 'type', 'tail', "info_json"]]
    else:
        df = pd.DataFrame(columns=['head', 'type', 'tail', "info_json"])

    row_list = [[triplet["head"], triplet["type"], triplet["tail"], triplet.get("info_json", {})] for triplet in
                extracted_triplets]

    df = pd_append(df, row_list)

    pd_to_file(df, dirout, show=1)


######################################################################################################
#######  DB Nebula Graph #############################################################################
def test_kg_db_insert_triplet_file():
    """ A function to test if data is inserted into KKG DB

    """
    # check if data is inserted
    space_name = "test_kg_relation"
    client = kg_db_get_client()
    kg_db_create_schema(client=client, space_name=space_name)
    time.sleep(10)

    resp = client.execute(f"USE {space_name};")
    kg_db_insert_triplet_file(dirin="data/kg_relation.csv", space_name=space_name, nrows=10)
    time.sleep(10)

    resp_json = client.execute_json(f"MATCH (s)-[e]->(o) RETURN count(e) as count;")
    json_obj = json.loads(resp_json)
    # {'errors': [{'code': 0}], 'results': [{'spaceName': 'test_kg_relation', 'data': [{'meta': [None], 'row': [10]}], 'columns': ['count'], 'errors': {'code': 0}, 'latencyInUs': 4081}]}
    assert json_obj["results"][0]["data"][0]["row"][0] == 10
    # drop space
    resp = client.execute(f"DROP SPACE {space_name};")


def kg_db_get_client(engine_name="nebula"):
    config = Config()
    connection_pool = ConnectionPool()
    assert connection_pool.init([('127.0.0.1', 9669)], config)
    # get session from  pool
    client = connection_pool.get_session('root', 'nebula')
    assert client is not None
    return client


def kg_db_create_schema(client=None, space_name="kg_relation"):
    if client is None:
        client = kg_db_get_client()
    resp = client.execute(
        f"CREATE SPACE {space_name}(vid_type=FIXED_STRING(256), partition_num=1, replica_factor=1);"
        f"USE {space_name};"
        "CREATE TAG entity(name string);"
        "CREATE EDGE relationship(relationship string);"
        "CREATE TAG INDEX entity_index ON entity(name(256));"
    )
    assert resp.is_succeeded(), resp.error_msg()


def kg_db_insert_triplet(client=None, space_name="kg_relation", row=None):
    resp = client.execute(f"USE {space_name};")
    assert resp.is_succeeded(), resp.error_msg()

    vertex_query = f"""INSERT VERTEX entity(name) VALUES "{row.head}":("{row.head}"), "{row.tail}":("{row.tail}")"""
    # log(vertex_query)
    resp = client.execute(vertex_query)
    assert resp.is_succeeded(), resp.error_msg()

    # edge query
    edge_query = f"""INSERT EDGE relationship(relationship) VALUES "{row.head}"->"{row.tail}":("{row.type}")"""

    # log(edge_query)
    resp = client.execute(edge_query)
    assert resp.is_succeeded(), resp.error_msg()


def kg_db_insert_triplet_file(dirin="data/kg_relation.csv", space_name="kg_relation", nrows: int = -1):
    """

    """
    df = pd_read_file(dirin)
    nrows = len(df) if nrows < 0 else nrows

    # create nebula client
    client = kg_db_get_client()
    assert client is not None

    log("#### create schema ")
    client.execute(f"""USE {space_name};""")

    log("#### insert ")
    for row in df[:nrows].itertuples():
        kg_db_insert_triplet(client=client, space_name=space_name, row=row)


def kg_db_query(space_name="agnews_kg_relation", query=""):
    """A function to query the knowledge graph database with the specified space name and query string.

    LlamaIndex uses LLM GPt3.5
          Naturaal Query ---> KG Nebula queries.
          Required OPENAI TOKEN in env variable.
          
        Digged deeper into llama-index query calls.
        For each query it is calling llm 2 times:
        1. Extract keywords from llm query
        2. Fetch answer from db output triplets


    Issues: LLM is called every time to convert Natural Queries --> KG Nebula queries

            Find a way to generate Nebula query from llama Index.



    Parameters:
    - space_name (str): The name of the space in the knowledge graph database to query.
    - query (str): The query string to search in the knowledge graph.

    """
    from llama_index.core import KnowledgeGraphIndex, StorageContext
    from llama_index.graph_stores.nebula import NebulaGraphStore

    if not query:
        return

    edge_types, rel_prop_names = ["relationship"], ["relationship"]
    tags = ["entity"]

    ### Init Databse
    # expects NEBULA_USER, NEBULA_PASSWORD, NEBULA_ADDRESS in environment variables
    graph_store = NebulaGraphStore(
        space_name=space_name,
        edge_types=edge_types,
        rel_prop_names=rel_prop_names,
        tags=tags,

    )
    # create storage context
    storage_context = StorageContext.from_defaults(graph_store=graph_store, )

    # fetch KG database index
    index = KnowledgeGraphIndex.from_documents(
        [],
        storage_context=storage_context,
        max_triplets_per_chunk=2,
        space_name=space_name,
        edge_types=edge_types,
        rel_prop_names=rel_prop_names,
        tags=tags,
    )
    query_engine = index.as_query_engine()

    # llm call here. adds network overhead to each query
    ### LLM is called to generate the Natural query --> KG Query
    response = query_engine.query(query)
    return response.response


######################################################################################################
#######  Query generator from KG db triplet ##########################################################
def kg_generate_questions_from_triplets(dirin="ztmp/kg/data/agnews_kg_relation_test.csv",
                                        dirout="ztmp/kg/data/agnews_kg_question.csv", nrows: int = 1000,
                                        batch_size: int = 20):
    """
    Generate questions based on triplets extracted from a file and save them to a new CSV file.

    :param dirin: Input file path containing triplets, default is "ztmp/kg/data/agnews_kg_relation_gpu.csv"
    :param dirout: Output file path to save the generated questions, default is "data/agnews_kg_question.csv"
    """
    df = pd_read_file(dirin)

    df = df[["head", "type", "tail"]]
    # remove duplicates
    df = df.drop_duplicates()
    # take first nrows
    df = df[:nrows]

    result_df = pd.DataFrame(columns=["head", "type", "tail", "question"])
    for i in range(0, len(df), batch_size):
        df_subset = df[i:i + batch_size]

        ####   |head|type|tail   |head|type|tail   
        triplet_str = "\n".join([f"{'|'.join([row.head, row.type, row.tail])}" for row in df_subset.itertuples()])
        # generate question using llm
        prompt = f"For each triplet, generate a question based on the triplet(head|type|tail):\n{triplet_str}"
        # print(f"prompt: {prompt}")

        response = llm_get_answer(prompt, model="gpt-3.5-turbo", max_tokens=1000)
        questions = response.split("\n")

        # clean up : remove preceeding numerical number
        questions = [q.split(".")[1].strip() if "." in q else q for q in questions]
        if len(questions) == len(df_subset):
            df_subset["question"] = questions
            result_df = pd.concat([result_df, df_subset])

    pd_to_file(result_df, dirout, index=False)


######################################################################################################
#######  Metrics /benchmark ##########################################################

def metrics_kg_is_triplet_covered(triplet_tuple, question, answer):
    return all([k in question or k in answer for k in triplet_tuple])


def kg_benchmark_queries(dirin="ztmp/kg/data/agnews_kg_question.csv",
                         dirout="ztmp/kg/data/agnews_kg_benchmark.csv",
                         queries=1000):
    """
    Average time taken per query: 1.82 seconds
        Accuracy: 80% 

    """
    question_df = pd_read_file(dirin)
    result = []
    for row in question_df[:queries].itertuples():
        s_time = time.time()
        response = kg_db_query(query=row.question)
        dt = time.time() - s_time

        is_correct = metrics_kg_is_triplet_covered([row.head, row.tail], row.question, response)
        result.append([row.question, response, dt, is_correct])

    df = pd.DataFrame(result, columns=["question", "response", "dt", "is_correct"])
    pd_to_file(df, dirout, index=False, show=1)
    log(f" Average time taken: {df.dt.mean():.2f} seconds")
    log(f" Percentage accuracy: {df.is_correct.mean() * 100:.2f} %")


###################################################################################################
if __name__ == "__main__":
    import fire

    fire.Fire()


#####################
# def zzz_query_using_llamaindex():
#     """
#         https://medium.com/@sauravjoshi23/building-knowledge-graphs-rebel-llamaindex-and-rebel-llamaindex-8769cf800115
#
#
#         # CREATE SPACE rebel_llamaindex(vid_type=FIXED_STRING(256), partition_num=1, replica_factor=1);
#         # :sleep 10;
#         # USE rebel_llamaindex;
#         # CREATE TAG entity(name string);
#         # CREATE EDGE relationship(relationship string);
#         # CREATE TAG INDEX entity_index ON entity(name(256));
#
#     """
#
#
#     from llama_index.query_engine import KnowledgeGraphQueryEngine
#
#     from llama_index.storage.storage_context import StorageContext
#     from llama_index.graph_stores import NebulaGraphStore
#
#
#     from llama_index import SimpleDirectoryReader
#
#     reader = SimpleDirectoryReader(input_dir="../data/knowledge graphs/rebel_llamaindex/wiki/")
#     documents = reader.load_data()
#
#     kg_index = KnowledgeGraphIndex.from_documents(
#         documents,
#         storage_context=storage_context,
#         max_triplets_per_chunk=5,
#         service_context=service_context,
#         space_name=space_name,
#         edge_types=edge_types,
#         rel_prop_names=rel_prop_names,
#         tags=tags,
#         include_embeddings=True,
#     )
#
#
#
#     query_engine = KnowledgeGraphQueryEngine(
#         storage_context=storage_context,
#         service_context=service_context,
#         llm=llm,
#         verbose=True,
#     )
#

###################################################################################################
#####################
#     # Function to parse  generated text and extract  triplets
# def zzz_extract_triplets_typed(text):
#     triplets = []
#     relation = ''
#     text = text.strip()
#     current = 'x'
#     subject, relation, object_, object_type, subject_type = '', '', '', '', ''
#
#     for token in text.replace("<s>", "").replace("<pad>", "").replace("</s>", "").replace("tp_XX", "").replace("__en__",
#                                                                                                                "").split():
#         if token == "<triplet>" or token == "<relation>":
#             current = 't'
#             if relation != '':
#                 triplets.append({'head': subject.strip(), 'head_type': subject_type, 'type': relation.strip(),
#                                  'tail': object_.strip(), 'tail_type': object_type})
#                 relation = ''
#             subject = ''
#         elif token.startswith("<") and token.endswith(">"):
#             if current == 't' or current == 'o':
#                 current = 's'
#                 if relation != '':
#                     triplets.append({'head': subject.strip(), 'head_type': subject_type, 'type': relation.strip(),
#                                      'tail': object_.strip(), 'tail_type': object_type})
#                 object_ = ''
#                 subject_type = token[1:-1]
#             else:
#                 current = 'o'
#                 object_type = token[1:-1]
#                 relation = ''
#         else:
#             if current == 't':
#                 subject += ' ' + token
#             elif current == 's':
#                 object_ += ' ' + token
#             elif current == 'o':
#                 relation += ' ' + token
#     if subject != '' and relation != '' and object_ != '' and object_type != '' and subject_type != '':
#         triplets.append(
#             {'head': subject.strip(), 'head_type': subject_type, 'type': relation.strip(), 'tail': object_.strip(),
#              'tail_type': object_type})
#     return triplets
