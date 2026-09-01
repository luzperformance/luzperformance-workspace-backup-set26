# BUILD.md — Como gerar o .zip do Starter Kit v1

> Instruções pra empacotar o starter-kit em arquivo distribuível pra alunos.

## Objetivo do .zip

Aluno baixa o .zip, descompacta no workspace do OpenClaw Managed (ou local), e o agente já tem todas as 14 skills + exemplos + FAQ disponíveis.

## Estrutura final do .zip

```
starter-kit-openclaw-v1.zip
└── starter-kit/
    ├── README.md
    ├── manifesto.md
    ├── FAQ.md
    ├── exemplos/
    │   ├── README.md
    │   ├── USER-amora.md (sanitizado)
    │   ├── IDENTITY-amora.md
    │   ├── SOUL-amora.md
    │   ├── AGENTS-amora.md
    │   └── MAPA-amora.md
    ├── templates/
    │   ├── README.md
    │   ├── IDENTITY.template.md
    │   ├── SOUL-stub.template.md
    │   ├── AGENTS.template.md
    │   ├── USER.template.md
    │   └── MAPA.template.md
    └── skills/
        ├── _registry.md
        ├── starter/ (8 skills)
        ├── canais/ (1 skill)
        ├── planejamento/ (4 skills)
        └── operacional/ (1 skill)
```

## O que NÃO entra no .zip

- `MAPA-DA-V2.md` (planejamento interno, não é pra aluno)
- `DECISOES-ARQUITETURA.md` (idem)
- `BUILD.md` (este arquivo)
- Pasta de scripts/utilities da Pixel (se tiver)
- Qualquer arquivo com info pessoal do Bruno fora dos exemplos sanitizados

## Comando pra gerar (zsh, do diretório `curso-openclaw-v2/`)

```bash
# 1. Pasta temporária com cópia limpa
TMP_BUILD=~/tmp/starter-kit-build-$(date +%Y-%m-%d-%H%M)
mkdir -p "$TMP_BUILD"
cp -R starter-kit "$TMP_BUILD/"

# 2. Remover arquivos macOS automáticos
find "$TMP_BUILD/starter-kit" -name ".DS_Store" -delete
find "$TMP_BUILD/starter-kit" -name "._*" -delete

# 3. Verificar duplicatas (problema observado: "onboarding-checklist 2/")
find "$TMP_BUILD/starter-kit" -type d -name "* 2" -exec echo "DUPLICATA: {}" \;
# Se aparecer alguma, remove manualmente antes de zipar

# 4. Zipar
cd "$TMP_BUILD"
zip -r "starter-kit-openclaw-v1.zip" starter-kit/ \
    --exclude "*.DS_Store" \
    --exclude "*/__pycache__/*" \
    --exclude "*/.git/*"

# 5. Verificar tamanho (deve ficar entre 200KB-1MB)
ls -lh starter-kit-openclaw-v1.zip
```

## Checklist pré-build

Antes de gerar o .zip, validar:

- [ ] Todos os 14 SKILL.md têm frontmatter V3 completo
- [ ] Todos têm `status: ATIVO` (não DRAFT, não PENDENTE)
- [ ] Templates raiz não têm placeholders quebrados (procurar `{NAOSUBSTITUIDO}`)
- [ ] Exemplos Amora estão sanitizados (sem dados de família, números financeiros específicos, contratos)
- [ ] FAQ revisado vs decisões da v2 (foi copiado da v1, pode ter info desatualizada)
- [ ] Manifesto e README batem com o que o kit realmente entrega
- [ ] Nenhum arquivo tem path absoluto do Mac do Bruno (`/Users/okamoto/...`) referenciado
- [ ] Nenhum SKILL.md menciona path absoluto fora do workspace do aluno

### Comando rápido pra detectar paths absolutos

```bash
grep -r "/Users/okamoto" starter-kit/ && echo "⚠️ Encontrei path absoluto" || echo "✓ Sem paths absolutos"
grep -r "okamoto/Documents" starter-kit/ && echo "⚠️ Path interno" || echo "✓ Sem path interno"
```

### Comando pra detectar PII

```bash
# Números de telefone
grep -rE "\+55|\([0-9]{2}\)" starter-kit/ | grep -v "exemplo"

# Emails específicos
grep -rE "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" starter-kit/ | \
   grep -v "bruno@microsaas.com.br" | \
   grep -v "exemplo"
```

(Email do Bruno em FAQ/manifesto é intencional — aluno precisa pra mandar feedback.)

## Onde hospedar o .zip

3 opções:

### A) GitHub Release (recomendado)
- Repo dedicado: `okjpg/openclaw-starter-kit-v1`
- Release tagueado: `v1.0.0`
- Aluno baixa direto do GitHub
- Vantagem: versionamento + changelog

### B) Hostinger / Pixel Educação
- Upload no painel
- Link de download na área de membros do mini-curso
- Vantagem: integrado com checkout

### C) Direto no Telegram
- Bot do mini-curso entrega .zip quando aluno completa registro
- Vantagem: zero atrito (aluno já tá no Telegram)

**Recomendado:** A + C (GitHub release pra histórico, bot Telegram pra distribuição final).

## Como aluno usa o .zip

```bash
# Aluno descompacta no workspace
unzip starter-kit-openclaw-v1.zip -d ~/

# Move skills pro local correto
mv ~/starter-kit/skills/* ~/.openclaw/workspace/skills/

# (ou ajusta path conforme estrutura do Managed dele)

# Inicia jornada
# Aluno abre Telegram, manda 'oi' → onboarding-checklist dispara automaticamente
```

Detalhes específicos por plataforma (Hostinger Managed vs VPS própria) vão no `README.md` do kit.

## Versionamento

- v1.0 → primeiro lançamento (Onda 2 + 3 completa, 14 skills)
- v1.1 → ajustes pós-feedback (typos, melhorias UX)
- v1.2 → melhorias de UX dos wizards baseadas em uso real
- v2.0 → reestruturação maior (se houver)

Cada release tem CHANGELOG.md atualizado.

## Roadmap pós-v1

Não entra no .zip v1, mas tá no radar:

- v1.1: WhatsApp pra Caso B+ (chip dedicado + whitelist + aprovação manual)
- v1.2: Skill `migra-secrets-1password` (substitui .env por 1Password vault)
- v1.3: Mais 4 superpowers curados (debugging, system-design, etc)
- v2: Curso pra aluno antigo (kit de upgrade dedicado em vez de só o prompt agentic)

---

*BUILD.md v1 — pronto pra gerar quando Bruno der OK depois dos testes.*
