


myutil :   Toolbox of many many utils...(too mamy)

Project : 
   Add Hybrid search  utilies  ( /API )

Combine mutiple search engine (in python) results: 


Scheme: 
 Engine1 ---> List1
 Engine2 ---> List2     ---> Merge (pip isntall RANX) ---> Results
 Engine3 ---> List3
 

 Input :  " my query"
 Ouput :  list of documents + text 

#### Indiviual engine
Engine1 : Qdrant 
             dense vector, Sparse Vector 
             Build the index on disk 
             Server ??? (http:// localhost ?? or not ), 
               we cannot query the index 
                FAISS ---> query the index directly... (Load the index in RAM)


Engine2: Tantivy (BM25 search : very fast)
                 we can query the index on disk directly (no need of server).
                 Disk should be fast.

Engine3:  XXXX                 



Fixed Price : upwork 
   




#### Merge
   pip install RANX --> many merge algo : RRF 
       Inverse rank (ranking merge) --> easy.
   --> Output



##### Start on creating index
def converter_text_to_parquet(dirin:str, dirout:str)--> None
   ### Custom per text data : Yaki job 
   https://www.kaggle.com/datasets/kotartemiy/topic-labeled-news-dataset

   


def create_qdrant_index_dense(dirin:str, dirout:str, 
                         coltext:str="body", ### Vector
                         colscat:list=None,
                         embed_engine_name="embed"
                          )--> None
   ### dirin: list of parquet files :  Ankush
     pip install fastembed
     

def create_qdrant_index_sparse(dirin:str, dirout:str, 
                         coltext:str="body", ### Vector
                         colscat:list=None,
                         embed_engine="embed"
                          )--> None
   ### dirin: list of parquet files :  Ankush
   ### pip install fastembed
   https://qdrant.tech/articles/sparse-vectors/



def merge_fun(x, cols, sep=" @ "):
    ##     textall = title + body. + cat1 " @ "
    ss = ""
    for ci in cols : 
         ss = x[ci] + sep 
    return ss[:-1] 


def create_tantivy_index(dirin:str, dirout:str, 
                         cols:list=None)--> None
   ### dirin: list of parquet files : Ankush
   df["textall"] = df.apply(lambda x : merge_fun(x, cols), axis=1)


#### packages to use 
  pip install fastembed fire python-box   tantivy-py  qdrant 



## def test(dirout:str):
### python myfile.py  test  -dirout ...








#### Document Schema : specificedby User.
   title  :   text
   body   :    text
   cat1   :    string   fiction / sport /  politics
   cat2   :    string     important / no-important 
   cat3   :    string
   cat4   :    string   
   cat5   :    string    
   dt_ymd :    int     20240311


   ---> Encode into Indexes by engine.

 Converter Tool 
    stored in raw text file --->  into parquet files 

     Insert Indexes takes parquet as INPUT ---> Insert into indexes.


   def engine_index_insert( engine_name,  filein:str,  engine_index_out : str, 
                            engine_pars: dict, cols:list=None ): 

      ### pip install utilmy
      from utilmy import pd_read_file  ### /*/ glob_glob
      df = pd_read_file(filein, columns=cols, npool=5)

      ### when we load engine --> also load the schema                                                
      engine = load_engine(engine_name, engin_index_outk, engine_pars)

      ### check schema
      engine_schema_check(engine, df.dtypes)

      dflist = engine_convert(df)
      engine.insert_bulk(  dflist )


#### Pipeline to create indexes
  Raw Text in txt file on disk --->. Parquet file --> Indexes 
   








#### API : I can do it in FastAPI (server)

















"""
The importance of search engines in our daily lives cannot be overstated. They help us navigate the vast ocean of information available on the internet and make it accessible at our fingertips. In this article, I’ll guide you through the process of building a custom search engine from scratch using FastAPI, a high-performance web framework for Python, and Tantivy, a fast, full-text search engine library written in Rust.

Before diving into the code, we need to set up our development environment. First, ensure that you have Python installed on your system. FastAPI requires Python 3.6 or higher. Next, install FastAPI and its dependencies. You can do this using the following command:
pip install fastapi[all]
This command will install FastAPI and all the optional dependencies needed for its various features. Tantivy is a Rust library, so we’ll need to use a Python wrapper called “tantivy-py” to work with it. Install the wrapper using:
pip install tantivy-py
Now that we have the necessary tools and libraries installed, create a virtual environment for your project and set up your preferred IDE or text editor.

FastAPI
FastAPI is a modern, high-performance web framework for building APIs with Python. It’s designed to be easy to use and has built-in support for type hints, which allows for automatic data validation, serialization, and documentation generation. FastAPI also has excellent support for asynchronous programming, which improves the performance of I/O-bound operations.

To create a FastAPI application, you’ll need to define routes, add parameters, and create request and response models. Routes are the different URLs or paths that your API can handle, while parameters are the variables passed in the URL, query string, or request body. Request and response models describe the data structure used for input and output, respectively.

Here’s an example of a FastAPI application with routes, parameters, and request/response models:


#### Rank Fusion
https://github.com/AmenRa/ranx?tab=readme-ov-file



"""



from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class UserIn(BaseModel):
    name: str
    age: int
    city: str

class UserOut(BaseModel):
    id: int
    name: str
    age: int
    city: str

users = []

@app.post("/users", response_model=UserOut)
def create_user(user: UserIn):
    user_id = len(users)
    new_user = UserOut(id=user_id, **user.dict())
    users.append(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int):
    if user_id >= len(users) or user_id < 0:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.get("/users", response_model=list[UserOut])
def search_users(city: str = None, min_age: int = None, max_age: int = None):
    filtered_users = users

    if city:
        filtered_users = [user for user in filtered_users if user.city.lower() == city.lower()]

    if min_age:
        filtered_users = [user for user in filtered_users if user.age >= min_age]

    if max_age:
        filtered_users = [user for user in filtered_users if user.age <= max_age]

    return filtered_users


"""    
In this example, we define a FastAPI application with three routes: create_user, get_user, and search_users. We use the UserIn and UserOut classes as request and response models to validate and serialize the input/output data. We also use parameters in the URL path (e.g., user_id), query string (e.g., city, min_age, max_age), and request body (e.g., user).

Tantivy
Tantivy is a full-text search engine library written in Rust. It is designed to be fast and efficient, making it a great choice for building search engines. Tantivy provides indexing and searching capabilities, allowing you to create a schema, add documents to the index, and execute search queries.

To work with Tantivy, you’ll need to create a schema, which is a description of the structure of your documents. The schema defines the fields in each document, their data types, and any additional options or settings. Once you have a schema, you can add documents to the index, store and retrieve data, and perform searches using basic or advanced query features, such as fuzzy search, filters, and pagination.

Here’s an example of creating a schema, indexing documents, and performing basic and advanced searches using Tantivy:
from tantivy import Collector, Index, QueryParser, SchemaBuilder, Term
"""


# Create a schema
schema_builder = SchemaBuilder()
title_field = schema_builder.add_text_field("title", stored=True)
body_field  = schema_builder.add_text_field("body", stored=True)
schema = schema_builder.build()

# Create an index with the schema
index = Index(schema)

# Add documents to the index
with index.writer() as writer:
    writer.add_document({"title": "First document", "body": "This is the first document."})
    writer.add_document({"title": "Second document", "body": "This is the second document."})
    writer.commit()

# Create a query parser
query_parser = QueryParser(schema, ["title", "body"])

###### Basic search
query = query_parser.parse_query("first")
collector = Collector.top_docs(10)
search_result = index.searcher().search(query, collector)

print("Basic search results:")
for doc in search_result.docs():
    print(doc)

####### Fuzzy search
fuzzy_query = query_parser.parse_query("frst~1")  # Allows one edit distance
fuzzy_collector = Collector.top_docs(10)
fuzzy_search_result = index.searcher().search(fuzzy_query, fuzzy_collector)

print("Fuzzy search results:")
for doc in fuzzy_search_result.docs():
    print(doc)

# Filtered search
title_term = Term(title_field, "first")
body_term = Term(body_field, "first")
filter_query = schema.new_boolean_query().add_term(title_term).add_term(body_term)
filtered_collector = Collector.top_docs(10)
filtered_search_result = index.searcher().search(filter_query, filtered_collector)

print("Filtered search results:")
for doc in filtered_search_result.docs():
    print(doc)








##### qdrant vector


from transformers import AutoModelForMaskedLM, AutoTokenizer

model_id = 'naver/splade-cocondenser-ensembledistil'

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForMaskedLM.from_pretrained(model_id)

text = """Arthur Robert Ashe Jr. (July"""




import torch

def compute_vector(text, tokenizer, model):
    """
    Computes a vector from logits and attention mask using ReLU, log, and max operations.

    Args:
    logits (torch.Tensor): The logits output from a model.
    attention_mask (torch.Tensor): The attention mask corresponding to the input tokens.

    Returns:
    torch.Tensor: Computed vector.
    """
    tokens = tokenizer(text, return_tensors="pt")
    output = model(**tokens)
    logits, attention_mask = output.logits, tokens.attention_mask
    relu_log = torch.log(1 + torch.relu(logits))
    weighted_log = relu_log * attention_mask.unsqueeze(-1)
    max_val, _ = torch.max(weighted_log, dim=1)
    vec = max_val.squeeze()

    return vec, tokens


vec, tokens = compute_vector(text, tokenizer=tokenizer, model=model)
print(vec.shape)

len(tokens.input_ids[0])




def extract_and_map_sparse_vector(vector, tokenizer):
    """
    Extracts non-zero elements from a given vector and maps these elements to their human-readable tokens using a tokenizer. The function creates and returns a sorted dictionary where keys are the tokens corresponding to non-zero elements in the vector, and values are the weights of these elements, sorted in descending order of weights.

    This function is useful in NLP tasks where you need to understand the significance of different tokens based on a model's output vector. It first identifies non-zero values in the vector, maps them to tokens, and sorts them by weight for better interpretability.

    Args:
    vector (torch.Tensor): A PyTorch tensor from which to extract non-zero elements.
    tokenizer: The tokenizer used for tokenization in the model, providing the mapping from tokens to indices.

    Returns:
    dict: A sorted dictionary mapping human-readable tokens to their corresponding non-zero weights.
    """

    # Extract indices and values of non-zero elements in the vector
    cols = vector.nonzero().squeeze().cpu().tolist()
    weights = vector[cols].cpu().tolist()

    # Map indices to tokens and create a dictionary
    idx2token = {idx: token for token, idx in tokenizer.get_vocab().items()}
    token_weight_dict = {idx2token[idx]: round(weight, 2) for idx, weight in zip(cols, weights)}

    # Sort the dictionary by weights in descending order
    sorted_token_weight_dict = {k: v for k, v in sorted(token_weight_dict.items(), key=lambda item: item[1], reverse=True)}

    return sorted_token_weight_dict

# Usage example
sorted_tokens = extract_and_map_sparse_vector(vec, tokenizer)
sorted_tokens

{'splendid': 2.49,
 'morning': 1.85,
 'eclipse': 0.05,
 'synonym': 0.04,
 'surprised': 0.03}








from transformers import AutoModelForMaskedLM, AutoTokenizer

doc_model_id = "naver/efficient-splade-VI-BT-large-doc"
doc_tokenizer = AutoTokenizer.from_pretrained(doc_model_id)
doc_model = AutoModelForMaskedLM.from_pretrained(doc_model_id)

query_model_id = "naver/efficient-splade-VI-BT-large-query"
query_tokenizer = AutoTokenizer.from_pretrained(query_model_id)
query_model = AutoModelForMaskedLM.from_pretrained(query_model_id)



text = "What a splendid morning!"

doc_vec, doc_tokens = compute_vector(text, model=doc_model, tokenizer=doc_tokenizer)
query_vec, query_tokens = compute_vector(text, model=query_model, tokenizer=query_tokenizer)



sorted_tokens = extract_and_map_sparse_vector(doc_vec, doc_tokenizer)
sorted_tokens
     


#### Hybrid search:


# Qdrant client setup
client = QdrantClient(":memory:")

# Define collection name
COLLECTION_NAME = "example_collection"

# Insert sparse vector into Qdrant collection
point_id = 1  # Assign a unique ID for the point

client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config={},
    sparse_vectors_config={
        "text": models.SparseVectorParams(
            index=models.SparseIndexParams(
                on_disk=False,
            )
        )
    },
)



