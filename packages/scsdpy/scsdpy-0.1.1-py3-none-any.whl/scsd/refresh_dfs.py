
#
# This work is licensed under THE ANTI-CAPITALIST SOFTWARE LICENSE (v 1.4) 
# To view a copy of this license, visit https://directory.fsf.org/wiki/License:ANTI-1.4

import pandas as pd
import os

output_path = os.path.join(os.path.dirname(__file__), 'data/scsd/')

from .scsd import model_objs_dict

all_motif = []
ssr_html = '<h2>Available CCDC structures by refcode for SCSD <br> Some examples may appear in multiple databases - contact C.K. for more info </h2>'
output_path = os.path.join(os.path.dirname(__file__),'data/scsd/')
for name, model in model_objs_dict.items():
    if isinstance(model.database_path, str):
        try:
            df = pd.read_pickle(output_path + model.database_path)
        except (ValueError, IndexError, FileNotFoundError):
            continue
        print(name)
        for_all = [[name, refcode] for refcode in df['name'].values.tolist()]
        # adding an index lookup
        ssr_html = ssr_html + '<h2>{}</h2> \n <p>{}</p> \n <br>'.format(name, ', '.join(["<a href = '/scsd/{0}'>{0}</a>".format(x) for x in df['name'].values.tolist()]))
        all_motif.append(for_all)

df_out = pd.DataFrame([item for sublist in all_motif for item in sublist])
df_out.columns = ['df_name', 'name']
df_out.to_pickle(output_path + 'combined_df.pkl')

f = open(f'{output_path}/scsd_structure_refcodes.html','w')
f.write(ssr_html)
f.close()
