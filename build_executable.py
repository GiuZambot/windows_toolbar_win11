import os
import sys
import subprocess


def install_dependencies():
    """Instala as dependências necessárias"""
    try:
        import PyQt5
        import pywin32
        from PIL import Image
    except ImportError:
        print("Instalando dependências necessárias...")
        subprocess.check_call(
            [sys.executable, '-m', 'pip', 'install', 'PyQt5', 'pywin32', 'Pillow', 'pyinstaller'])


def convert_icon(png_path, ico_path):
    """Converte ícone PNG para ICO"""
    try:
        from PIL import Image

        # Verifica se o arquivo PNG existe
        if not os.path.exists(png_path):
            print(f"Erro: Arquivo {png_path} não encontrado.")
            return False

        # Abre a imagem
        img = Image.open(png_path)

        # Redimensiona para tamanhos padrão de ícone
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]

        # Salva como ICO
        img.save(ico_path, format='ICO', sizes=sizes)

        print(f"Ícone convertido com sucesso: {ico_path}")
        return True
    except Exception as e:
        print(f"Erro ao converter ícone: {e}")
        return False


def create_executable():
    """Cria o executável usando PyInstaller"""
    # Importa PyInstaller
    import PyInstaller.__main__

    # Caminho para o script principal
    script_path = 'floating_toolbar.py'

    # Caminho do ícone
    png_icon_path = 'icon.png'
    ico_icon_path = 'icon.ico'

    # Converte o ícone
    if os.path.exists(png_icon_path):
        if not convert_icon(png_icon_path, ico_icon_path):
            print("Continuando sem ícone...")
            ico_icon_path = None
    else:
        print(f"Arquivo de ícone {png_icon_path} não encontrado.")
        ico_icon_path = None

    # Opções do PyInstaller
    pyinstaller_args = [
        '--onefile',      # Cria um único arquivo executável
        '--windowed',     # Sem console/janela de terminal
        '--name=FloatingToolbar',  # Nome do executável
    ]

    # Adiciona ícone se existir
    if ico_icon_path and os.path.exists(ico_icon_path):
        # Usa caminho absoluto
        full_ico_path = os.path.abspath(ico_icon_path)
        print(f"Caminho completo do ícone: {full_ico_path}")
        pyinstaller_args.extend(['--icon', full_ico_path])

    # Adiciona o script principal
    pyinstaller_args.append(script_path)

    print("Criando executável...")
    print("Argumentos do PyInstaller:", pyinstaller_args)
    PyInstaller.__main__.run(pyinstaller_args)
    print("Executável criado com sucesso!")


def main():
    # Instala dependências
    install_dependencies()

    # Cria o executável
    create_executable()

    print("Processo concluído. Verifique a pasta 'dist' para o executável.")


if __name__ == '__main__':
    main()