######
client.upsert(
    collection_name=COLLECTION_NAME,
    points=[
        models.PointStruct(
            id=point_id,
            payload={},  # Add any additional payload if necessary
            vector={
                "text": models.SparseVector(
                    indices=indices.tolist(), values=values.tolist()
                )
            },
        )
    ],
)



####### Preparing a query vector
query_text = "Who was Arthur Ashe?"
query_vec, query_tokens = compute_vector(query_text)
query_vec.shape

query_indices = query_vec.nonzero().numpy().flatten()
query_values = query_vec.detach().numpy()[indices]

# Searching for similar documents
result = client.search(
    collection_name=COLLECTION_NAME,
    query_vector=models.NamedSparseVector(
        name="text",
        vector=models.SparseVector(
            indices=query_indices,
            values=query_values,
        ),
    ),
    with_vectors=True,
)
print(result)




client.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config={
        "text-dense": models.VectorParams(
            size=1536,  # OpenAI Embeddings
            distance=models.Distance.COSINE,
        )
    },
    sparse_vectors_config={
        "text-sparse": models.SparseVectorParams(
            index=models.SparseIndexParams(
                on_disk=False,
            )
        )
    },
)



query_text = "Who was Arthur Ashe?"

# Compute sparse and dense vectors
query_indices, query_values = compute_sparse_vector(query_text)
query_dense_vector = compute_dense_vector(query_text)


