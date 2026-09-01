from pathlib import Path
import json, re, sys
root=Path(__file__).resolve().parents[1]
errors=[]
for p in root.rglob('*'):
    if not p.is_file(): continue
    if p.suffix.lower() in {'.png','.jpg','.jpeg','.gif','.webp','.7z','.zip'}: continue
    try: text=p.read_text(encoding='utf-8')
    except UnicodeDecodeError: continue
    low=text.lower()
    # O guia de migração cita nomes antigos deliberadamente; o validador contém os padrões de bloqueio.
    if p.name not in {'MIGRACAO-OPENCLAW-HERMES.md', 'validate.py'}:
        for banned in ('openclaw ', 'openclaw\n', '.openclaw', 'openclaw.json', 'docs.openclaw'):
            if banned in low: errors.append(f'{p.relative_to(root)}: referência residual {banned!r}')
    if p.name=='SKILL.md':
        if not text.startswith('---\n') or '\nname:' not in text or '\ndescription:' not in text:
            errors.append(f'{p.relative_to(root)}: frontmatter inválido')
    if p.suffix=='.json':
        try: json.loads(text)
        except Exception as e: errors.append(f'{p.relative_to(root)}: JSON inválido: {e}')
for p in root.rglob('*.md'):
    text=p.read_text(encoding='utf-8')
    for link in re.findall(r'\[[^]]+\]\(([^)]+)\)', text):
        if '://' in link or link.startswith('#') or link.startswith('mailto:'): continue
        target=(p.parent/link.split('#')[0]).resolve()
        if not target.exists(): errors.append(f'{p.relative_to(root)}: link ausente {link}')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print(f'OK: {sum(1 for p in root.rglob("*") if p.is_file())} arquivos validados')
