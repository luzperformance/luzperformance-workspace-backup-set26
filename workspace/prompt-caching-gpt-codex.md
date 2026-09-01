# Parte 6: Prompt Caching para GPT Codex

## Objetivo

Reduzir latência e custo ao reutilizar prefixos de prompt estáveis nos modelos GPT/Codex.

> **Importante:** na API da OpenAI, o prompt caching é automático para requisições elegíveis. Não use opções Anthropic/OpenClaw inventadas como `cache.enabled`, `cache.ttl`, `cache.priority` ou `models.cache` sem confirmar que o cliente realmente as implementa e encaminha para a API.

## Modelos e roteamento

### Regra de seleção

```text
MODEL SELECTION RULE:

Default: Always use Terra.

Switch to Sol for:
- Coding and software-development tasks
- Long-running tasks

Switch to Luna ONLY when:
- The user explicitly requests Luna by name

Never select Luna automatically.

When in doubt: Use Terra.
```

Prioridade prática:

1. **Luna** somente quando chamada explicitamente pelo nome.
2. **Sol** para codificação e tarefas longas.
3. **Terra** como padrão para todo o restante.

### Exemplo de configuração dos aliases

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "openai-codex/gpt-5.6-terra"
      },
      "models": {
        "openai-codex/gpt-5.6-terra": {
          "alias": "terra"
        },
        "openai-codex/gpt-5.6-sol": {
          "alias": "sol"
        },
        "openai-codex/gpt-5.6-luna": {
          "alias": "luna"
        }
      }
    }
  }
}
```

> Os identificadores acima seguem a nomenclatura definida para este ambiente. Se o provedor expuser IDs diferentes, preserve os aliases `terra`, `sol` e `luna`, mas substitua as chaves pelos IDs efetivamente disponíveis.

---

## Como o cache da OpenAI funciona

O prompt caching:

- funciona automaticamente em modelos recentes elegíveis;
- exige, em GPT‑5.6+, um prefixo renderizado de pelo menos **1.024 tokens** até o breakpoint;
- reutiliza somente prefixos idênticos;
- reduz a latência e cobra os tokens reutilizados pela tarifa de entrada em cache do modelo;
- pode usar `prompt_cache_key` para melhorar o roteamento de requisições que compartilham o mesmo prefixo;
- expõe leituras em `cached_tokens` e, em GPT‑5.6+, gravações em `cache_write_tokens`.

O primeiro pedido normalmente cria uma entrada elegível. Pedidos posteriores podem reutilizá-la quando:

1. o conteúdo até o breakpoint é idêntico;
2. a chave `prompt_cache_key` é consistente;
3. o cache ainda está disponível;
4. o modelo e o endpoint usados oferecem esse comportamento.

## O que deve ficar no prefixo estável

### Coloque antes do breakpoint

- instruções de sistema estáveis;
- identidade e princípios operacionais estáveis;
- documentação de ferramentas;
- schemas de ferramentas e saídas estruturadas;
- exemplos reutilizados;
- especificações e referências estáveis;
- templates de projeto.

### Coloque depois do breakpoint

- mensagem atual do usuário;
- timestamps;
- IDs de execução;
- notas diárias;
- histórico recente variável;
- resultados de ferramentas;
- dados específicos do cliente ou da tarefa;
- qualquer conteúdo alterado frequentemente.

Uma única alteração antes do breakpoint produz outro prefixo e pode impedir o cache hit.

## Organização recomendada

```text
/workspace/
├── SOUL.md                      # estável
├── USER.md                      # estável quando contém perfil durável
├── TOOLS.md                     # estável
├── memory/
│   ├── MEMORY.md                # dinâmico; não incluir no prefixo estável inteiro
│   └── YYYY-MM-DD.md            # dinâmico
└── projects/
    └── PROJECT/
        ├── REFERENCE.md         # estável
        └── NOTES.md             # dinâmico
```

A aplicação precisa montar o prompt nesta ordem:

```text
Instruções e referências estáveis
[BREAKPOINT DE CACHE]
Contexto dinâmico
Mensagem atual
```

Manter arquivos separados ajuda na organização, mas **não cria cache sozinho**. O que determina a reutilização é o prompt final renderizado, seu breakpoint e a igualdade exata do prefixo.

## Configuração correta na API OpenAI

O cache automático não exige uma chave `cache.enabled`. Para workloads com prefixos compartilhados, use uma chave estável:

```json
{
  "model": "gpt-5.6-sol",
  "prompt_cache_key": "workspace:project-a:instructions-v1",
  "input": [
    {
      "role": "developer",
      "content": "Instruções estáveis e referências do projeto..."
    },
    {
      "role": "user",
      "content": "Conteúdo variável desta execução..."
    }
  ]
}
```

Se o SDK/endpoint usado oferecer breakpoints explícitos para GPT‑5.6+, marque o fim do bloco estável conforme a sintaxe daquele SDK. Não invente essa sintaxe em arquivos de configuração do agente: confirme que o cliente a suporta e a encaminha à Responses API.

### Retenção

Quando suportado pelo modelo e endpoint, `prompt_cache_retention` permite selecionar a política de retenção:

```json
{
  "prompt_cache_retention": "in_memory"
}
```

Em cache `in_memory`, prefixos geralmente permanecem ativos por **5 a 10 minutos de inatividade**, com máximo de até uma hora. Alguns modelos oferecem retenção estendida de até 24 horas, mas o suporte deve ser verificado para cada ID de modelo. Retenção maior não garante cache hit.

## Estratégia para Terra, Sol e Luna

### Terra — padrão

- usar em tarefas comuns;
- manter o prefixo-base estável;
- não trocar automaticamente por outro modelo;
- usar cache quando o prompt atingir o mínimo elegível.

### Sol — código e tarefas longas

- reutilizar as mesmas instruções de repositório e schemas;
- manter regras do projeto antes do breakpoint;
- colocar diffs, logs, pedidos atuais e resultados de testes depois do breakpoint;
- usar uma `prompt_cache_key` por projeto e versão do conjunto de instruções.

Exemplo:

```text
workspace:backend:instructions-v3
```

### Luna — somente por solicitação explícita

- nunca selecionar automaticamente;
- quando solicitada, preservar a mesma estratégia de prefixo estável;
- usar uma chave separada se a troca de modelo ou persona alterar o prefixo renderizado.

## Rate limits e orçamento

```text
RATE LIMITS:

