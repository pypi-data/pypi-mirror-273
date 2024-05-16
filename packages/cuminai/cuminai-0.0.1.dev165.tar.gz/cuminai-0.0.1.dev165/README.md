# cuminai

This package contains the Cumin AI Python SDK. Cumin AI is a Managed LLM Context Service. This package provides integration with Langchain.

## Installation

```bash
pip install cuminai
```

In the rare scenario, if you are on Windows, and you get `File Too Long` error for any dependency package while installing `cuminai`. Run the below command to fix it.
```bash
git config --global core.longpaths true
```

## Usage

The `cuminai` class helps easily access the Cumin AI Context store.

```python
# Setup API key
import os
from getpass import getpass

CUMINAI_API_KEY = getpass("Enter Cumin AI API Key: ")
os.environ["CUMINAI_API_KEY"] = CUMINAI_API_KEY
```

```python
# Access Cumin AI Client
from cuminai import CuminAI

embedding =  ... # use a LangChain Embeddings class

client = CuminAI(
    source="<Cumin AI Context Source>",
    embedding_function = embedding
)
```

```python
# Get Langchain retreiver for Appending to Chain.
num_docs_to_retrieve = ... # number of docs to retrieve. Defaults to 4
retriever = client.as_retriever(search_kwargs={"k": num_docs_to_retrieve})
```

## Release
Currently Cumin AI is in `pre-release` mode. We have exciting things planned. You can check out our [roadmap](https://roadmap.cuminai.com) to know more.

## License
[Apache 2.0](./LICENSE)