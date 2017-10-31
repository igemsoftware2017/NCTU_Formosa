import json
import numpy
# read json to np_array
def json_read(data_str,sort_list=None):
    data = json.loads(data_str)
    if sort_list:
        out_array=None
        for key in sort_list:
            if key not in sorted(data) : continue
            features = np.array([float(n) for n in data[key]],type=np.float32)
            if out_array:
                out_array = features
            else:
                out_array = np.vstack([out_array,features]).T
        return out_array
    else:
        return data

def json_write(dic):
    data_str = json.dumps(dic)
    return data_str