client.search_batch(
    collection_name=COLLECTION_NAME,
    requests=[
        models.SearchRequest(
            vector=models.NamedVector(
                name="text-dense",
                vector=query_dense_vector,
            ),
            limit=10,
        ),
        models.SearchRequest(
            vector=models.NamedSparseVector(
                name="text-sparse",
                vector=models.SparseVector(
                    indices=query_indices,
                    values=query_values,
                ),
            ),
            limit=10,
        ),
    ],
)



##### Re-ranking
You can use obtained results as a first stage of a two-stage retrieval process. 
In the second stage, you can re-rank the results from the first stage using a more complex model, such as Cross-Encoders or services like Cohere Rerank.

And that’s it! You’ve successfully achieved hybrid search with Qdrant!


https://www.sbert.net/examples/applications/cross-encoder/README.html




##### Merge ranking using RRF
https://github.com/AmenRa/ranx?tab=readme-ov-file



#### Usearch
https://github.com/unum-cloud/usearch

















######################################################################################
"""    
In this example, we first create a schema with two text fields: “title” and “body”. Then, we create an index and add documents to it. We also create a query parser to parse queries for searching the index. We demonstrate basic search, fuzzy search (with a specified edit distance), and filtered search (using boolean queries to combine terms).
Building the Search Engine
Now that we have an understanding of FastAPI and Tantivy, it’s time to build our search engine. We’ll start by designing the search engine architecture, which includes the FastAPI application and the Tantivy index.

First, create a FastAPI application by defining search and indexing endpoints. These endpoints will be responsible for processing search queries and indexing new documents, respectively. Implement request and response models for each endpoint to describe the data structure used for input and output.
"""


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tantivy import Collector, Index, QueryParser, SchemaBuilder

app = FastAPI()

# Create a schema
schema_builder = SchemaBuilder()
title_field = schema_builder.add_text_field("title", stored=True)
body_field = schema_builder.add_text_field("body", stored=True)
schema = schema_builder.build()

# Create an index with the schema
index = Index(schema)

# Create a query parser
query_parser = QueryParser(schema, ["title", "body"])

