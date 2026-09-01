# Build e validação

O artefato oficial é `starter-kit-hermes.zip`.

## Checklist

```bash
python scripts/validate.py
bash -n scripts/install.sh
python -m json.tool skills/starter/onboarding-checklist/evals/evals.json >/dev/null
```

A validação falha se encontrar comandos/caminhos da plataforma anterior, JSON inválido, SKILL sem frontmatter ou links locais ausentes.
