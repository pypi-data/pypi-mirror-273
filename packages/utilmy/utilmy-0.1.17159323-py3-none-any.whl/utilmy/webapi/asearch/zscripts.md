```bash



############################################################################################
### Generate Prompt, query from Answers using GPT-3.5

  ### generate prompt via DSPy
     python query.py prompt_find_best --dirdata "./ztmp/bench/norm/"  --dataset "ag_news"  --dirout ./ztmp/exp  

          --> Add 1 prompt to PromptStorage Saved in ztmp/prompt_hist.csv
          --> Pick up manually promptid from ztmp/prompt_hist.csv


  ### Generate synthetic from specific Prompt-id (using default promptStorage path)
     python query.py generator_syntheticquery --dataset "ag_news" --nfile 70 --nquery 100 --prompt_id "20240507-671"

          -->  saves queries in ztmp/bench/ag_news/query/df_synthetic_queries_{dt}.parquet

          export dirquery="ztmp/bench/ag_news/query/df_synthetic_queries_20240509_171632.parquet" 



############################################################################################
###### Benchmark Engine  ###################################################################
    alias pybench=" python3 -u bench.py ";
    function echo2() { echo -e "$1" >> zresults.md; }


#### Prepare parquet data to feed Engine Indexes 
   # pybench bench_v1_data_convert  --dirin "./ztmp/hf_dataset/ag_news/"    --dirout "./ztmp/bench/ag_news"


#### Create Engine Indexes for later retrieval
   dataset=="ag_news"
   dirdata="ztmp/bench"

   ### Load data from f"ztmp/bench/norm/ag_news/" 
   pybench bench_v1_create_sparse_indexes  --dirdata_root $dirdata

   pybench bench_v1_create_dense_indexes   --dirdata_root $dirdata

   pybench bench_v1_create_tantivy_indexes --dirdata_root $dirdata



#### Generate bechnmark of retrieval engine using query file.

    dirquery="ztmp/bench/ag_news/query/df_synthetic_queries_20240509_171632.parquet" 

    echo2 `date`
    echo2 "\`\`\`" ;

    echo2 "### dense run"
    pybench bench_v1_dense_run   --dirquery $dirquery  >> zresults.md

    
    echo2 "### sparse run"
    pybench bench_v1_sparse_run  --dirquery $dirquery  >> zresults.md;
    
    echo2 "### tantivy run"
    pybench bench_v1_tantivy_run --dirquery $dirquery  >> zresults.md;


    echo2 "\`\`\`"
    echo2 "---" 



#### Create Analysis report
    pybench create_error_report --dirin "ztmp/bench/"  --dataset $dataset --dirquery $dirquery 




```