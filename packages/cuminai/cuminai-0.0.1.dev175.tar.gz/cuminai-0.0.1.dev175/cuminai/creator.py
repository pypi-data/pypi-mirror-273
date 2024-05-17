import os
import click
from pathlib import Path
import http.client
import yaml
from cuminai.constants import (
    _CUMINAI_CONFIG_DIR,
    _CUMINAI_CONFIG_FILE,
    _CUMINAI_CREATOR_HOST,
    _CUMIN_FILE_NAME,
    _CUMINAI_DUMMY_TENANT_NAME,
    _CUMINAI_DUMMY_DATABASE_NAME,
    _LINK_KIND,
    _PUBLIC_VISIBILITY,
    _PRIVATE_VISIBILITY,
    _GLOBAL_TAGGING,
    _LOCAL_TAGGING,
    _DEFAULT_CHUNK_SIZE,
    _DEFAULT_CHUNK_OVERLAP
)

import cuminai.validator as validator

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
import chromadb

@click.group()
def executor():
    pass

@executor.command(help='Log in to a Cumin AI managed knowledge store')
@click.option('-u', '--username',  help='username', required=True)
@click.option('-k', '--apikey', help='api key', required=True)
def login(username, apikey):
    username = username.strip()
    apikey = apikey.strip()
    
    if not validator.UsernameValidator.match(username):
        click.echo("username must be an alphanumeric between 6 and 36 characters")
        return

    if apikey == "":
        click.echo("apikey can't be empty")
        return

    # validate the client credentials from Cumin AI
    connection = http.client.HTTPSConnection("api.creator.cuminai.com", timeout=10)
    connection.request("GET", "/v1/creator/auth/verify", headers={
        "CUMINAI-API-KEY": apikey,
        "CUMINAI-CLIENT-ID": username
    })
    response = connection.getresponse()
    if response.status != 200:
        click.echo("Login failed: invalid client credentials. please try again with correct username and apikey combination.")
        return

    if not os.path.exists(Path.home() / _CUMINAI_CONFIG_DIR):
        os.makedirs(Path.home() / _CUMINAI_CONFIG_DIR)
        with open(Path.home() / _CUMINAI_CONFIG_DIR / _CUMINAI_CONFIG_FILE, 'x') as f:
            yaml.dump(None, f)

    data = {}
    with open(Path.home() / _CUMINAI_CONFIG_DIR / _CUMINAI_CONFIG_FILE, 'r') as f:
        data = yaml.safe_load(f)
        if data is None:
            data = {}

    data["username"] = username
    data["apikey"] = apikey
        
    with open(Path.home() / _CUMINAI_CONFIG_DIR / _CUMINAI_CONFIG_FILE, 'w') as f:
        yaml.dump(data, f)

    click.echo(f'Cumin AI login Successful for creator:{username}')

@executor.command(help='Log out from Cumin AI managed knowledge store')
def logout():
    if not os.path.exists(Path.home() / _CUMINAI_CONFIG_DIR):
        click.echo(f'Creator not logged in yet. "cuminai login" first before logging out')
        return

    data = {}
    with open(Path.home() / _CUMINAI_CONFIG_DIR / _CUMINAI_CONFIG_FILE, 'r') as f:
        data = yaml.safe_load(f)
        if data is None:
            data = {}

    if 'username' not in data or 'apikey' not in data:
        click.echo(f'Creator not logged in yet. "cuminai login" first before logging out')
        return
    
    data.pop("username", None)
    data.pop("apikey", None)

    with open(Path.home() / _CUMINAI_CONFIG_DIR / _CUMINAI_CONFIG_FILE, 'w') as f:
        yaml.dump(data, f)
    click.echo(f'Creator logged out successfully from Cumin AI')

@executor.command(help='Validate the CuminFile for any errors')
@click.option('-pdir', '--projectdir', help='path of directory containing CuminFile', default='.')
def validate(projectdir):
    try:
        _validate(projectdir)
        click.echo("cuminfile validation successful. deploy knowledge using 'cuminai deploy'")
    except ValueError as e:
        click.echo(f'cuminfile validation failed {str(e)}')
    except OSError as e:
        click.echo('CUMINFILE.yaml not found. nothing to validate. exiting...')

