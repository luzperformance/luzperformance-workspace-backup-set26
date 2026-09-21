#!/usr/bin/env python3
"""Rebuild the active semantic-memory index from approved operational sources only."""
import hashlib
import json
import os
import sys
import time
from pathlib import Path

HOME = Path('/data')
RESULT = HOME / 'logs' / 'operational-memory-reindex.json'
RESULT.parent.mkdir(parents=True, exist_ok=True)

# The OpenAI credential is injected by the container and deliberately remains out of files/logs.
for item in Path('/proc/1/environ').read_bytes().split(b'\0'):
    if item.startswith(b'OPENAI_API_KEY='):
        os.environ['OPENAI_API_KEY'] = item.split(b'=', 1)[1].decode()
        break
if not os.environ.get('OPENAI_API_KEY'):
    raise RuntimeError('OPENAI_API_KEY is unavailable in the container environment')

# Give the stopped gateway time to release the old local-Qdrant lock.
time.sleep(3)

# Preserve the previous vector store untouched; use a clean collection path for this filtered index.
config_path = HOME / 'mem0.json'
config = json.loads(config_path.read_text(encoding='utf-8'))
oss = config.get('oss', {})
embedder = oss.get('embedder', {})
if embedder.get('provider') != 'openai' or embedder.get('config', {}).get('model') != 'text-embedding-3-small':
    raise RuntimeError('Mem0 is not configured with OpenAI text-embedding-3-small')
oss.setdefault('vector_store', {}).setdefault('config', {})['path'] = '/data/mem0_qdrant_operational'
config['oss'] = oss
config_path.write_text(json.dumps(config, indent=2) + '\n', encoding='utf-8')

# Sources: all operational context. The patient-case section of USER.md is intentionally excluded.
memory = (HOME / 'memories' / 'MEMORY.md').read_text(encoding='utf-8')
user = (HOME / 'USER.md').read_text(encoding='utf-8')
user = user.split('\n## Cases OpenClaw / Comunidade', 1)[0].rstrip() + '\n'
agents = (HOME / 'AGENTS.md').read_text(encoding='utf-8')
mapa = (HOME / 'MAPA.md').read_text(encoding='utf-8')
decisions = (HOME / 'decisions' / '2026-09.md').read_text(encoding='utf-8')
sources = {
    '/data/memories/MEMORY.md': memory,
    '/data/USER.md (operational section only)': user,
    '/data/AGENTS.md': agents,
    '/data/MAPA.md': mapa,
    '/data/decisions/2026-09.md': decisions,
}
for name, text in sources.items():
    if any(token in text for token in ('K.E.F.', 'E.R.R.', 'R.E.G.', '## Cases OpenClaw')):
        raise RuntimeError(f'Patient content detected in approved source: {name}')

sys.path.insert(0, '/opt/hermes-agent')
from plugins.memory.mem0._backend import OSSBackend
backend = OSSBackend(oss)
user_id = config.get('user_id') or 'vinicius'
agent_id = config.get('agent_id') or 'hermes'
for source, text in sources.items():
    backend.add(
        [{'role': 'user', 'content': f'Contexto operacional indexado — {source}:\n\n{text}'}],
        user_id=user_id,
        agent_id=agent_id,
        infer=False,
        metadata={'source': source, 'sha256': hashlib.sha256(text.encode()).hexdigest(), 'scope': 'operational-only'},
    )
results = backend.search('qual é o negócio e o objetivo operacional do usuário', filters={'user_id': user_id}, top_k=5)
if not results:
    raise RuntimeError('Semantic retrieval returned no results')
serialized = json.dumps(results, ensure_ascii=False)
if any(token in serialized for token in ('K.E.F.', 'E.R.R.', 'R.E.G.')):
    raise RuntimeError('Patient content appeared in semantic-retrieval results')
RESULT.write_text(json.dumps({
    'status': 'completed',
    'sources_indexed': list(sources),
    'source_count': len(sources),
    'embedder': 'text-embedding-3-small',
    'vector_store': '/data/mem0_qdrant_operational',
    'semantic_results': len(results),
    'patient_content_indexed': False,
}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(str(RESULT))