class DocumentIn(BaseModel):
    title: str
    body: str

class DocumentOut(BaseModel):
    title: str
    body: str

@app.post("/index", response_model=None)
def index_document(document: DocumentIn):
    with index.writer() as writer:
        writer.add_document(document.dict())
        writer.commit()

@app.get("/search", response_model=list[DocumentOut])
def search_documents(q: str):
    query = query_parser.parse_query(q)
    collector = Collector.top_docs(10)
    search_result = index.searcher().search(query, collector)

    documents = [DocumentOut(**doc) for doc in search_result.docs()]
    return documents


"""
In this example, we create a FastAPI application with two endpoints: index_document and search_documents. The index_document endpoint is responsible for indexing new documents, while the search_documents endpoint is responsible for processing search queries. We use the DocumentIn and DocumentOut classes as request and response models to describe the data structure for input and output.

Next, index documents using Tantivy. Write a function that processes and stores data in the Tantivy index. This function should take input data, create a document based on the schema, and add it to the index.
"""
from typing import Dict
from tantivy import Index, SchemaBuilder

# Create a schema
schema_builder = SchemaBuilder()
title_field = schema_builder.add_text_field("title", stored=True)
body_field = schema_builder.add_text_field("body", stored=True)
schema = schema_builder.build()

# Create an index with the schema
index = Index(schema)

def index_document(document_data: Dict[str, str]) -> None:
    with index.writer() as writer:
        writer.add_document(document_data)
        writer.commit()

# Example usage
document = {"title": "Example document", "body": "This is an example document."}
index_document(document)


"""
In this example, we define a function called index_document that takes a dictionary as input data, representing a document to be indexed. This function creates a document based on the schema and adds it to the Tantivy index. The example usage demonstrates how to use the function to index a sample document.

Finally, implement the search functionality. Use Tantivy to execute search queries, and handle search results by processing and returning them in a format that can be easily consumed by the client.
rom typing import Dict, List
from tantivy import Collector, Index, QueryParser, SchemaBuilder
"""


# Create a schema
schema_builder = SchemaBuilder()
title_field = schema_builder.add_text_field("title", stored=True)
body_field = schema_builder.add_text_field("body", stored=True)
schema = schema_builder.build()

# Create an index with the schema
index = Index(schema)

# Create a query parser
query_parser = QueryParser(schema, ["title", "body"])

def search_documents(query_str: str) -> List[Dict[str, str]]:
    query = query_parser.parse_query(query_str)
    collector = Collector.top_docs(10)
    search_result = index.searcher().search(query, collector)

    documents = [doc.as_json() for doc in search_result.docs()]
    return documents

# Example usage
search_query = "example"
results = search_documents(search_query)
print(f"Search results for '{search_query}':")
for doc in results:
    print(doc)

"""
In this example, we define a function called search_documents that takes a query string as input and uses Tantivy to execute the search query. The function processes the search results by converting each result document to a dictionary and returns a list of dictionaries that can be easily consumed by the client. The example usage demonstrates how to use the function to perform a search and display the results.

Testing and Optimization
To ensure that your search engine works correctly and efficiently, write unit tests for the FastAPI and Tantivy components. Test the functionality of each endpoint and the proper interaction between FastAPI and Tantivy. Additionally, benchmark your search engine to assess its performance and identify any bottlenecks or areas for improvement. Optimize your code by addressing these bottlenecks and making any necessary adjustments.

Here’s an example of unit tests for the FastAPI and Tantivy components using pytest and httpx libraries:
"""





#############################################################################################
import pytest
import httpx
from fastapi import FastAPI
from fastapi.testclient import TestClient
from .main import app, index_document, search_documents

client = TestClient(app)

# Test FastAPI endpoints
def test_index_document():
    response = client.post("/index", json={"title": "Test document", "body": "This is a test document."})
    assert response.status_code == 200

def test_search_documents():
    response = client.get("/search", params={"q": "test"})
    assert response.status_code == 200
    assert len(response.json()) > 0
    assert response.json()[0]["title"] == "Test document"

# Test Tantivy components
def test_tantivy_index_document():
    document = {"title": "Tantivy test document", "body": "This is a Tantivy test document."}
    index_document(document)

def test_tantivy_search_documents():
    search_query = "tantivy"
    results = search_documents(search_query)
    assert len(results) > 0
    assert results[0]["title"] == "Tantivy test document"

"""
# Performance benchmarking and optimization can be done using profiling tools,
# such as cProfile, Py-Spy, or others, depending on the specific bottlenecks and areas
# for improvement identified in your application.
To benchmark the search engine and identify bottlenecks, you can use profiling tools, such as cProfile or Py-Spy. Once you’ve identified the areas for improvement, optimize your code by addressing the bottlenecks and making necessary adjustments. Performance optimization is an iterative process and may require multiple rounds of profiling and optimization.

Deploying the Search Engine
Once your search engine is fully functional and optimized, it’s time to deploy it. Choose a deployment platform that best suits your needs, such as a cloud provider or a dedicated server. Configure the deployment environment by setting up necessary components, such as a web server, application server, and any required databases or storage systems.

After deployment, monitor and maintain your search engine to ensure its smooth operation. Keep an eye on performance metrics, such as response times and resource utilization, and address any issues that arise.

In this article, we’ve explored the process of building a search engine from scratch using FastAPI and Tantivy. We’ve covered the fundamentals of both FastAPI and Tantivy, as well as the steps needed to create, test, optimize, and deploy a custom search engine. By following this guide, you should now have a working search engine that can be tailored to your specific needs.

The possibilities with this custom search engine are vast, and you can extend its functionality to accommodate various applications, such as site search, document search, or even powering a custom search service. As you continue to experiment and explore, you’ll discover the true power and flexibility of using FastAPI and Tantivy to create search solutions that meet your unique requirements.
"""









