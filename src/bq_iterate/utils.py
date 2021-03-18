
from collections.abc import Iterable, Iterator

from bq_iterate.config import logging


def batchify_iterator(iterator, batch_slice=100):

    batchify_iterator.batch_count = 0

    if isinstance(iterator, Iterable) and not isinstance(iterator, Iterator):
        iterator = iter(iterator)
    elif not isinstance(iterator, Iterator):
        raise Exception(f"{type(iterator)} not iterable")

    while (el := next(iterator, None)) is not None:

        batchify_iterator.batch_count += 1

        logging.info(
            f"""yielding the {batchify_iterator.batch_count}th batch
            for a batch slice {batch_slice}"""
        )
        yield [el] + \
              [
                  el for _ in range(batch_slice - 1)
                  if (el := next(iterator, None))
              ]
    batchify_iterator.batch_count = 0

def bq_row_to_dict(bq_row):
    return {k: v for k, v in bq_row.items()}
