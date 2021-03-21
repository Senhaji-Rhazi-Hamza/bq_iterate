# Introduction
This project serves as a BigQuery helper that allows you to query data from BigQuery, without worrying about memory limitation concerns, it makes working with BigQuery data as easy as working with lists in python

## Installation : 
```python3.8 -m pip install  bq-iterate```
## Usage
```python
from bq_iterate import BqQueryRowIterator, batchify_iterator
query = "select * from <project_id>.<dataset_id>.<table_id>"
row_itrator = BqQueryRowIterator(query=query, batch_size=2000000) #  choose a batch_size that will fit into your memory
batches = batchify_iterator(row_itrator, batch_slice=50000) #  choose a batch_slice that will fit into your memory
data = []
for batch in batches:
    # do your batch processing here
    data.append(len(batch))
print(sum(data))
```

## What happens behind the scenes :

**bq_iterate provide two functionalities :**

* 2 classes BqQueryIterator and BqTableRowIterator, they behave like an iterator, where they hold only <batch_size> elements in memory and when you want to access the element <batch_size + 1> the iterator calls in memory the next batch_size + 1 elements

* A function batchify_iterator, what this function does, it takes an iterator and yields slices of it, the <batch_slice> can be bigger than the <batch_size> even if by common sens it's supposed to be smaller, it doesn't matter, since batchify_iterator will create in memory at each batch it yields, a list of <batch_slice> elements, once the batch consumed it freed from memory, since it's a generator