@executor.command(help='Deploy knowledge to Cumin AI')
@click.option('-pdir', '--projectdir', help='path of directory containing CuminFile', default='.')
def deploy(projectdir):
    click.echo("Validating CUMINFILE...")
    cuminfile = {}
    try:
        cuminfile = _validate(projectdir, get_parsed=True)
        click.echo("validation successful")
    except ValueError as e:
        click.echo(f'cuminfile validation failed {str(e)}')
        return
    except OSError as e:
        click.echo('CUMINFILE.yaml not found. nothing to validate. exiting...')
        return

    click.echo("Fetching creator credentials...")
    if not os.path.exists(Path.home() / _CUMINAI_CONFIG_DIR):
        click.echo("creator not logged in. Run command: 'cuminai login' with username and apikey")
        return
    
    creds = {}

    if not os.path.exists(Path.home() / _CUMINAI_CONFIG_DIR):
        click.echo(f"creator not logged in. Run command: 'cuminai login' with username and apikey")
        return
    
    with open(Path.home() / _CUMINAI_CONFIG_DIR / _CUMINAI_CONFIG_FILE, 'r') as f:
        data = yaml.safe_load(f)
        if data is None or 'username' not in data or 'apikey' not in data:
            click.echo("creator not logged in. Run command: 'cuminai login' with username and apikey")
            return
        creds['username'] = data['username']
        creds['apikey'] = data['apikey']
    
    click.echo("creator logged in. got credentials")

    click.echo("Preparing knowledge...")
    links = [source['link'] for source in cuminfile['knowledge']]
    
    docs = [WebBaseLoader(url).load() for url in links]
    docs_list = [item for sublist in docs for item in sublist]

    chunk_size = _DEFAULT_CHUNK_SIZE
    chunk_overlap = _DEFAULT_CHUNK_OVERLAP

    if 'chunkstrategy' in cuminfile:
        chunk_size = cuminfile['chunkstrategy']['size']
        chunk_overlap = cuminfile['chunkstrategy']['overlap']

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    doc_splits = text_splitter.split_documents(docs_list)

    click.echo("knowledge prepared")

    click.echo("Enriching knowledge metadata...")

    tags = dict()
    for source in cuminfile['knowledge']:
        tags[source['link']] = source['metadata']['tags']

    tag_type = cuminfile['tag']['type']

    if tag_type == _GLOBAL_TAGGING:
        for doc in doc_splits:
            for tag in tags[doc.metadata['source']]:
                doc.metadata[f'tag-{tag}'] = True
    elif tag_type == _LOCAL_TAGGING:
        tag_min_occur_th = cuminfile['tag']['minoccurances']
        for doc in doc_splits:
            for tag in tags[doc.metadata['source']]:
                if doc.page_content.count(tag) >= tag_min_occur_th:
                     doc.metadata[f'tag:{tag.lower()}'] = True

    click.echo("knowledge metadata enriched")

    match = validator.OllamaEmbeddingFetcher.match(cuminfile['embedding'])
    ollama_embedding_name = match.groups(1)[0]
    embedding_function = OllamaEmbeddings(model=ollama_embedding_name)

    is_public_header = "false"
    if cuminfile['type'] == _PUBLIC_VISIBILITY:
        is_public_header = "true"

    click.echo("Deploying knowledge to Cumin AI...")

    chroma_client = None
    try:
        chroma_client = chromadb.HttpClient(host=_CUMINAI_CREATOR_HOST, 
                                            port=443, 
                                            tenant=_CUMINAI_DUMMY_TENANT_NAME, 
                                            database=_CUMINAI_DUMMY_DATABASE_NAME, 
                                            ssl=True, 
                                            headers={
                                                "CUMINAI-API-KEY": creds['apikey'],
                                                "CUMINAI-KB-NAME": cuminfile['name'],
                                                "CUMINAI-IS-PUBLIC": is_public_header,
                                            }
        )
    except ValueError as e:
        click.echo("Failed to connect to Cumin AI. Please try again after sometime")
        return

    try:
        Chroma.from_documents(
            client=chroma_client,
            documents=doc_splits,
            collection_name=cuminfile['name'],
            embedding=embedding_function,
        )
    except ValueError as e:
        click.echo("Oops... something went wrong. Failed to deploy to Cumin AI")
        return
    
    click.echo(f"knowledge deployed and is available at @{creds['username']}/{cuminfile['name']}")

