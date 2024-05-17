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

## For Creators
Publishing knowledge is simple with Cumin AI. Currently we support the following knowledge types:
- Links - scrapable URLs can be given as input

To upload knowledge to Cumin AI, the creators must first create a `CUMINFILE.yaml` in their project directory.

Sample CUMINFILE.yaml for getting started:
```yaml
name: "<name of knowledge source>"
kind: LINK
version: 1
type: PUBLIC
embedding: ollama/nomic-embed-text:v1.5
tag:
    type: global
chunkstrategy:
    size: 1024
    overlap: 100
knowledge:
    - link: "<enter url for first link source>"
    - link: "<enter url for second link source>"
    - link: "<enter url for third link source>"
```

Then make sure you have latest version of cuminai
```bash
pip install cuminai
```

Subsequently login into Cumin AI using your username and api key obtained from Cumin AI dashboard. 
```bash
cuminai login --username <username> --apikey <Cumin AI API Key>
```

once you have authenticated, go to the project directory and validate your `CUMINFILE.yaml` by running the following command from your terminal
```bash
cuminai validate
```

then once the validation is successful, you can deploy your knowledge to Cumin AI using the below command
```bash
cuminai deploy
```

Post deployment your knowledge will be available for Cumin AI users at
```
@<username>/<name of knowledge source>
```

this knowledge source can be accessed in python
```python
# Access Cumin AI Client
from cuminai import CuminAI

embedding =  ... # use a LangChain Embeddings class

client = CuminAI(
    source="@<username>/<name of knowledge source>",
    embedding_function = embedding
)
```

you can logout of Cumin AI by typing the below on your terminal
```
cuminai logout
```

## Release
Currently Cumin AI is in `pre-release` mode. We have exciting things planned. You can check out our [roadmap](https://roadmap.cuminai.com) to know more.

## License
[Apache 2.0](./LICENSE)