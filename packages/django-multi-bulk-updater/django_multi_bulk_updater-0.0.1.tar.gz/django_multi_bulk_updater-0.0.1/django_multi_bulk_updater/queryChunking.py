from .queryConvertor import QueryConvertor
from django.db.models import Model
import concurrent.futures
import os

class QueryChunkingProcess(QueryConvertor):
    @staticmethod
    def GetUpdateAblePrimaryIDs(results: list, primaryColumnName: str, modelOrDictType:str="Model") -> tuple:
        try:
            if modelOrDictType == dict:
                return tuple(row[primaryColumnName] for row in results)
            return tuple(getattr(row, primaryColumnName) for row in results)
        except Exception as e:
            raise Exception(e)

    @classmethod
    def SetUpdateValueKeyWise(
        cls,
        results: list,
        columnName: str,
        tableName: str,
        primaryColumnName,
        fieldType,
        modelOrDictType: str = "Model",
    ) -> str:
        try:
            queryResult = cls.GetSetInitiateValue(columnName=columnName)
            for _, row in enumerate(results):
                queryResult += cls.SetValuesByColumnName(
                    tableName=tableName,
                    value=cls.GetValuesByColumnName(
                        columnName=columnName, row=row, modelOrDictType=modelOrDictType
                    ),
                    primaryColumnName=primaryColumnName,
                    primaryKey=cls.GetValuesByColumnName(
                        columnName=primaryColumnName,
                        row=row,
                        modelOrDictType=modelOrDictType,
                    ),
                    fieldType=fieldType,
                )
            queryResult += cls.GetEnclosedQueryOperand()
            return queryResult
        except Exception as e:
            raise Exception(e)

    @classmethod
    def GenerateChunksOfRawQuery(
        cls,
        yourModel: Model,
        results: list,
        fields: list,
        batch_size: int,
        modelOrDictType: str = "Model",
    ) -> list:
        try:
            queryResultChunkList = []
            (
                queryResultTemplate,
                tableName,
                primaryColumnName,
            ) = cls.GetUpdateClauseByTableName(yourModel=yourModel)
            num_threads = min(len(fields), os.cpu_count() or 1)
            for index in range(0, len(results), batch_size):
                processOn = results[index : index + batch_size]
                queryResult = queryResultTemplate
                executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)
                future_results = executor.map(
                    lambda field: cls.SetUpdateValueKeyWise(
                        results=processOn,
                        columnName=field,
                        tableName=tableName,
                        primaryColumnName=primaryColumnName,
                        fieldType=yourModel._meta.get_field(
                            field_name=field
                        ).get_internal_type(),
                        modelOrDictType=modelOrDictType,
                    ),
                    fields,
                )
                queryResult += " , ".join(future_results)
                executor.shutdown()
                queryResultChunkList.append(
                    queryResult
                    + " WHERE `{tableName}`.`{primaryColumnName}` IN {primaryIds}".format(
                        tableName=tableName,
                        primaryColumnName=primaryColumnName,
                        primaryIds=cls.GetUpdateAblePrimaryIDs(
                            results=processOn, primaryColumnName=primaryColumnName, modelOrDictType=modelOrDictType
                        ),
                    )
                )
                queryResult = ""
            return queryResultChunkList
        except Exception as e:
            raise Exception(e)

    def Parallel_Bulk_Update(
        self, yourModel: Model, results: list, fields: list, batch_size: int
    ):
        try:
            self.GenerateChunksOfRawQuery(yourModel, results, fields, batch_size)
        except Exception as e:
            raise Exception(e)
