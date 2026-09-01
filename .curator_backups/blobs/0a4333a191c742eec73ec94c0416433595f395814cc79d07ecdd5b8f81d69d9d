# Drive público — pasta de criativos

URL canônica (precisa de `?usp=sharing` senão parece login wall):

https://drive.google.com/drive/folders/1XBchmeeu8UE0ew2f8mF_aLs1T1j1JQiP?usp=sharing

## Listar IDs sem OAuth

1. GET o HTML da URL com sharing.
2. Pares: `aria-label="NOME.mp4 ..."` + `ssk='5:auSv138:FILEID'`.
3. FILEID é o prefixo antes de `-0-16` se o ssk vier sufixado.

## Download (gdown 6.x)

```python
import gdown
gdown.download(id=FILE_ID, output=dest, quiet=False)
# NÃO passar fuzzy=True — TypeError no 6.1
```

SRT primeiro (1–3 KB). Vídeo: um master por peça. Clones (`with_captions`, `(1)`, `comuns4`) ignorar.

## Extração

- ffprobe: duration, 1080x1920, 25fps típico HeyGen
- frames: 0.3s, 2s, 5s, meio, fim
- caption queimada: crop terço inferior, frame a cada 4–8s

Saída de análise: `content/archive/heygen-analise/`
Roteiros: `content/drafts/heygen/`
