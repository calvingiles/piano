import os
import pandas as pd
out = {}
for filename in os.listdir('./data'):
    try:
        parts = filename.split('.')
        if len(parts) != 7:
            raise IndexError
        else:
            filename_parts = parts
        out[parts[-3],parts[-2]] = pd.read_csv('data/{}'.format(filename),header=None,index_col=0)
        if len(out.keys()) == 1:
            single = pd.DataFrame(out[parts[-3],parts[-2]]).copy()
        single['{}.{}'.format(parts[-3],parts[-2])] = pd.DataFrame(out[parts[4],parts[5]])
    except IndexError:
        #not the right file.
        pass
del single[1]
single.to_csv('./data/{}'.format('.'.join(filename_parts[:-3]+ filename_parts[-1:])),index_label='Frequency')