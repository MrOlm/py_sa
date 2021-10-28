# py_sa

py_sa is a way to interact with aegea and s3 through python

# Example mapping

```angular2html
import importlib
importlib.reload(py_sa)

import py_sa
import py_sa.aegea_cmds

rdb = py_sa.load_running_aegea()
s3_store_folder = 's3://czbiohub-microbiome/Sonnenburg_Lab/InfantMicrobiome/B_longum/mapping/'
index_loc = 's3://czbiohub-microbiome/Sonnenburg_Lab/InfantMicrobiome/B_longum/Bifidobacterium_longum_subsp_infantis_ATCC_15697.fna.fa.bt2'

for i, row in PXdb.iterrows():
    cmd, result = py_sa.aegea_cmds.make_mapping_command(row['r1'], row['r2'], 'junk', 
                            s3_store_folder, index_location=index_loc,
                            output_type='BAM', ret_result=True)
    py_sa.submit_aegea_job(cmd, result, verbose=True, rdb=rdb)
    break
```