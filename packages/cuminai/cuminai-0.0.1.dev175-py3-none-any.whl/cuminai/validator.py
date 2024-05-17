import re

UsernameValidator = re.compile('^[0-9a-zA-Z]{6,36}$')
NameValidator = re.compile('^[0-9a-zA-Z]+$')

OllamaEmbeddingValidator = re.compile('^ollama/(mxbai-embed-large|nomic-embed-text|all-minilm)(latest|(:v[0-9a-zA-Z-_.]+))?$')

LinkValidator = re.compile('^(https://www.|https://)[a-zA-Z]{2,}(.[a-zA-Z]{2,})(.[a-zA-Z]{2,})?/[a-zA-Z0-9]{2,}|((https://www.|https://)[a-zA-Z]{2,}(.[a-zA-Z]{2,})(.[a-zA-Z]{2,})?)|(https://www.|https://)[a-zA-Z0-9]{2,}.[a-zA-Z0-9]{2,}.[a-zA-Z0-9]{2,}(.[a-zA-Z0-9]{2,})?$')

OllamaEmbeddingFetcher = re.compile('^ollama/(.*)$')