"""
    What The Code Does
    Query Generation: The system starts by generating multiple queries from a user's initial query using OpenAI's GPT model.

    Vector Search: Conducts vector-based searches on each of the generated queries to retrieve relevant documents from a predefined set.

    Reciprocal Rank Fusion: Applies the Reciprocal Rank Fusion algorithm to re-rank the documents based on their relevance across multiple queries.

    Output Generation: Produces a final output consisting of the re-ranked list of documents.

    How to Run the Code
    Install the required dependencies (openai).
    Place your OpenAI API key in the appropriate spot in the code.
    Run the script.
    Why RAG-Fusion?
    RAG-Fusion is an ongoing experiment that aims to make search smarter and more context-aware, thus helping us uncover the richer, deeper strata of information that we might not have found otherwise.




"""
import os
import openai
import random

# Initialize OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")  # Alternative: Use environment variable
if openai.api_key is None:
    raise Exception(
        "No OpenAI API key found. Please set it as an environment variable or in main.py"
    )


# Function to generate queries using OpenAI's ChatGPT
def generate_queries_chatgpt(original_query):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates multiple search queries based on a single input query.",
            },
            {
                "role": "user",
                "content": f"Generate multiple search queries related to: {original_query}",
            },
            {"role": "user", "content": "OUTPUT (4 queries):"},
        ],
    )

    generated_queries = response.choices[0]["message"]["content"].strip().split("\n")
    return generated_queries


# Mock function to simulate vector search, returning random scores
def vector_search(query, all_documents):
    available_docs = list(all_documents.keys())
    random.shuffle(available_docs)
    selected_docs = available_docs[: random.randint(2, 5)]
    scores = {doc: round(random.uniform(0.7, 0.9), 2) for doc in selected_docs}
    return {
        doc: score
        for doc, score in sorted(scores.items(), key=lambda x: x[1], reverse=True)
    }


# Reciprocal Rank Fusion algorithm
def reciprocal_rank_fusion(search_results_dict, k=60):
    fused_scores = {}
    print("Initial individual search result ranks:")
    for query, doc_scores in search_results_dict.items():
        print(f"For query '{query}': {doc_scores}")

    for query, doc_scores in search_results_dict.items():
        for rank, (doc, score) in enumerate(
            sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        ):
            if doc not in fused_scores:
                fused_scores[doc] = 0
            previous_score = fused_scores[doc]
            fused_scores[doc] += 1 / (rank + k)
            print(
                f"Updating score for {doc} from {previous_score} to {fused_scores[doc]} based on rank {rank} in query '{query}'"
            )

    reranked_results = {
        doc: score
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    }
    print("Final reranked results:", reranked_results)
    return reranked_results


# Dummy function to simulate generative output
def generate_output(reranked_results, queries):
    return f"Final output based on {queries} and reranked documents: {list(reranked_results.keys())}"


# Predefined set of documents (usually these would be from your search database)
all_documents = {
    "doc1": "Climate change and economic impact.",
    "doc2": "Public health concerns due to climate change.",
    "doc3": "Climate change: A social perspective.",
    "doc4": "Technological solutions to climate change.",
    "doc5": "Policy changes needed to combat climate change.",
    "doc6": "Climate change and its impact on biodiversity.",
    "doc7": "Climate change: The science and models.",
    "doc8": "Global warming: A subset of climate change.",
    "doc9": "How climate change affects daily weather.",
    "doc10": "The history of climate change activism.",
}

# Main function
if __name__ == "__main__":
    original_query = "impact of climate change"
    generated_queries = generate_queries_chatgpt(original_query)

    all_results = {}
    for query in generated_queries:
        search_results = vector_search(query, all_documents)
        all_results[query] = search_results

    reranked_results = reciprocal_rank_fusion(all_results)

    final_output = generate_output(reranked_results, generated_queries)

    print(final_output)


   import openai

   openai.api_key = 'your-api-key'

   response = openai.File.create(
     file=open("path_to_your_file.jsonl"),
     purpose='fine-tune'
   )
   file_id = response['id']





   fine_tune = openai.FineTune.create(
     model="gpt-4",  # Ensure you specify GPT-4
     training_file=file_id,
     n_epochs=4,
     learning_rate_multiplier=0.1,
     batch_size=4
   )
   print(f"Fine-tune job created with ID: {fine_tune['id']}")


   status = openai.FineTune.retrieve(id=fine_tune['id'])
   print(f"Fine-tune job status: {status['status']}")



   import openai

   openai.api_key = 'your-api-key'

   response = openai.Completion.create(
     model="your-fine-tuned-model-name",  # Replace with your fine-tuned model name
     prompt="Your prompt here",
     max_tokens=50
   )

   print(response.choices[0].text.strip())



   







https://gautam75.medium.com/unlocking-the-power-of-rag-fusion-53437e77d9c2


#####
   query ---> Generate Similar query --> do RAG on similar query. 
   



