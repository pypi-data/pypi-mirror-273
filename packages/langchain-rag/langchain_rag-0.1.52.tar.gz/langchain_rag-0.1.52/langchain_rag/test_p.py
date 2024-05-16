from langchain_community.indexes.base import RecordManager

from langchain_rag.patch_langchain_community.indexes._sql_record_manager import (
    SQLRecordManager,
)

x: RecordManager = SQLRecordManager(namespace="", engine=None, async_mode=True)
