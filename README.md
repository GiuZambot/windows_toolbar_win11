# Toolbar Flutuante para Windows 11

Esta aplicação cria uma toolbar flutuante que fica sempre visível na tela. Você pode usá-la para acessar rapidamente seus projetos e aplicativos favoritos.

## Características principais

- **Sempre visível**: Fica por cima de outras janelas
- **Transparente**: Semi-transparente para não atrapalhar sua visão
- **Arrável**: Pode ser posicionada em qualquer lugar da tela
- **Atalhos rápidos**: Botões diretos para seus projetos mais utilizados
- **Categorias**: Menus organizados por tipo de aplicativo (VS Code, Godot, etc.)
- **Personalizável**: Interface completa de configuração

## Requisitos

- Python 3.6 ou superior
- PyQt5
- Pillow (opcional, para criar ícones)
- pywin32 (opcional, para inicialização automática com o Windows)

## Instalação

1. Salve o código em um arquivo chamado `toolbar_flutuante.py`
2. Instale as dependências:
   ```
   pip install PyQt5 pillow pywin32
   ```

## Como usar

1. Execute o programa:
   ```
   python toolbar_flutuante.py
   ```

2. A toolbar aparecerá na parte inferior da tela
3. Clique nos botões para abrir os aplicativos diretamente
4. Clique nos botões de categoria para ver mais opções em um menu
5. Arraste a toolbar pela "alça" (≡) ou por qualquer parte dela para reposicionar

## Configuração

Na primeira execução, será criado um arquivo de configuração padrão chamado `toolbar_config.json` no mesmo diretório. Este arquivo já estará pré-configurado com exemplos, incluindo o VS Code apontando para o caminho que você mencionou.

Para configurar seus atalhos e categorias:

1. Clique no botão de configurações (ícone de engrenagem) na toolbar
2. Você verá três abas:
   - **Atalhos Rápidos**: Configure botões diretos que aparecem na toolbar
   - **Categorias**: Organize seus projetos em categorias
   - **Geral**: Configurações de transparência, posição e inicialização com o Windows

## Atalhos rápidos

Os atalhos rápidos são botões que aparecem diretamente na toolbar para acesso com um clique. Para cada atalho, você pode configurar:

- **Nome**: Nome visível no tooltip
- **Executável**: Caminho para o programa a ser executado
- **Argumentos**: Parâmetros de linha de comando (como o caminho do projeto)
- **Ícone** (opcional): Caminho para um ícone personalizado
- **Tooltip**: Texto que aparece ao passar o mouse sobre o botão

## Categorias

As categorias são menus que aparecem ao clicar em um botão da toolbar. Cada categoria pode conter múltiplos atalhos.

- Você pode criar categorias como "VS Code", "Godot", "Unity", etc.
- Cada categoria pode ter quantos atalhos quiser
- Os atalhos funcionam da mesma forma que os atalhos rápidos

## Exemplos de configuração

### Para o VS Code:
- **Nome**: VS Code Affiliate
- **Executável**: `C:\Users\giuli\AppData\Local\Programs\Microsoft VS Code\Code.exe`
- **Argumentos**: `C:\Almatter\afiliate`

### Para o Godot 4.4:
- **Nome**: Meu Projeto Godot
- **Executável**: Caminho para o executável do Godot
- **Argumentos**: `--path C:\caminho\para\projeto`

## Inicialização com o Windows

Na aba "Geral" das configurações, você pode ativar a opção "Iniciar com o Windows" para que a toolbar seja iniciada automaticamente quando você ligar o computador.