def dataset_custom_map_v1(dataset_name):
    """Converts a Hugging Face dataset to a Parquet file.
    Args:
        dataset_name (str):  name of  dataset.
        mapping (dict):  mapping of  column names. Defaults to None.
    """
    dataset = datasets.load_dataset(dataset_name)

    df
    # print(dataset)
    for key in dataset:
        df = pd.DataFrame(dataset[key])
        if mapping is not None:
            df = df.rename(columns=mapping)
        # print(df.head)



ksize=1000
kmax = int(len(df) // ksize) +1
for k in range(0, kmax):
    log(k)
    dirouk = f"{dirout}/{df}_{k}.parquet"
    pd_to_file( df.iloc[k*ksize:(k+1)*ksize, : ], dirouk, show=0)




## Recommended Imports
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    NamedSparseVector,
    NamedVector,
    SparseVector,
    PointStruct,
    SearchRequest,
    SparseIndexParams,
    SparseVectorParams,
    VectorParams,
    ScoredPoint,
)

## Creating a collection
client.create_collection(
    collection_name,
    vectors_config={
        "text-dense": VectorParams(
            size=1024,  # OpenAI Embeddings
            distance=Distance.COSINE,
        )
    },
    sparse_vectors_config={
        "text-sparse": SparseVectorParams(
            index=SparseIndexParams(
                on_disk=False,
            )
        )
    },
)

## Creating Points
points = []
for idx, (text, sparse_vector, dense_vector) in enumerate(
    zip(product_texts, sparse_vectors, dense_vectors)
):
    sparse_vector = SparseVector(
        indices=sparse_vector.indices.tolist(), values=sparse_vector.values.tolist()
    )
    point = PointStruct(
        id=idx,
        payload={
            "text": text,
            "product_id": rows[idx]["product_id"],
        },  # Add any additional payload if necessary
        vector={
            "text-sparse": sparse_vector,
            "text-dense": dense_vector,
        },
    )
    points.append(point)

## Upsert
client.upsert(collection_name, points)






def zzz_fastembed_embed_v2(wordlist: list[str], size=128, model=None) -> List:
    """pip install fastembed
    Docs:

         BAAI/bge-small-en-v1.5 384   0.13
         BAAI/bge-base-en       768   0.14
         sentence-transformers/all-MiniLM-L6-v2   0.09

        ll= list( qdrant_embed(['ik', 'ok']))

        ### https://qdrant.github.io/fastembed/examples/Supported_Models/
        from fastembed import TextEmbedding
        import pandas as pd
        pd.set_option("display.max_colwidth", None)
        pd.DataFrame(TextEmbedding.list_supported_models())

    """
    # from fastembed.embedding import FlagEmbedding as Embedding
    #
    # if model is None:
    #     model = Embedding(model_name=model_name, max_length=size)

    vectorlist = list(model.embed(wordlist))
    return vectorlist


# def zzz_test_qdrant_dense_search():  # moved to benchmark function
#     """
#         Unit test for search
#
#
#        Time performance
#
#     """
#     # create query df in ztmp directory
#     collection_name = "hf-dense-3"
#     dirtmp = "ztmp/df_search_test.parquet"
#
#     if not os.path.exists(dirtmp):
#         # df = pd_fake_data(nrows=1000, dirout=None, overwrite=False)
#         df = pd_read_file("norm/*/df_0.parquet")
#         # pick thousand random rows
#         search_df = df.sample(1000)
#         pd_to_file(search_df, dirtmp)
#     else:
#         search_df = pd_read_file(dirtmp)
#
#     model_type = "stransformers"
#     model_id = "sentence-transformers/all-MiniLM-L6-v2"  ### 384,  50 Mb
#     model = EmbeddingModel(model_id, model_type)
#
#     for i, row in search_df.iterrows():
#         # print(row)
#         id = row["id"]
#         query = row["body"][:300]
#         results = qdrant_dense_search(query, collection_name=collection_name,
#                                       model=model, topk=5)
#         top_5 = [scored_point.id for scored_point in results]
#         try:
#             assert len(results) > 0
#             assert id in top_5
#         except AssertionError:
#             log(f"Query: {query}")
#             log(f"id: {id}")
#             log(f"Top 5: {top_5}")
#             raise AssertionError

# def zzz_test_datasets_convert_kaggle_to_parquet():
#     """test function for converting Kaggle datasets to Parquet files
#     """
#     dataset_name = "gowrishankarp/newspaper-text-summarization-cnn-dailymail"
#     mapping = {"comment_text": "body", "toxic": "cat1"}
#     datasets_convert_kaggle_to_parquet(dataset_name, dirout="kaggle_datasets", mapping=mapping)
#     assert os.path.exists(f"kaggle_datasets/{dataset_name}.parquet")
#     # pd = pd_read_file(f"kaggle_datasets/{dataset_name}.parquet")
#     # print(pd.columns)


