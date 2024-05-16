from collections import defaultdict
import numpy as np
import torch

# from modelbest_sdk.dataset.collater.collater import Collater
from modelbest_sdk.dataset.weighted_dataset import WeightedDataset
from modelbest_sdk.dataset.thrift_wrapper.base_doc import BaseDoc
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import *
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext

def default_factory_list():
    return list()

def default_factory_dict():
    return defaultdict(default_factory_list)

class SegmentDataset(torch.utils.data.IterableDataset):
    def __init__(self, context, weighted_dataset, max_len, drop_last=False):
        self.context = context
        self.weighted_dataset = weighted_dataset
        self.max_len = max_len
        self.drop_last = drop_last
        
        self.buffer = []
        self.current_length = 0
        
    def __iter__(self):
        for data in self.weighted_dataset:
            while self.current_length > self.max_len:
                yield self.pop()
            self.put(data)
        while self.buffer:
            yield self.pop()
    
    def put(self, data):
        self.buffer.append(data)
        self.current_length += len(data['doc'].token_ids)
    
    def pop(self):
        tokens = torch.zeros((self.max_len + 1), dtype=torch.int32)
        mask = torch.zeros((self.max_len + 1), dtype=torch.bool)
        attention_mask = torch.tril(
            torch.ones((self.max_len, self.max_len))
        ).unsqueeze(0) < 0.5
        position_ids = torch.arange((self.max_len), dtype=torch.int32)
        indexes = defaultdict(default_factory_dict)        

        remaining_seq_length = self.max_len + 1
        begin = 0
        while self.buffer and remaining_seq_length > 0:
            data = self.buffer.pop(0)
            doc: BaseDoc = data['doc']
            index = data['index']
            chunk = data['chunk']
            dataset_idx = data['dataset_idx']
            indexes[int(dataset_idx)][chunk].append(index)

            if remaining_seq_length > len(doc.token_ids):
                end = begin + len(doc.token_ids)
                doc_to_fill = doc
                
            else:
                end = begin + remaining_seq_length
                doc1, doc2 = doc.split(remaining_seq_length)
                doc_to_fill = doc1
                self.buffer.insert(0, {'doc': doc2, 'chunk': data['chunk'], 'index': data['index'], 'dataset_idx': data['dataset_idx']})
                self.current_length += 1
            
            tokens[begin:end] = torch.tensor(doc_to_fill.token_ids, dtype=torch.int32)
            mask[begin:end] = torch.tensor(doc_to_fill.mask, dtype=torch.bool)
            remaining_seq_length -= len(doc_to_fill.token_ids)
            self.current_length -= len(doc_to_fill.token_ids)
            begin = end
        if remaining_seq_length > 0 and self.drop_last:
            raise StopIteration
        return {
            'tokens': tokens[:-1],
            'labels': tokens[1:],
            'loss_mask': ~mask[1:],
            'attention_mask': attention_mask,
            'position_ids': position_ids,
            'indexes': indexes
        } 
    
    def collate_fn(batch):
        # 'batch' 是一个列表，其中包含所有 `__getitem__` 的返回值
        # 初始化一个字典来存储所有批处理后的数据
        batched_data = {k: [] for k in batch[0]}
        
        # 遍历批次中的每个样本
        for item in batch:
            for key in item:
                batched_data[key].append(item[key])

        # 对于可以直接转换为张量的数据，使用 torch.stack
        for key in ['tokens', 'labels', 'loss_mask', 'attention_mask', 'position_ids']:
            batched_data[key] = torch.stack(batched_data[key])

        # 对于 'indexes' 这样的复杂结构，保持原样或根据需要处理
        # 这里我们保持它作为一个列表
        batched_data['indexes'] = batched_data['indexes'][0]
        return batched_data
            
if __name__ == '__main__':
    context = DatasetContext(world_size=1, rank=0, num_workers=1)
    context.world_size = 8
    context.rank = 6
    dataset_info_list = [
        DatasetInfo(
            path="/home/emr-user/modelbest_sdk/example/mbtable_data/base_doc_simple",
            weight=1,
            max_epoch=1
        )
    ]
    
    dataset_info_list = DatasetInfoList(dataset_info_list)
    
    w_dataset = WeightedDataset(
        context=context,
        dataset_info_list=dataset_info_list
    )
    
    dataset = SegmentDataset(
        context=context,
        weighted_dataset=w_dataset,
        max_len=16
    )
    
    dataloader = torch.utils.data.DataLoader(
        dataset,
        batch_size=2,
        collate_fn=SegmentDataset.collate_fn
    )
    i = 0
    for data in dataloader:
        print(data)
    
