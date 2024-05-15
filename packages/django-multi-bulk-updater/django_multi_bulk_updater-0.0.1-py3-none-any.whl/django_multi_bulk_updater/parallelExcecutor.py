from django.db import connection
import time
import concurrent.futures
from .queryChunking import QueryChunkingProcess
from django.db.models import Model
import os
from django.db.models.query import QuerySet
from django.db.models.base import ModelBase
class ParallelyQueryExcecutor(QueryChunkingProcess):
    def __init__(self, queuePoolSize:int=20) -> None:
        self.queuePoolSize = queuePoolSize

    @staticmethod
    def __processQuery(query: str) -> None:
        with connection.cursor() as cursor:
            try:
                cursor.execute("START TRANSACTION")
                cursor.execute(query)
                cursor.execute("COMMIT")
            except Exception as e:
                cursor.execute("ROLLBACK")
            finally:
                cursor.close()
                connection.close()

    def multiQueryExcecutorHandler(self, queryChunkList):
        try:
            reportAnalysis = []
            batchCounter = 1
            num_threads = min(len(queryChunkList), os.cpu_count() or 1)
            for pointer in range(0, len(queryChunkList), self.queuePoolSize):
                start_time = time.time()
                queryBucket = queryChunkList[pointer : pointer + self.queuePoolSize]
                executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)
                executor.map(
                    lambda query: self.__processQuery(query=query),
                    queryBucket,
                )
                executor.shutdown()
                reportAnalysis.append(
                    {"Batch": batchCounter, "TimeTook": time.time() - start_time}
                )
                batchCounter += 1
            return reportAnalysis
        except Exception as e:
            raise Exception(e)

    @staticmethod
    def GetProcessableResultDataType(
        result: Model | dict | None,
    ) -> Model | dict | None:
        try:
            if isinstance(result, Model):
                return Model
            elif isinstance(result, dict):
                return dict
            return None
        except Exception as e:
            raise Exception(e)

    def Multi_Parallel_Bulk_Update(
        self, yourModel: ModelBase, results: QuerySet, fields: list, batch_size: int = 50
    ):
        try:
            if not isinstance(results, QuerySet):
                raise Exception("Results should be a list")
            if not results:
                return 1
            if not isinstance(fields, list):
                raise Exception("Fields should be a list")
            if not fields:
                raise Exception("Fields should not be empty")
            if not isinstance(yourModel, ModelBase):
                raise Exception("yourModel should be an instance of Model")
            if not isinstance(batch_size, int):
                raise Exception("Batch size should be an integer")
            if batch_size <= 0:
                raise Exception("Batch size should be greater than 0")
            modelOrDictType = self.GetProcessableResultDataType(
                results[0]
            )
            return self.multiQueryExcecutorHandler(
                queryChunkList=self.GenerateChunksOfRawQuery(
                    yourModel,
                    results,
                    fields,
                    batch_size,
                    modelOrDictType=modelOrDictType,
                )
            )
        except Exception as e:
            raise Exception(e)