def zzz_torch_sparse_vectors_calc(texts: list, model_id: str = None):
    """Compute sparse vectors from a list of texts
    texts: list: list of texts to compute sparse vectors
    model_id: str: name of  model to use
    :return: list of tuples (indices, values) for each text


    """

    # Initialize tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForMaskedLM.from_pretrained(model_id)

    # Tokenize all texts
    tokens_batch = tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    # Forward pass through  model
    with torch.no_grad():
        output = model(**tokens_batch)

    # Extract logits and attention mask
    logits = output.logits
    attention_mask = tokens_batch["attention_mask"]

    # ReLU and weighting
    relu_log = torch.log(1 + torch.relu(logits))
    weighted_log = relu_log * attention_mask.unsqueeze(-1)

    # Compute max values
    max_vals, _ = torch.max(weighted_log, dim=1)
    # log(f"max_vals.shape: {max_vals.shape}")

    # for each tensor in  batch, get  indices of  non-zero elements
    indices_list = [torch.nonzero(tensor, as_tuple=False) for tensor in max_vals]
    indices_list = [indices.numpy().flatten().tolist() for indices in indices_list]
    # for each tensor in  batch, get  values of  non-zero elements
    values = [
        max_vals[i][indices].numpy().tolist() for i, indices in enumerate(indices_list)
    ]

    return list(zip(indices_list, values))


def zzz_torch_sparse_map_vector(cols: List, weights: List, model_id=None):
    """Extracts non-zero elements from a given vector and maps these elements to their human-readable tokens using a tokenizer.  function creates and returns a sorted dictionary where keys are  tokens corresponding to non-zero elements in  vector, and values are  weights of these elements, sorted in descending order of weights.

     function is useful in NLP tasks where you need to understand  significance of different tokens based on a model's output vector. It first identifies non-zero values in  vector, maps them to tokens, and sorts them by weight for better interpretability.

    Args:
    vector (torch.Tensor): A PyTorch tensor from which to extract non-zero elements.
    tokenizer:  tokenizer used for tokenization in  model, providing  mapping from tokens to indices.

    Returns:
    dict: A sorted dictionary mapping human-readable tokens to their corresponding non-zero weights.
    """
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    # Map indices to tokens and create a dictionary
    idx2token = {idx: token for token, idx in tokenizer.get_vocab().items()}
    token_weight_dict = {
        idx2token[idx]: round(weight, 2) for idx, weight in zip(cols, weights)
    }

    # Sort  dictionary by weights in descending order
    sorted_token_weight_dict = {
        k: v
        for k, v in sorted(
            token_weight_dict.items(), key=lambda item: item[1], reverse=True
        )
    }

    return sorted_token_weight_dict









pip install qdrant-client
pip install qdrant_openapi_client



from qdrant_client import QdrantClient
from qdrant_client.http.models import CollectionConfig, Distance, FieldIndexOperations, OptimizersConfig, WalConfig
from qdrant_openapi_client.models.models import VectorParams

# Initialize the Qdrant client with embedded mode
client = QdrantClient(embedded=True, storage_path="/path/to/storage")

# Create a collection with specific configuration
collection_name = "my_embedded_collection"
vector_dim = 128
collection_config = CollectionConfig(
    vector_size=vector_dim,
    distance=Distance.COSINE,
    optimizers_config=OptimizersConfig(
        wal=WalConfig(
            wal_capacity_mb=32,
            wal_segments_ahead=0
        )
    )
)
client.recreate_collection(collection_name, collection_config)

# Insert points into the collection
points = [
    {"id": 1, "vector": [0.1]*vector_dim, "payload": {"name": "point1"}},
    {"id": 2, "vector": [0.2]*vector_dim, "payload": {"name": "point2"}}
]
client.upsert_points(collection_name, points)

# Search for points
query_vector = [0.15]*vector_dim
search_params = {"top": 10}
results = client.search(collection_name, query_vector, search_params)

# Print search results
for result in results:
    print(f"ID: {result['id']}, Distance: {result['distance']}, Payload: {result['payload']}")

# Delete the collection
client.drop_collection(collection_name)






""" 
######### Ressources


https://medium.com/gopenai/improved-rag-with-llama3-and-ollama-c17dc01f66f6








"""



import datasets 

name="ag_news"
version=None


dataset = datasets.load_dataset(name, version,  streaming=False) 


dirdata = f"./ztmp/hf_data/"

# Save it to disk
dataset.save_to_disk(f'./ztmp/hf_data/{name}/')


# Save it to disk
dataset.save_to_disk(f'./ztmp/hf_data/{name}/', )



from datasets import load_dataset

# Load a dataset (example)
dataset = load_dataset('squad')

# Save the dataset to disk
dataset.save_to_disk('/path/to/save/dataset')

# Save only the metadata
metadata = dataset.info
with open('/path/to/save/metadata.json', 'w') as f:
    f.write(metadata.to_json())



# Save only the metadata for each split
for split_name, split in dataset.items():
    split_metadata = split.info
    with open(f'{dirdata}/{name}/{split_name}_metadata.json', 'w') as f:
        f.write(split_metadata.to_json())

from datasketch import MinHash



from datasets import load_dataset
from gcsfs import GCSFileSystem

fs = GCSFileSystem()

dataset = load_dataset(path="multi_nli", split="train")

dataset.save_to_disk("gs://YOUR_BUCKET_NAME_HERE/multi_nli/train", fs=fs)


import pandas as pd
from datasets import Dataset
import json

def save_dataset_and_metadata(df, dataset_path, metadata_path):
    # Create Hugging Face dataset from Pandas DataFrame
    dataset = Dataset.from_pandas(df)
    
    # Save the dataset to disk
    dataset.save_to_disk(dataset_path)
    
    # Extract and save metadata
    metadata = {
        'features': {k: str(v) for k, v in dataset.features.items()},
        'num_rows': dataset.num_rows,
        'num_columns': len(dataset.column_names)
    }
    
    
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)

