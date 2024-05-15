from django.db.models import Model


class QueryConvertor:
    @staticmethod
    def GetUpdateClauseByTableName(yourModel: Model) -> tuple:
        try:
            meta = yourModel._meta
            return f"UPDATE `{meta.db_table}` SET ", meta.db_table, meta.pk.name
        except Exception as e:
            raise e

    @staticmethod
    def GetSetInitiateValue(columnName: str) -> str:
        return f" `{columnName}` = CASE "

    @staticmethod
    def SetValuesByColumnName(
        tableName: str, value, primaryColumnName: str, primaryKey: int, fieldType
    ) -> str:
        try:
            if value is None:
                return f" WHEN (`{tableName}`.`{primaryColumnName}` = {primaryKey}) THEN NULL "
            if fieldType == "DateTimeField" or fieldType == "CharField":
                return f" WHEN (`{tableName}`.`{primaryColumnName}` = {primaryKey}) THEN '{value}' "
            if (
                fieldType == "IntegerField"
                or fieldType == "FloatField"
                or fieldType == "DecimalField"
            ):
                return f" WHEN (`{tableName}`.`{primaryColumnName}` = {primaryKey}) THEN {value} "
            return f" WHEN (`{tableName}`.`{primaryColumnName}` = {primaryKey}) THEN '{value}' "
        except Exception as e:
            raise e

    @staticmethod
    def GetEnclosedQueryOperand():
        try:
            return " ELSE NULL END "
        except Exception as e:
            raise e

    @staticmethod
    def GetValuesByColumnName(
        columnName: str, row: dict | Model, modelOrDictType: dict | Model
    ) -> str | None | int | float | bool:
        try:
            if modelOrDictType == dict:
                return row[columnName]
            return getattr(row, columnName, None)
        except Exception as e:
            raise e
