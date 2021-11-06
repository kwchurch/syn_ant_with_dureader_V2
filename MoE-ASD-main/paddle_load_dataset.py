
import pdb

def read_row(data_path):
    label_symbol_table = {'0' : 'synonym', '1' : 'antonym'}
    with open(data_path, 'r', encoding='utf-8') as f:
        next(f)
        for line in f:
            # print(line)
            # pdb.set_trace()
            id,word1,word2,antmorph,gold = line.strip('\n').split(',')
            yield {'id' : id, 'question': word1, 'answer': word2, 'antmorph': antmorph, 'labels': int(gold) }

import paddlenlp
from paddlenlp.datasets.dataset import load_dataset
dir='/mnt/home/kwc/morphology/MoE-ASD-main/dataset_csv/'
pos='adjective'

train_ds = load_dataset(read_row, data_path=dir + 'tag-' + pos + '-pairs.train.csv', lazy=False)
dev_ds = load_dataset(read_row, data_path=dir + 'tag-' + pos + '-pairs.val.csv', lazy=False)
test_ds = load_dataset(read_row, data_path=dir + 'tag-' + pos + '-pairs.test.csv', lazy=False)

print('len(train_ds): ' + str(len(str(train_ds))))
print('len(dev_ds): ' + str(len(str(dev_ds))))
print('len(test_ds): ' + str(len(str(test_ds))))

pdb.set_trace()