# Example usage
df = pd.DataFrame({
    'text': ['Hello, world!', 'Machine learning is fun.'],
    'label': [1, 0]
})

save_dataset_and_metadata(df, f'{dirdata}/dataset', f'{dirdata}/metadata.json')


ds = dataset 

from utilmy import os_makedirs




def ds_to_file(ds, dirout, show=0):
   for key in ds.keys():
       dirout1 = f"{dirout}/{key}/" 
       os_makedirs(dirout1) 
       print(dirout1)
       ds[key].info.write_to_directory(f"{dirout1}/", )
       ds[key].to_parquet(f"{dirout1}/df.parquet", )


dirout= "./ztmp/hf_data/"
ds_to_file(ds, dirout)



from datasets import load_from_disk

# Load the dataset from disk
ds2 = load_from_disk(f'{dirout}/ag_news/')


dataset = load_from_disk(f'{dirout}/ztest/')

# Example usage
print(dataset)


from datasets import Dataset, DatasetDict

from utilmy import (log, loge)

def ds_read_file(dirin:str, format="parquet")->DatasetDict:

    dirin= dirin[:-1] if dirin[-1] == "/" else dirin
    dirin= dirin.replace("//","/") if ":" not in dirin else dirin 

    dsdict = DatasetDict()

    from utilmy import glob_glob
    fpaths = glob_glob(f"{dirin}/*" )

    for fp in fpaths:     
       key = fp.split("/")[-1]
       if "." in key : continue 
       flist = glob_glob(fp + f"/*.{format}")
       if flist is None or len(flist)<1:
           continue 
       log(flist[-1], len(flist))
       dsdict[key] = Dataset.from_parquet(flist)

    return dsdict



dsdict = ds_read_file(dirout +"/ztest")



# Load the dataset from a Parquet file
dataset = Dataset.from_parquet(f'{dirout}/ztest/train/df.parquet')

# Example usage
print(dataset)



# Update the MinHash object with the string


def hash_text_minhash(text:str, ksize:int=10, n_hashes:int=2):

   from datasketch import MinHash
   m = MinHash(num_perm=n_hashes)

   for k in range(0,  1+ len(text)// ksize ):
      m.update(text[k*ksize: (k+1)*ksize ].encode('utf8'))


   return m.hashvalues


def hash_text_minhash(text:str, sep=" ", ksize:int=None, n_hashes:int=2):

    from datasketch import MinHash
    m = MinHash(num_perm=n_hashes)

    if ksize is None :
        for token in text.split(sep):
            m.update(token.encode('utf8'))
    else:
        for k in range(0,  1+ len(text)// ksize ):
            m.update(text[k*ksize: (k+1)*ksize ].encode('utf8'))

    return m.hashvalues


from datasketch import MinHash

# Example arrays of hashes
hashes1 = [1, 2, 3, 4, 5]
hashes2 = [1, 2, 3, 6, 7]

# Create MinHash objects
minhash1 = MinHash(num_perm=len(hashes1))
minhash2 = MinHash(num_perm=len(hashes2))

# Update MinHash objects with the hashes
for h in hashes1:
    minhash1.update(h.to_bytes(4, byteorder='little'))

for h in hashes2:
    minhash2.update(h.to_bytes(4, byteorder='little'))

# Calculate Jaccard similarity
similarity = minhash1.jaccard(minhash2)
print(f"Jaccard similarity: {similarity}")

import numpy as np

def np_jaccard_sim(hashes1, hashes2):
    set1 = set(hashes1)
    set2 = set(hashes2)
    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    
    return intersection / union

def np_jaccard_sim(hashes1, hashes2):
    set2 = set(hashes2)
    intersection = 0
    union        = len(set1)
    for x in hashes1:
        if x in set2:
            intersection += 1
        else : 
            union += 1
            
    return intersection / union

    
    intersection = len(set1 & set2)
    union = len(set1 | set2)
    


# Example usage
hashes1 = np.array([1, 2, 3, 4, 5])
hashes2 = np.array([1, 2, 3, 6, 7])

similarity = jaccard_similarity(hashes1, hashes2)
print(f"Jaccard similarity: {similarity}")



hash_text_minhash("my very long string text ", n_hashes=4)


hash_text_minhash("my very very small string text almost equal ", n_hashes=4)


# Get the hash value
hash_value = m.digest()
print(hash_value)


from datasketch import MinHash

# Create a MinHash object with a smaller number of permutations
num_permutations = 4
m = MinHash(num_perm=num_permutations)

# Update the MinHash object with the string
string = "your_string_here"
for char in string:
    m.update(char.encode('utf8'))

# Get the list of hash values
hash_values = m.hashvalues
print(hash_values)



import xxhash



def hash_text(txt, nmax=1000):
    hash_value = xxhash.xxh64(txt[:nmax])
    return hash_value


def hash_int64(xstr:str, n_chars=10000, seed=123):
  import xxhash  
  return xxhash.xxh64_intdigest(str(xstr)[:n_chars], seed=seed)



hash_int64( "abcd", n_chars=10000)


# Example usage
long_string = "your_long_string_here"
hash_value = hash_long_string(long_string)
print(hash_value)




# Example usage
long_string = "your_long_string_here"
hash_value = hash_long_string(long_string)
print(hash_value)

