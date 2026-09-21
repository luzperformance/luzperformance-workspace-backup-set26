# Fallback XDG Trash no Linux

Use somente quando não houver um utilitário de lixeira e a origem puder ser movida no mesmo sistema de arquivos do diretório XDG Trash.

## Estrutura padrão

- `~/.local/share/Trash/files/` — conteúdo recuperável.
- `~/.local/share/Trash/info/` — um arquivo `<nome-unico>.trashinfo` para cada item.

## Sequência segura

1. Confirme que a origem existe e obtenha o identificador do dispositivo da origem e da lixeira (por exemplo, `stat -c %d`). Se forem diferentes, não faça uma movimentação manual que possa virar cópia seguida de exclusão; use uma lixeira do mesmo volume ou pare.
2. Crie `files/` e `info/` se necessário.
3. Gere um nome único e mova o diretório inteiro para `files/<nome-unico>`.
4. Crie `info/<nome-unico>.trashinfo` com:

```ini
[Trash Info]
Path=<caminho-original-com-escape-URL>
DeletionDate=<AAAA-MM-DDTHH:MM:SS>
```

5. Verifique que a origem não existe, o destino existe e o `.trashinfo` existe antes de atualizar índices.

## Recuperação

Para restaurar, mova o conteúdo de `files/<nome-unico>` de volta ao caminho indicado no `.trashinfo`, após garantir que o destino original não foi reutilizado. Remova o `.trashinfo` correspondente somente após restaurar com êxito.

Este procedimento preserva recuperação manual e evita transformar uma solicitação de exclusão em perda definitiva.