- Minimum of 5 seconds between API calls
- Minimum of 10 seconds between web searches
- Maximum of 5 searches per batch, followed by a 2-minute break
- Batch similar work whenever possible
- Warn when usage reaches 75% of the configured budget
- On HTTP 429: stop, wait 5 minutes, then retry
```

Esses limites são controles locais de uso. Eles não ativam o prompt caching, mas ajudam a evitar loops, picos de tráfego e gastos inesperados.

> Observação: agrupar trabalhos semelhantes é útil, mas não se deve disparar requisições em sequência rápida apenas para tentar manter o cache. Os intervalos de rate limit definidos acima continuam prevalecendo.

## Como maximizar cache hits

1. Mantenha instruções, ferramentas e schemas estáveis.
2. Coloque conteúdo estável no início e conteúdo variável no fim.
3. Defina o breakpoint logo após o prefixo estável elegível.
4. Reutilize a mesma `prompt_cache_key` para o mesmo prefixo lógico.
5. Versione a chave quando as instruções mudarem.
6. Não coloque timestamps, IDs aleatórios ou notas diárias antes do breakpoint.
7. Não altere o conjunto ou a ordem das ferramentas entre pedidos que devem compartilhar cache.
8. Em workloads de alto volume, distribua chaves de maneira estável; não use uma chave aleatória por pedido.

## Monitoramento

Na Responses API, verifique:

```json
{
  "usage": {
    "input_tokens": 2600,
    "input_tokens_details": {
      "cached_tokens": 2000,
      "cache_write_tokens": 400
    }
  }
}
```

Interpretação:

- `cached_tokens`: tokens de entrada lidos do cache;
- `cache_write_tokens`: tokens novos gravados no cache;
- `input_tokens - cached_tokens - cache_write_tokens`: tokens de entrada que não foram lidos nem gravados em cache.

Métricas úteis:

- proporção de `cached_tokens` sobre `input_tokens`;
- volume de `cache_write_tokens` sem leituras posteriores;
- latência com e sem cache hit;
- custo de entrada normal, de gravação e de leitura em cache;
- mudanças frequentes na chave ou no prefixo.

Se `cache_write_tokens` cresce continuamente e `cached_tokens` permanece baixo, investigue:

- timestamps ou IDs no prefixo;
- alterações frequentes nas instruções;
- mudança de ferramentas ou schemas;
- chaves inconsistentes;
- breakpoint posicionado depois de conteúdo dinâmico;
- prefixo com menos de 1.024 tokens.

## Quando o cache pode não compensar

- prompts menores que o mínimo elegível;
- tarefas isoladas sem repetição de prefixo;
- desenvolvimento com mudanças constantes nas instruções;
- conteúdo quase totalmente dinâmico;
- workloads nos quais o cliente não expõe ou não preserva os recursos de cache da API.

## Checklist

- [ ] Terra é o modelo padrão.
- [ ] Sol é usado para codificação e tarefas longas.
- [ ] Luna só é usada quando solicitada explicitamente.
- [ ] O prefixo estável vem antes do conteúdo variável.
- [ ] O breakpoint cobre pelo menos 1.024 tokens em GPT‑5.6+.
- [ ] `prompt_cache_key` é estável e versionada.
- [ ] Timestamps e resultados de ferramentas ficam após o breakpoint.
- [ ] `cached_tokens` e `cache_write_tokens` são monitorados.
- [ ] Os rate limits locais continuam ativos.
- [ ] Preços e suporte de retenção são consultados para o modelo real antes de estimar economia.

## Resultado esperado

Antes:

- contexto estável reprocessado sem estratégia;
- baixa previsibilidade de cache hits;
- conteúdo dinâmico invalidando prefixos;
- ausência de métricas de leitura e gravação.

Depois:

- Terra como padrão e roteamento controlado para Sol/Luna;
- prefixo estável e versionado;
- conteúdo variável depois do breakpoint;
- monitoramento por `cached_tokens` e `cache_write_tokens`;
- economia calculada com as tarifas reais do modelo, sem assumir percentuais da Anthropic.

## Referência oficial

- OpenAI — Prompt Caching: https://developers.openai.com/api/docs/guides/prompt-caching/
