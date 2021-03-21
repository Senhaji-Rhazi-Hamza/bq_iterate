import logging
from google.cloud import bigquery

from bq_iterate.retry import default_retry

class BqRowIterator:
    client = None

    def __init__(self,  batch_size=10000, client=None):
        self.batch_size = batch_size
        self.initialized = False
        self.nth_batch = 0
        if self.__class__.client is None:
            self.__class__.client = bigquery.Client() if (client is None)  else client

    def __iter__(self):
        return self

    def __next__(self):
        if not self.initialized:
            self.initialize()
            return next(self.row_iterator)
        if (el := next(self.row_iterator, None)) :
            return el
        elif self.row_iterable.next_page_token is None:
            raise StopIteration
        else:
            self.call_next_batch()
            return next(self.row_iterator)

    @default_retry
    def call_next_batch(self):
        page_token = (
            self.row_iterable.next_page_token if hasattr(self, "row_iterable") else None
        )
        logging.info(
            f"""calling bq client list_rows with batch size : {self.batch_size}
            batch number :{self.nth_batch} with page_token :{page_token or "None"}"""
        )
        self.row_iterable = self.list_next_rows(page_token)
        self.row_iterator = iter(self.row_iterable)
        self.nth_batch += 1

    @classmethod
    def update_client(cls, client):
      cls.__class__.client = client

    def list_next_rows(self, page_token= None):
        pass

    def initialize(self):
        self.call_next_batch()
        self.initialized = True


class BqQueryRowIterator(BqRowIterator):

    def __init__(self,  query, batch_size=10000, client=None):
        self.query = query
        super().__init__(batch_size,  client=client)
        self.query_job = self.client.query(query)

    def list_next_rows(self, page_token= None):
        return self.client.list_rows(
            self.query_job.destination,
            max_results=self.batch_size,
            page_token=page_token,
        )


class BqTableRowIterator(BqRowIterator):

    def __init__(self, project_id, dataset_id, table_id, batch_size=10000, client=None):
        self.project_id = project_id
        self.dataset_id = dataset_id
        self.table_id = table_id
        super().__init__(batch_size=batch_size, client=client)

    def list_next_rows(self, page_token=None):
        try:
            return self.client.list_rows(
                f"{self.project_id}.{self.dataset_id}.{self.table_id}",
                max_results=self.batch_size,
                page_token=page_token,
            )
        except Exception as e:
          logging.error(f'something wrong happend : {e}')
          raise