def _validate(projectdir, get_parsed=False):
    data = {}
    with open(os.path.join(projectdir, _CUMIN_FILE_NAME), 'r') as f:
        try:
            data = yaml.safe_load(f)
        except:
            raise ValueError("failed to validate CUMINFILE")
    
    if 'name' not in data or \
        not validator.NameValidator.match(data['name']):
        raise ValueError("::invalid name field: 'name' is required field and should be non empty alphanumeric string without spaces and symbols")
    
    if 'kind' not in data or \
        data['kind'] != _LINK_KIND:
        raise ValueError(f"::invalid kind: 'kind' is required and its value should be {_LINK_KIND}")
    
    if 'version' not in data or \
        not isinstance(data['version'], int) or \
        data['version'] <= 0:
        raise ValueError("::invalid version: 'version' is required and should be a positive integer")
    
    if 'type' in data and \
        data['type'] not in [_PUBLIC_VISIBILITY, _PRIVATE_VISIBILITY]:
        raise ValueError(f"::invalid type: 'type' is an optional field, but if defined, its value should be [{_PUBLIC_VISIBILITY}|{_PRIVATE_VISIBILITY}]. default: {_PRIVATE_VISIBILITY}")
    
    if 'embedding' not in data or \
        not isinstance(data['embedding'], str) or \
        not validator.OllamaEmbeddingValidator.match(data['embedding']):
        raise ValueError("::invalid embedding: 'embedding' is required, its value should be a valid ollama embedding name like 'ollama/nomic-embed-text:v1.5'")
    
    if 'tag' not in data or \
        not isinstance(data['tag'], dict) or \
        data['tag']['type'] not in [_GLOBAL_TAGGING, _LOCAL_TAGGING]:
        
        raise ValueError(f"::invalid tag: 'tag' is required, its type should be [{_GLOBAL_TAGGING}|{_LOCAL_TAGGING}]")
    
    if data['tag']['type'] == _LOCAL_TAGGING:
        if 'minoccurances' not in data['tag'] or \
            not isinstance(data['tag']['minoccurances'], int) or \
            data['tag']['minoccurances'] < 0:
            raise ValueError(f"::invalid tag:type:local: local tag must have valid minoccurances field value")

    if 'knowledge' not in data or \
        not isinstance(data['knowledge'], list) or \
        any('link' not in source for source in data['knowledge']) or \
        any(not validator.LinkValidator.match(source['link']) for source in data['knowledge']):
        raise ValueError("::invalid knowledge source: 'knowledge' is required, and should be a list of valid knowledge sources of the particular kind to ingest")
    
    if any('metadata' in source and 'tags' in source['metadata'] and not isinstance(source['metadata']['tags'], list) for source in data['knowledge']):
        raise ValueError("::invalid knowledge:metadata:tags: metadata tags should be a list of string tags")
    
    if any('metadata' in source and any(not isinstance(tag, str) for tag in source['metadata']['tags']) for source in data['knowledge']):
        raise ValueError("::invalid knowledge:metadata:tags: metadata tags should be a list of string tags")
    
    if 'chunkstrategy' in data and not isinstance(data['chunkstrategy'], dict):
        raise ValueError("::invalid chunkstrategy: chunk strategy is optional, but if defined, must be a dict containing size and overlap")
    
    if 'chunkstrategy' in data:
        if 'size' not in data['chunkstrategy'] or not isinstance(data['chunkstrategy']['size'], int) or \
            data['chunkstrategy']['size'] < 100 or data['chunkstrategy']['size'] > 8196:
            raise ValueError("::invalid chunkstrategy:size: size should be a positive integer value (min:10, max:8196)")
        
        if 'overlap' not in data['chunkstrategy'] or not isinstance(data['chunkstrategy']['overlap'], int) or \
            data['chunkstrategy']['overlap'] < 0 or data['chunkstrategy']['overlap'] > data['chunkstrategy']['size']/2:
            raise ValueError("::invalid chunkstrategy:overlap: overlap should be a non negative integer value (min:10, max:val[size]/2)")
    
    if get_parsed:
        return data