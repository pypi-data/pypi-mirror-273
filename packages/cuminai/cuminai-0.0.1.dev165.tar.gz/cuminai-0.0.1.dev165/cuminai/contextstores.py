import os
from typing import (
    Any, 
    Optional
)

import chromadb
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_core.embeddings import Embeddings
from chromadb.api.models import Collection
from cuminai.constants import (
    _CUMINAI_DUMMY_TENANT_NAME,
    _CUMINAI_DUMMY_DATABASE_NAME,
    _CUMINAI_DUMMY_COLLECTION_NAME,
    _CUMINAI_API_KEY_ENV,
    _CUMINAI_HOST,
)

class CuminAI:
    """`Cumin AI context store

    To use, you should have the ``chromadb`` python package and ``langchain-chroma`` python package installed.

    Example:
        .. code-block:: python

                from cuminai import CuminAI

                embeddings = OpenAIEmbeddings()
                contextsource = CuminAI("cuminai_source", embeddings)
    """

    def __init__(
            self,
            source: str,
            embedding_function: Optional[Embeddings] = None
    ) -> None:
        """Initialize with a Cumin AI client"""
        if source is None:
            raise ValueError("No context source present.")
        api_key = os.getenv(_CUMINAI_API_KEY_ENV)
        if api_key is None:
            raise ValueError("Cumin AI api key not set in env.")
        
        self._embedding_function = embedding_function
        
        try:
            self._client = chromadb.HttpClient(host=_CUMINAI_HOST, 
                                        port=443, 
                                        tenant=_CUMINAI_DUMMY_TENANT_NAME, 
                                        database=_CUMINAI_DUMMY_DATABASE_NAME, 
                                        ssl=True, 
                                        headers={
                                            "CUMINAI-API-KEY": api_key,
                                            "CUMINAI-ALIAS": source
                                        }
            )
        except ValueError:
            raise ValueError(f"Could not connect to {source}. Please make sure the source exists or the Cumin AI API key is valid.")

    def as_retriever(self, **kwargs: Any) -> VectorStoreRetriever:
        store = Chroma(
            client=self._client,
            collection_name=_CUMINAI_DUMMY_COLLECTION_NAME,
            embedding_function=self._embedding_function,
            create_collection_if_not_exists=False,
        )

        return store.as_retriever(**kwargs)