# Floating Toolbar Launcher

![image](https://github.com/user-attachments/assets/2240ef86-3ea9-4d9d-b76e-9d1c47655a54)

## Descrição

Uma aplicação de toolbar flutuante personalizada para lançar rapidamente atalhos e projetos em diferentes aplicativos.

## Requisitos

- Python 3.7+
- PyQt5
- pywin32 (opcional, para inicialização automática)

## Instalação

### Dependências

Instale as dependências necessárias usando pip:

```bash
pip install PyQt5 pywin32
```

### Configuração do Ambiente

1. Clone o repositório ou baixe os arquivos do script.
2. Certifique-se de ter o Python instalado em seu sistema.

## Executando a Aplicação

### Método Direto

```bash
python floating_toolbar.py
```

### Criando um Executável (Opcional)

Você pode criar um executável usando PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed floating_toolbar.py
```

## Funcionalidades

### Toolbar Flutuante

- Mova a toolbar arrastando o botão com três linhas (≡)
- Personalize a posição e opacidade nas configurações
- Adicione atalhos rápidos e categorias de projetos

### Configurações

- Posicionamento da toolbar na tela
- Controle de opacidade
- Inicialização automática com o Windows
- Gerenciamento de atalhos rápidos
- Gerenciamento de categorias de projetos

## Como Usar

### Atalhos Rápidos

1. Clique no botão de configurações
2. Vá para a aba "Atalhos Rápidos"
3. Adicione novos atalhos com nome, executável, argumentos, ícone e tooltip

### Categorias

1. Na aba "Categorias", adicione categorias de projetos
2. Adicione atalhos para cada categoria
3. Clique no botão da categoria na toolbar para ver os atalhos disponíveis

### Inicialização

- Marque "Iniciar com o Windows" nas configurações gerais para iniciar automaticamente

## Personalização

- Edite o arquivo `toolbar_config.json` para configurações avançadas
- Modifique o código-fonte para personalizar o comportamento

## Solução de Problemas

- Certifique-se de ter todas as dependências instaladas
- Verifique os caminhos dos executáveis ao adicionar atalhos
- Reinicie a aplicação se encontrar problemas

## Licença

[Especifique a licença do seu projeto]

## Contribuições

Contribuições são bem-vindas! Por favor, abra uma issue ou envie um pull request.

## Autor

Giu Zambot
