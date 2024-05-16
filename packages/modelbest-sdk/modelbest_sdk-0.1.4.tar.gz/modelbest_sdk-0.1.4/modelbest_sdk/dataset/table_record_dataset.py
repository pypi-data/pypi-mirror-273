import torch
from modelbest_sdk.dataset.batched_dataset import BatchedDataset
from modelbest_sdk.dataset.cuda_prefetcher import CudaPrefetcher
from modelbest_sdk.dataset.megatron.segment_dataset import SegmentDataset
from modelbest_sdk.dataset.thrift_wrapper.dataset_checkpoint import DatasetInfoList
from modelbest_sdk.dataset.thrift_wrapper.dataset_context import DatasetContext
from modelbest_sdk.dataset.weighted_dataset import WeightedDataset

class BaseTableRecordDataset(torch.utils.data.IterableDataset):
    def __init__(self, context: DatasetContext, batch_size=1, max_len=4096, prefetch_chunk_cnt=20, chunk_size=1024, num_workers=1, prefetch_factor=20, cuda_prefetch=True):
        self.context = context
        self.context.num_workers = num_workers
        dataset_info_list = DatasetInfoList.load_from_file(context.dataset_config_path)
        
        self.weighted_dataset = WeightedDataset(context=context, dataset_info_list=dataset_info_list, prefetch_chunk_cnt=prefetch_chunk_cnt, chunk_size=chunk_size)
        self.setup_dataset(context, batch_size, max_len)
        
        self.dataloader = torch.utils.data.DataLoader(dataset=self.dataset, batch_size=batch_size, num_workers=num_workers, prefetch_factor=prefetch_factor, collate_fn=self.dataset_collate_fn())
        self.cuda_prefetch = cuda_prefetch
        
        if self.cuda_prefetch:
            self.cuda_prefetcher = CudaPrefetcher(context, self.dataloader)

    def setup_dataset(self, context, batch_size, max_len):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def dataset_collate_fn(self):
        raise NotImplementedError("This method should be overridden by subclasses.")

    def __iter__(self):
        prefetcher = self.cuda_prefetcher if self.cuda_prefetch else self.dataloader
        for batch in prefetcher:
            yield batch

class SegmentTableRecordDataset(BaseTableRecordDataset):
    def setup_dataset(self, context, batch_size, max_len):
        self.dataset = SegmentDataset(context=context, weighted_dataset=self.weighted_dataset, max_len=max_len)
    
    def dataset_collate_fn(self):
        return SegmentDataset.collate_fn

class BatchedTableRecordDataset(BaseTableRecordDataset):
    def setup_dataset(self, context, batch_size, max_len):
        self.dataset = BatchedDataset(context=context, weighted_dataset=self.weighted_dataset, batch_size=batch_size, max_len=max_len)
    
    def dataset_collate_fn(self):
        return BatchedDataset.collate_fn
