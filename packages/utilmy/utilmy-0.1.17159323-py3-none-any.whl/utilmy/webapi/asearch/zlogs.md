# kg query benchmarking
```bash
# pyinstrument  engine_kg.py kg_benchmark_queries --dirin ztmp/kg/data/agnews_kg_question.csv --dirout ztmp/kg/data/agnews_kg_benchmark.csv --queries=5
#ztmp/kg/data/agnews_kg_benchmark.csv
                                            question  ...        dt
0  What is the relationship between Turner and Fe...  ...  2.298924
1                What is the capital city of Canada?  ...  1.432849
2  What is the connection between protein and ami...  ...  2.166291
3  Who founded the Prediction Unit Helps Forecast...  ...  1.930334
4  What jurisdiction does the smog-fighting agenc...  ...  1.739533

[5 rows x 3 columns]
Average time taken: 1.91 seconds

  _     ._   __/__   _ _  _  _ _/_   Recorded: 20:31:12  Samples:  6916
 /_//_/// /_\ / //_// / //_'/ //     Duration: 19.191    CPU time: 11.769
/   _/                      v4.6.2

Program: /home/ankush/workplace/fl_projects/myutil/.venv/bin/pyinstrument engine_kg.py kg_benchmark_queries --dirin ztmp/kg/data/agnews_kg_question.csv --dirout ztmp/kg/data/agnews_kg_benchmark.csv --queries=5

19.185 <module>  engine_kg.py:1
├─ 10.191 Fire  fire/core.py:81
│     [3 frames hidden]  fire
│        10.139 _CallAndUpdateTrace  fire/core.py:661
│        └─ 10.138 kg_benchmark_queries  engine_kg.py:502
│           ├─ 9.568 kg_db_query  engine_kg.py:438
│           │  ├─ 9.101 wrapper  llama_index/core/instrumentation/dispatcher.py:258
│           │  │     [69 frames hidden]  llama_index, tenacity, openai, httpx,...
│           │  │        4.789 _SSLSocket.read  <built-in>
│           │  │        3.902 _SSLSocket.read  <built-in>
│           │  └─ 0.311 KnowledgeGraphIndex.from_documents  llama_index/core/indices/base.py:105
│           │        [10 frames hidden]  llama_index, tiktoken, tiktoken_ext
│           └─ 0.382 pd_to_file  utilmy/ppandas.py:585
│              └─ 0.359 collect  <built-in>
├─ 4.273 <module>  spacy/__init__.py:1
│     [27 frames hidden]  spacy, thinc, torch, <built-in>, conf...
├─ 2.399 <module>  llama_index/core/__init__.py:1
│     [39 frames hidden]  llama_index, openai, llama_index_clie...
├─ 1.957 <module>  spacy_component.py:1
│  └─ 1.892 _LazyModule.__getattr__  transformers/utils/import_utils.py:1494
│        [46 frames hidden]  transformers, importlib, accelerate, ...
└─ 0.331 <module>  query.py:1
   └─ 0.320 <module>  dspy/__init__.py:1
         [6 frames hidden]  dspy, dsp, datasets

To view this report with different options, run:
    pyinstrument --load-prev 2024-05-14T20-31-12 [options]
```
# 15 May
```
# pykg kg_benchmark_queries --dirin ztmp/kg/data/agnews_kg_questions2.csv --dirout ztmp/kg/data/agnews_kg_benchmark2.csv --queries=20
ztmp/kg/data/agnews_kg_benchmark2.csv
                                             question  ... is_correct
0   Who founded the Prediction Unit that helps for...  ...      False
1   What jurisdiction does the smog-fighting agenc...  ...       True
2   What is an example of an instance of an open l...  ...       True
3                   What product does Sophos produce?  ...       True
4    How is FOAF used in the concept of web-of-trust?  ...       True
5   How does phishing relate to E-mail scam in ter...  ...       True
6    In which country is the Card fraud unit located?  ...       True
7   What type of product or material does STMicroe...  ...       True
8                  Who is the developer of Final Cut?  ...       True
9   Where is the headquarters of Free Record Shop ...  ...      False
10  Which country is the city of Melbourne located...  ...       True
11  How do socialites unite dolphin groups in term...  ...       True
12                 In what instance did the teenage T  ...      False
13  What is Ganymede an instance of within our sol...  ...       True
14  Which space agency operates the Mars Express s...  ...       True

[15 rows x 4 columns]
 Average time taken: 1.97 seconds
 Percentage accuracy: 80.00 %







 
```
# Llama index graph query logs
```
# pykg kg_db_query --space_name "agnews_kg_relation" --query "Which country is the city of Melbourne located in?"

HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
** Messages: **
user: A question is provided below. Given the question, extract up to 10 keywords from the text. Focus on extracting the keywords that we can use to best lookup answers to the question. Avoid stopwords.
---------------------
Which country is the city of Melbourne located in?
---------------------
Provide keywords in the following comma-separated format: 'KEYWORDS: <keywords>'

**************************************************
** Response: **
assistant: KEYWORDS: country, city, Melbourne, located
**************************************************


Index was not constructed with embeddings, skipping embedding usage...
HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
** Messages: **
system: You are an expert Q&A system that is trusted around the world.
Always answer the query using the provided context information, and not prior knowledge.
Some rules to follow:
1. Never directly reference the given context in your answer.
2. Avoid statements like 'Based on the context, ...' or 'The context information ...' or anything along those lines.
user: Context information is below.
---------------------
kg_schema: {'schema': "Node properties: [{'tag': 'entity', 'properties': [('name', 'string')]}]\nEdge properties: [{'edge': 'relationship', 'properties': [('relationship', 'string')]}]\nRelationships: ['(:entity)-[:relationship]->(:entity)']\n"}

The following are knowledge sequence in max depth 2 in the form of directed graph like:
`subject -[predicate]->, object, <-[predicate_next_hop]-, object_next_hop ...`
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- Virgin Blue{name: Virgin Blue}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- CANBERRA{name: CANBERRA}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- Dow Jones{name: Dow Jones}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- Sons Of Gwalia{name: Sons Of Gwalia}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country of citizenship}]- Jana Pittman{name: Jana Pittman}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- Australia Police to Trap Cyberspace Pedophiles{name: Australia Police to Trap Cyberspace Pedophiles}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: member of sports team}]- Andrew Symonds{name: Andrew Symonds}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country of citizenship}]- Nathan Baggaley{name: Nathan Baggaley}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- Sons of Gwalia{name: Sons of Gwalia}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- Seven Network Ltd{name: Seven Network Ltd}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- PERTH{name: PERTH}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country of citizenship}]- Rod Eddington{name: Rod Eddington}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- Qantas Airways{name: Qantas Airways}
Melbourne{name: Melbourne} -[relationship:{relationship: country}]-> Australia{name: Australia} <-[relationship:{relationship: country}]- SYDNEY{name: SYDNEY}
---------------------
Given the context information and not prior knowledge, answer the query.
Query: Which country is the city of Melbourne located in?
Answer: 
**************************************************
** Response: **
assistant: Australia
**************************************************


Australia
```