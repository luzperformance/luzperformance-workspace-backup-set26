# Padrão: frente recorrente de conhecimento

Use este padrão quando uma pasta passa a concentrar material que continuará chegando ao longo do tempo, como ensinamentos de curso, pesquisa ou referências operacionais.

## Estrutura mínima

```text
area-pai/
└── frente-nomeada/
    └── MAPA.md
```

## Conteúdo mínimo do `MAPA.md`

1. Finalidade em uma frase.
2. O que entra: aulas, notas, fontes, materiais e aplicações práticas.
3. O que sai: conteúdo editorial, decisões e outros derivados devem seguir para suas áreas canônicas.

## Registros obrigatórios

- Incluir a frente no `MAPA.md` da área-pai.
- Incluir no mapa raiz, se ele catalogar frentes ativas.
- Registrar a decisão no arquivo mensal de `decisions/`.

## Critério de qualidade

Uma pessoa que abra somente o mapa raiz deve conseguir descobrir a frente; uma pessoa que abra somente o mapa local deve saber o que guardar ali.