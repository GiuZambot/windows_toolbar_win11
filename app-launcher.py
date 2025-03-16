import sys
import os
import json
from PyQt5 import QtWidgets, QtCore, QtGui
import subprocess


class FloatingToolbar(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Configurações de janela para ficar sempre visível e sem bordas
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.Tool
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Carrega configurações
        self.config_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'toolbar_config.json')
        self.config = self.load_config()

        # Cria o layout principal
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(5)

        # Layout para os botões
        self.toolbar_layout = QtWidgets.QHBoxLayout()
        self.toolbar_layout.setSpacing(2)

        # Adiciona botões diretos e botões de categoria
        self.create_toolbar_buttons()

        # Adiciona o layout da toolbar ao layout principal
        self.main_layout.addLayout(self.toolbar_layout)

        # Cria um frame visual para a toolbar
        self.frame = QtWidgets.QFrame()
        self.frame.setObjectName("toolbarFrame")
        self.frame.setLayout(self.main_layout)

        # Aplica o estilo com a opacidade salva nas configurações
        opacity_percentage = self.config["settings"]["opacity"]
        opacity_value = int(opacity_percentage * 255 / 100)

        self.frame.setStyleSheet(f"""
            #toolbarFrame {{
                background-color: rgba(50, 50, 50, {opacity_value});
                border-radius: 10px;
                border: 1px solid rgba(100, 100, 100, 200);
            }}
            QPushButton {{
                border: none;
                border-radius: 5px;
                padding: 5px;
                background-color: rgba(70, 70, 70, 200);
            }}
            QPushButton:hover {{
                background-color: rgba(90, 90, 90, 200);
            }}
            QPushButton:pressed {{
                background-color: rgba(120, 120, 120, 200);
            }}
        """)

        # Define o layout principal do widget
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.frame)

        # Posição inicial da toolbar
        self.setGeometry(100, 100, 100, 50)

        # Posiciona conforme configuração salva
        self.apply_saved_position()

        # Variáveis para controlar o arrasto da toolbar
        self.dragging = False
        self.drag_position = None

    def load_config(self):
        """Carrega as configurações do arquivo"""
        default_config = {
            "quick_shortcuts": [
                {
                    "name": "VS Code Affiliate",
                    "icon": "",
                    "exe": "C:\\Users\\giuli\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
                    "args": ["C:\\Almatter\\afiliate"],
                    "tooltip": "Projeto Affiliate no VS Code"
                },
                {
                    "name": "Godot Projeto1",
                    "icon": "",
                    "exe": "C:\\Path\\To\\Godot\\Godot.exe",
                    "args": ["--path", "C:\\Path\\To\\GodotProject1"],
                    "tooltip": "Projeto 1 no Godot"
                }
            ],
            "categories": {
                "VS Code": [
                    {
                        "name": "Projeto Affiliate",
                        "exe": "C:\\Users\\giuli\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
                        "args": ["C:\\Almatter\\afiliate"]
                    },
                    {
                        "name": "Projeto 2",
                        "exe": "C:\\Users\\giuli\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
                        "args": ["C:\\Path\\To\\Project2"]
                    }
                ],
                "Godot": [
                    {
                        "name": "Projeto 1",
                        "exe": "C:\\Path\\To\\Godot\\Godot.exe",
                        "args": ["--path", "C:\\Path\\To\\GodotProject1"]
                    }
                ]
            },
            "settings": {
                # Valores: bottom-center, top-center, bottom-left, bottom-right, top-left, top-right
                "position": "bottom-center",
                "opacity": 80,  # Porcentagem de opacidade (0-100)
                "autostart": False  # Iniciar com o Windows
            }
        }

        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                    # Verifica se a configuração tem a chave "settings"
                    if "settings" not in config:
                        config["settings"] = default_config["settings"]
                    # Verifica se todas as configurações estão presentes
                    for key in default_config["settings"]:
                        if key not in config["settings"]:
                            config["settings"][key] = default_config["settings"][key]

                    return config
            else:
                # Cria arquivo de configuração padrão se não existir
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=4)
                return default_config
        except Exception as e:
            print(f"Erro ao carregar configurações: {e}")
            return default_config

    def save_config(self):
        """Salva as configurações no arquivo"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")

    def apply_saved_position(self):
        """Aplica a posição salva nas configurações"""
        position = self.config["settings"]["position"]
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()

        # Determina as coordenadas baseadas na posição salva
        if position == "bottom-center":
            x = (screen.width() - size.width()) // 2
            y = screen.height() - size.height() - 100
        elif position == "top-center":
            x = (screen.width() - size.width()) // 2
            y = 100
        elif position == "bottom-left":
            x = 100
            y = screen.height() - size.height() - 100
        elif position == "bottom-right":
            x = screen.width() - size.width() - 100
            y = screen.height() - size.height() - 100
        elif position == "top-left":
            x = 100
            y = 100
        elif position == "top-right":
            x = screen.width() - size.width() - 100
            y = 100
        else:
            # Posição padrão se a configuração for inválida
            x = (screen.width() - size.width()) // 2
            y = screen.height() - size.height() - 100

        self.move(x, y)

    def center_on_screen(self):
        """Posiciona a toolbar na parte inferior central da tela"""
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        size = self.geometry()

        # Posiciona 100 pixels acima da parte inferior da tela
        x = (screen.width() - size.width()) // 2
        y = screen.height() - size.height() - 100

        self.move(x, y)

    def create_toolbar_buttons(self):
        """Cria os botões da toolbar baseados na configuração"""
        # Limpa todos os botões existentes
        for i in reversed(range(self.toolbar_layout.count())):
            item = self.toolbar_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()

        # Adiciona botões diretos
        for shortcut in self.config["quick_shortcuts"]:
            btn = self.create_shortcut_button(shortcut)
            self.toolbar_layout.addWidget(btn)

        # Separador visual
        if self.config["quick_shortcuts"] and self.config["categories"]:
            separator = QtWidgets.QFrame()
            separator.setFrameShape(QtWidgets.QFrame.VLine)
            separator.setFrameShadow(QtWidgets.QFrame.Sunken)
            separator.setStyleSheet(
                "background-color: rgba(100, 100, 100, 150);")
            separator.setMaximumWidth(1)
            separator.setMinimumWidth(1)
            self.toolbar_layout.addWidget(separator)

        # Adiciona botões de categoria
        for category in self.config["categories"]:
            btn = self.create_category_button(category)
            self.toolbar_layout.addWidget(btn)

        # Adiciona os botões de controle diretamente aqui em vez de chamar add_control_buttons()
        # Separador
        separator = QtWidgets.QFrame()
        separator.setFrameShape(QtWidgets.QFrame.VLine)
        separator.setFrameShadow(QtWidgets.QFrame.Sunken)
        separator.setStyleSheet("background-color: rgba(100, 100, 100, 150);")
        separator.setMaximumWidth(1)
        separator.setMinimumWidth(1)
        self.toolbar_layout.addWidget(separator)

        # Botão para configurações
        config_btn = QtWidgets.QPushButton()
        config_btn.setIcon(self.get_settings_icon())
        config_btn.setIconSize(QtCore.QSize(20, 20))
        config_btn.setMinimumSize(36, 36)
        config_btn.setMaximumSize(36, 36)
        config_btn.setToolTip("Configurações")
        config_btn.clicked.connect(self.open_config_dialog)
        self.toolbar_layout.addWidget(config_btn)

        # Botão para movimento (simulando uma "alça" de arrasto)
        move_btn = QtWidgets.QPushButton("≡")
        move_btn.setMinimumSize(24, 36)
        move_btn.setMaximumSize(24, 36)
        move_btn.setToolTip("Mover Toolbar")
        # Instala filtro de eventos para detectar arrasto
        move_btn.installEventFilter(self)
        move_btn.setObjectName("moveBtn")
        move_btn.setStyleSheet("""
            #moveBtn {
                color: rgba(200, 200, 200, 200);
                font-size: 16px;
                font-weight: bold;
            }
        """)
        self.toolbar_layout.addWidget(move_btn)

        # Adiciona separador
        separator2 = QtWidgets.QFrame()
        separator2.setFrameShape(QtWidgets.QFrame.VLine)
        separator2.setFrameShadow(QtWidgets.QFrame.Sunken)
        separator2.setStyleSheet("background-color: rgba(100, 100, 100, 150);")
        separator2.setMaximumWidth(1)
        separator2.setMinimumWidth(1)
        self.toolbar_layout.addWidget(separator2)

        # Adiciona botão de fechar
        close_btn = QtWidgets.QPushButton("✕")
        close_btn.setObjectName("closeButton")
        close_btn.setStyleSheet("""
            #closeButton {
                background-color: transparent;
                color: #aaaaaa;
                font-weight: bold;
                border: none;
                padding: 0px;
                min-width: 20px;
                max-width: 20px;
                min-height: 36px;
                max-height: 36px;
            }
            #closeButton:hover {
                background-color: #ff4d4d;
                color: white;
                border-radius: 5px;
            }
        """)
        close_btn.setToolTip("Fechar Toolbar")
        close_btn.clicked.connect(self.close_application)
        self.toolbar_layout.addWidget(close_btn)

    def create_shortcut_button(self, shortcut):
        """Cria um botão para um atalho direto"""
        btn = QtWidgets.QPushButton(shortcut.get(
            "name", "")[0])  # Primeira letra como texto do botão

        # Tenta usar um ícone se especificado
        if shortcut.get("icon") and os.path.exists(shortcut["icon"]):
            btn.setIcon(QtGui.QIcon(shortcut["icon"]))
            btn.setText("")  # Remove o texto se tiver ícone
        else:
            # Cria um ícone colorido com a primeira letra se não tiver ícone
            pixmap = QtGui.QPixmap(32, 32)
            pixmap.fill(QtCore.Qt.transparent)

            painter = QtGui.QPainter(pixmap)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)

            # Cor de fundo aleatória mas consistente baseada no nome
            import hashlib
            name_hash = int(hashlib.md5(
                shortcut["name"].encode()).hexdigest(), 16)
            color = QtGui.QColor(name_hash % 200 + 55, (name_hash // 256) %
                                 200 + 55, (name_hash // 65536) % 200 + 55)

            painter.setBrush(QtGui.QBrush(color))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawEllipse(2, 2, 28, 28)

            painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
            painter.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
            painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter,
                             shortcut["name"][0].upper())

            painter.end()

            btn.setIcon(QtGui.QIcon(pixmap))
            btn.setText("")  # Remove o texto

        # Configura o botão
        btn.setIconSize(QtCore.QSize(24, 24))
        btn.setMinimumSize(36, 36)
        btn.setMaximumSize(36, 36)

        if shortcut.get("tooltip"):
            btn.setToolTip(shortcut["tooltip"])
        else:
            btn.setToolTip(shortcut["name"])

        # Conecta a função de lançamento
        btn.clicked.connect(lambda: self.launch_app(
            shortcut["exe"], shortcut["args"]))

        return btn

    def create_category_button(self, category):
        """Cria um botão que abre um menu com os atalhos de uma categoria"""
        # Obtém os dados da categoria (agora pode ser um dicionário ou uma string)
        category_name = category
        category_icon = ""

        # Verifica se a categoria é um dicionário com informações estendidas
        if isinstance(category, dict):
            category_name = category.get("name", "")
            category_icon = category.get("icon", "")

        # Primeira letra como texto do botão
        btn = QtWidgets.QPushButton(category_name[0])

        # Tenta usar um ícone se especificado
        if category_icon and os.path.exists(category_icon):
            btn.setIcon(QtGui.QIcon(category_icon))
            btn.setText("")  # Remove o texto se tiver ícone
        else:
            # Cria um ícone colorido para a categoria
            pixmap = QtGui.QPixmap(32, 32)
            pixmap.fill(QtCore.Qt.transparent)

            painter = QtGui.QPainter(pixmap)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)

            # Cor consistente baseada no nome da categoria
            import hashlib
            name_hash = int(hashlib.md5(
                category_name.encode()).hexdigest(), 16)
            color = QtGui.QColor(name_hash % 200 + 55, (name_hash // 256) %
                                 200 + 55, (name_hash // 65536) % 200 + 55)

            painter.setBrush(QtGui.QBrush(color))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRect(2, 2, 28, 28)

            painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 255)))
            painter.setFont(QtGui.QFont("Arial", 14, QtGui.QFont.Bold))
            painter.drawText(pixmap.rect(), QtCore.Qt.AlignCenter,
                             category_name[0].upper())

            painter.end()

            btn.setIcon(QtGui.QIcon(pixmap))
            btn.setText("")  # Remove o texto

        btn.setIconSize(QtCore.QSize(24, 24))
        btn.setMinimumSize(36, 36)
        btn.setMaximumSize(36, 36)
        btn.setToolTip(f"Projetos {category_name}")

        # Cria e conecta o menu
        menu = QtWidgets.QMenu(self)
        menu.setStyleSheet("""
            QMenu {
                background-color: rgba(60, 60, 60, 230);
                border: 1px solid rgba(100, 100, 100, 200);
                border-radius: 5px;
                padding: 5px;
            }
            QMenu::item {
                background-color: transparent;
                padding: 5px 20px 5px 20px;
                border-radius: 3px;
                color: rgba(230, 230, 230, 255);
            }
            QMenu::item:selected {
                background-color: rgba(100, 100, 100, 200);
            }
            QMenu::indicator {
                width: 0px;
                height: 0px;
            }
            QMenu::right-arrow {
                width: 0px;
                height: 0px;
                padding: 0px;
                margin: 0px;
            }
        """)

        # Obtém os atalhos da categoria
        shortcuts = self.config["categories"][category_name if isinstance(
            category, str) else category["name"]]

        for shortcut in shortcuts:
            action = menu.addAction(shortcut["name"])
            action.triggered.connect(
                lambda checked, e=shortcut["exe"], a=shortcut["args"]: self.launch_app(
                    e, a)
            )

        btn.setMenu(menu)

        # Estilo do botão para esconder a seta
        btn.setStyleSheet("""
            QPushButton::menu-indicator { 
                width: 0px; 
                image: none;
                subcontrol-position: right center;
                subcontrol-origin: padding;
                left: -2px;
            }
        """)

        return btn

    def get_settings_icon(self):
        """Cria um ícone para o botão de configurações"""
        import math

        pixmap = QtGui.QPixmap(32, 32)
        pixmap.fill(QtCore.Qt.transparent)

        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # Desenha uma engrenagem simples
        painter.setPen(QtGui.QPen(QtGui.QColor(200, 200, 200), 2))
        painter.setBrush(QtCore.Qt.NoBrush)

        painter.drawEllipse(8, 8, 16, 16)

        # Desenha os "dentes" da engrenagem
        for i in range(8):
            angle = i * 45 * math.pi / 180
            x1 = 16 + 8 * math.cos(angle)
            y1 = 16 + 8 * math.sin(angle)
            x2 = 16 + 12 * math.cos(angle)
            y2 = 16 + 12 * math.sin(angle)
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        painter.end()

        return QtGui.QIcon(pixmap)

    def eventFilter(self, obj, event):
        """Filtro de eventos para detectar arrasto do botão de movimento"""
        if obj.objectName() == "moveBtn":
            if event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.LeftButton:
                    self.dragging = True
                    self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
                    return True

            elif event.type() == QtCore.QEvent.MouseMove:
                if self.dragging and event.buttons() & QtCore.Qt.LeftButton:
                    self.move(event.globalPos() - self.drag_position)
                    return True

            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton:
                    self.dragging = False
                    return True

        return super().eventFilter(obj, event)

    def mousePressEvent(self, event):
        """Permite arrastar a toolbar inteira"""
        if event.button() == QtCore.Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Trata o clique no ícone da barra de tarefas"""
        if event.button() == QtCore.Qt.LeftButton:
            self.show_menu()

    def show_menu(self):
        """Exibe o menu de atalhos"""
        # Posição do menu - na parte superior da tela, alinhado com a janela
        pos = self.mapToGlobal(QtCore.QPoint(0, 0))
        self.menu.popup(pos)

    def mouseMoveEvent(self, event):
        """Move a toolbar ao arrastar"""
        if self.dragging and event.buttons() & QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.drag_position)

            # Ao mover manualmente, atualiza a posição nas configurações
            screen = QtWidgets.QDesktopWidget().screenGeometry()
            toolbar_pos = self.pos()
            toolbar_size = self.size()

            # Determina a posição atual para salvar
            is_left = toolbar_pos.x() < screen.width() / 3
            is_right = toolbar_pos.x() > (2 * screen.width() / 3)
            is_center = not is_left and not is_right
            is_top = toolbar_pos.y() < screen.height() / 2

            if is_top and is_center:
                self.config["settings"]["position"] = "top-center"
            elif is_top and is_left:
                self.config["settings"]["position"] = "top-left"
            elif is_top and is_right:
                self.config["settings"]["position"] = "top-right"
            elif not is_top and is_left:
                self.config["settings"]["position"] = "bottom-left"
            elif not is_top and is_right:
                self.config["settings"]["position"] = "bottom-right"
            else:
                self.config["settings"]["position"] = "bottom-center"

            # Não salva a cada movimento para não sobrecarregar o disco
            # A configuração será salva quando o aplicativo for fechado

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Para de arrastar a toolbar"""
        self.dragging = False
        super().mouseReleaseEvent(event)

    def launch_app(self, exe, args):
        """Lança um aplicativo com os argumentos especificados"""
        try:
            cmd = [exe] + args
            subprocess.Popen(cmd)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, "Erro", f"Não foi possível iniciar:\n{e}")

    def open_config_dialog(self):
        """Abre o diálogo de configuração geral"""
        dialog = ConfigDialog(self.config, self)
        if dialog.exec_():
            self.config = dialog.get_config()
            self.save_config()
            # Recria todos os botões, incluindo os botões de controle
            self.create_toolbar_buttons()

    def browse_icon_for_input(self, input_field):
        """Abre diálogo para selecionar o ícone e coloca no campo informado"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Selecionar Ícone", "", "Imagens (*.png *.jpg *.ico);;Todos os Arquivos (*.*)")
        if file_path:
            input_field.setText(file_path)

    def close_application(self):
        """Fecha a aplicação após confirmação"""
        reply = QtWidgets.QMessageBox.question(
            self, 'Confirmar Saída',
            "Deseja realmente fechar a Toolbar de Atalhos?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            # Salva todas as configurações antes de fechar
            self.save_config()
            QtWidgets.QApplication.quit()


class ConfigDialog(QtWidgets.QDialog):
    """Diálogo para configuração geral da toolbar"""

    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config.copy()

        self.setWindowTitle("Configurações da Toolbar")
        self.resize(700, 500)

        layout = QtWidgets.QVBoxLayout(self)

        # Tabs para diferentes seções de configuração
        self.tabs = QtWidgets.QTabWidget()

        # Tab para atalhos rápidos
        self.quick_tab = QtWidgets.QWidget()
        self.setup_quick_tab()

        # Tab para categorias
        self.categories_tab = QtWidgets.QWidget()
        self.setup_categories_tab()

        # Tab para configurações gerais
        self.general_tab = QtWidgets.QWidget()
        self.setup_general_tab()

        self.tabs.addTab(self.quick_tab, "Atalhos Rápidos")
        self.tabs.addTab(self.categories_tab, "Categorias")
        self.tabs.addTab(self.general_tab, "Geral")

        # Botões OK/Cancelar
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(self.tabs)
        layout.addWidget(buttons)

    def setup_quick_tab(self):
        """Configura a tab de atalhos rápidos"""
        layout = QtWidgets.QVBoxLayout(self.quick_tab)

        # Lista de atalhos rápidos
        self.quick_list = QtWidgets.QListWidget()
        self.update_quick_list()

        # Botões
        btn_layout = QtWidgets.QHBoxLayout()

        add_btn = QtWidgets.QPushButton("Adicionar")
        edit_btn = QtWidgets.QPushButton("Editar")
        remove_btn = QtWidgets.QPushButton("Remover")
        up_btn = QtWidgets.QPushButton("↑")
        down_btn = QtWidgets.QPushButton("↓")

        add_btn.clicked.connect(self.add_quick_shortcut)
        edit_btn.clicked.connect(self.edit_quick_shortcut)
        remove_btn.clicked.connect(self.remove_quick_shortcut)
        up_btn.clicked.connect(self.move_quick_up)
        down_btn.clicked.connect(self.move_quick_down)

        btn_layout.addWidget(add_btn)
        btn_layout.addWidget(edit_btn)
        btn_layout.addWidget(remove_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(up_btn)
        btn_layout.addWidget(down_btn)

        layout.addWidget(self.quick_list)
        layout.addLayout(btn_layout)

    def setup_categories_tab(self):
        """Configura a tab de categorias"""
        layout = QtWidgets.QVBoxLayout(self.categories_tab)

        # Layout dividido
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # Lista de categorias
        categories_widget = QtWidgets.QWidget()
        categories_layout = QtWidgets.QVBoxLayout(categories_widget)

        self.categories_list = QtWidgets.QListWidget()
        self.update_categories_list()

        cat_btn_layout = QtWidgets.QHBoxLayout()

        add_cat_btn = QtWidgets.QPushButton("Adicionar")
        edit_cat_btn = QtWidgets.QPushButton("Renomear")
        remove_cat_btn = QtWidgets.QPushButton("Remover")

        add_cat_btn.clicked.connect(self.add_category)
        edit_cat_btn.clicked.connect(self.edit_category)
        remove_cat_btn.clicked.connect(self.remove_category)

        cat_btn_layout.addWidget(add_cat_btn)
        cat_btn_layout.addWidget(edit_cat_btn)
        cat_btn_layout.addWidget(remove_cat_btn)

        categories_layout.addWidget(QtWidgets.QLabel("Categorias:"))
        categories_layout.addWidget(self.categories_list)
        categories_layout.addLayout(cat_btn_layout)

        # Painel para atalhos da categoria selecionada
        shortcuts_widget = QtWidgets.QWidget()
        shortcuts_layout = QtWidgets.QVBoxLayout(shortcuts_widget)

        self.shortcuts_list = QtWidgets.QListWidget()

        shortcut_btn_layout = QtWidgets.QHBoxLayout()

        add_shortcut_btn = QtWidgets.QPushButton("Adicionar")
        edit_shortcut_btn = QtWidgets.QPushButton("Editar")
        remove_shortcut_btn = QtWidgets.QPushButton("Remover")

        add_shortcut_btn.clicked.connect(self.add_category_shortcut)
        edit_shortcut_btn.clicked.connect(self.edit_category_shortcut)
        remove_shortcut_btn.clicked.connect(self.remove_category_shortcut)

        shortcut_btn_layout.addWidget(add_shortcut_btn)
        shortcut_btn_layout.addWidget(edit_shortcut_btn)
        shortcut_btn_layout.addWidget(remove_shortcut_btn)

        shortcuts_layout.addWidget(QtWidgets.QLabel("Atalhos na Categoria:"))
        shortcuts_layout.addWidget(self.shortcuts_list)
        shortcuts_layout.addLayout(shortcut_btn_layout)

        # Conecta o evento de seleção da categoria
        self.categories_list.currentItemChanged.connect(self.category_selected)

        # Adiciona os widgets ao splitter
        splitter.addWidget(categories_widget)
        splitter.addWidget(shortcuts_widget)

        layout.addWidget(splitter)

    def setup_general_tab(self):
        """Configura a tab de configurações gerais"""
        layout = QtWidgets.QVBoxLayout(self.general_tab)

        # Opção de inicializar com o Windows
        self.startup_check = QtWidgets.QCheckBox("Iniciar com o Windows")
        self.startup_check.setChecked(self.config["settings"]["autostart"])

        # Opção para posicionamento
        position_group = QtWidgets.QGroupBox("Posição na Tela")
        position_layout = QtWidgets.QVBoxLayout(position_group)

        self.position_combo = QtWidgets.QComboBox()
        self.position_combo.addItems(["Inferior Centro", "Superior Centro", "Inferior Esquerda",
                                     "Inferior Direita", "Superior Esquerda", "Superior Direita"])

        # Define o índice do combo box baseado na posição salva
        position = self.config["settings"]["position"]
        if position == "bottom-center":
            self.position_combo.setCurrentIndex(0)
        elif position == "top-center":
            self.position_combo.setCurrentIndex(1)
        elif position == "bottom-left":
            self.position_combo.setCurrentIndex(2)
        elif position == "bottom-right":
            self.position_combo.setCurrentIndex(3)
        elif position == "top-left":
            self.position_combo.setCurrentIndex(4)
        elif position == "top-right":
            self.position_combo.setCurrentIndex(5)

        apply_position_btn = QtWidgets.QPushButton("Aplicar Posição")
        apply_position_btn.clicked.connect(self.apply_position)

        position_layout.addWidget(self.position_combo)
        position_layout.addWidget(apply_position_btn)

        # Opção para transparência
        transparency_group = QtWidgets.QGroupBox("Transparência")
        transparency_layout = QtWidgets.QVBoxLayout(transparency_group)

        # Obtém o valor salvo de transparência
        current_opacity = self.config["settings"]["opacity"]

        self.transparency_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.transparency_slider.setRange(20, 100)
        self.transparency_slider.setValue(current_opacity)
        self.transparency_slider.valueChanged.connect(
            self.update_transparency_preview)

        self.transparency_label = QtWidgets.QLabel(
            f"Opacidade: {current_opacity}%")

        # Cria uma prévia da transparência
        self.preview_frame = QtWidgets.QFrame()
        self.preview_frame.setMinimumHeight(40)
        self.preview_frame.setStyleSheet(f"""
            background-color: rgba(50, 50, 50, {int(current_opacity * 255 / 100)});
            border-radius: 5px;
            border: 1px solid rgba(100, 100, 100, 200);
        """)

        apply_transparency_btn = QtWidgets.QPushButton("Aplicar Transparência")
        apply_transparency_btn.clicked.connect(self.apply_transparency)

        transparency_layout.addWidget(self.transparency_label)
        transparency_layout.addWidget(self.transparency_slider)
        transparency_layout.addWidget(self.preview_frame)
        transparency_layout.addWidget(apply_transparency_btn)

        layout.addWidget(self.startup_check)
        layout.addWidget(position_group)
        layout.addWidget(transparency_group)
        layout.addStretch()

    def update_transparency_preview(self, value):
        """Atualiza a prévia de transparência ao mover o slider"""
        self.transparency_label.setText(f"Opacidade: {value}%")
        self.preview_frame.setStyleSheet(f"""
            background-color: rgba(50, 50, 50, {int(value * 255 / 100)});
            border-radius: 5px;
            border: 1px solid rgba(100, 100, 100, 200);
        """)

    def apply_position(self):
        """Aplica a posição selecionada à toolbar"""
        position_index = self.position_combo.currentIndex()
        screen = QtWidgets.QDesktopWidget().screenGeometry()
        toolbar_size = self.parent().size()

        # Define a posição e o código de posição para salvar na configuração
        if position_index == 0:  # Inferior Centro
            x = (screen.width() - toolbar_size.width()) // 2
            y = screen.height() - toolbar_size.height() - 100
            position_code = "bottom-center"
        elif position_index == 1:  # Superior Centro
            x = (screen.width() - toolbar_size.width()) // 2
            y = 100
            position_code = "top-center"
        elif position_index == 2:  # Inferior Esquerda
            x = 100
            y = screen.height() - toolbar_size.height() - 100
            position_code = "bottom-left"
        elif position_index == 3:  # Inferior Direita
            x = screen.width() - toolbar_size.width() - 100
            y = screen.height() - toolbar_size.height() - 100
            position_code = "bottom-right"
        elif position_index == 4:  # Superior Esquerda
            x = 100
            y = 100
            position_code = "top-left"
        else:  # Superior Direita (5)
            x = screen.width() - toolbar_size.width() - 100
            y = 100
            position_code = "top-right"

        # Move a toolbar para a nova posição
        self.parent().move(x, y)

        # Salva a posição na configuração
        self.config["settings"]["position"] = position_code

        # Mostra confirmação
        position_name = self.position_combo.currentText()
        QtWidgets.QMessageBox.information(self, "Posição Aplicada",
                                          f"Toolbar movida para a posição: {position_name}")

    def apply_transparency(self):
        """Aplica a transparência selecionada à toolbar"""
        opacity = self.transparency_slider.value()
        alpha_value = int(opacity * 255 / 100)

        # Obtém o styleSheet atual da toolbar
        current_style = self.parent().frame.styleSheet()

        # Substitui o valor de transparência no background-color
        new_style = ""
        for line in current_style.split("}"):
            if "#toolbarFrame" in line and "background-color" in line:
                # Substitui o valor RGBA mantendo a cor
                parts = line.split("background-color:")
                prefix = parts[0]

                # Extrai os valores RGB do RGBA atual
                rgba_part = parts[1].split(";")[0].strip()
                try:
                    rgba_values = rgba_part.split(
                        "rgba(")[1].split(")")[0].split(",")
                    r = rgba_values[0].strip()
                    g = rgba_values[1].strip()
                    b = rgba_values[2].strip()

                    # Reconstrói com o novo valor alpha
                    new_line = f"{prefix}background-color: rgba({r}, {g}, {b}, {alpha_value});"

                    # Adiciona o resto das propriedades
                    for prop in parts[1].split(";")[1:]:
                        if prop.strip():
                            new_line += f" {prop.strip()};"

                    new_style += new_line + "}"
                except:
                    # Se falhar na extração, mantém a linha original
                    new_style += line + "}"
            else:
                new_style += line + "}" if line.strip() else ""

        # Remove o último caractere } extra
        if new_style.endswith("}"):
            new_style = new_style[:-1]

        # Aplica o novo estilo
        self.parent().frame.setStyleSheet(new_style)

        # Salva a opacidade na configuração
        self.config["settings"]["opacity"] = opacity

        # Mostra confirmação
        QtWidgets.QMessageBox.information(self, "Transparência Aplicada",
                                          f"Transparência ajustada para {opacity}%.")

    def update_quick_list(self):
        """Atualiza a lista de atalhos rápidos"""
        self.quick_list.clear()
        for shortcut in self.config["quick_shortcuts"]:
            self.quick_list.addItem(shortcut["name"])

    def update_categories_list(self):
        """Atualiza a lista de categorias"""
        self.categories_list.clear()
        for category in self.config["categories"]:
            self.categories_list.addItem(category)

    def category_selected(self, current, previous):
        """Atualiza a lista de atalhos quando uma categoria é selecionada"""
        self.shortcuts_list.clear()
        if current:
            category = current.text()
            for shortcut in self.config["categories"][category]:
                self.shortcuts_list.addItem(shortcut["name"])

    def add_quick_shortcut(self):
        """Adiciona um novo atalho rápido"""
        dialog = QuickShortcutDialog(self)
        if dialog.exec_():
            name, exe, args, icon, tooltip = dialog.get_values()
            self.config["quick_shortcuts"].append({
                "name": name,
                "exe": exe,
                "args": args,
                "icon": icon,
                "tooltip": tooltip
            })
            self.update_quick_list()

    def edit_quick_shortcut(self):
        """Edita um atalho rápido existente"""
        current_row = self.quick_list.currentRow()
        if current_row >= 0:
            shortcut = self.config["quick_shortcuts"][current_row]
            dialog = QuickShortcutDialog(
                self,
                shortcut["name"],
                shortcut["exe"],
                shortcut["args"],
                shortcut.get("icon", ""),
                shortcut.get("tooltip", "")
            )
            if dialog.exec_():
                name, exe, args, icon, tooltip = dialog.get_values()
                self.config["quick_shortcuts"][current_row] = {
                    "name": name,
                    "exe": exe,
                    "args": args,
                    "icon": icon,
                    "tooltip": tooltip
                }
                self.update_quick_list()

    def remove_quick_shortcut(self):
        """Remove um atalho rápido"""
        current_row = self.quick_list.currentRow()
        if current_row >= 0:
            reply = QtWidgets.QMessageBox.question(
                self, 'Confirmação',
                "Deseja remover este atalho rápido?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            if reply == QtWidgets.QMessageBox.Yes:
                del self.config["quick_shortcuts"][current_row]
                self.update_quick_list()

    def move_quick_up(self):
        """Move um atalho rápido para cima na lista"""
        current_row = self.quick_list.currentRow()
        if current_row > 0:
            # Troca a posição no config
            self.config["quick_shortcuts"][current_row], self.config["quick_shortcuts"][current_row-1] = \
                self.config["quick_shortcuts"][current_row -
                                               1], self.config["quick_shortcuts"][current_row]

            # Atualiza a lista e seleciona o item movido
            self.update_quick_list()
            self.quick_list.setCurrentRow(current_row - 1)

    def move_quick_down(self):
        """Move um atalho rápido para baixo na lista"""
        current_row = self.quick_list.currentRow()
        if current_row >= 0 and current_row < len(self.config["quick_shortcuts"]) - 1:
            # Troca a posição no config
            self.config["quick_shortcuts"][current_row], self.config["quick_shortcuts"][current_row+1] = \
                self.config["quick_shortcuts"][current_row +
                                               1], self.config["quick_shortcuts"][current_row]

            # Atualiza a lista e seleciona o item movido
            self.update_quick_list()
            self.quick_list.setCurrentRow(current_row + 1)

    def add_category(self):
        """Adiciona uma nova categoria"""
        # Criamos um diálogo similar ao de edição
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Nova Categoria")
        dialog.resize(450, 150)

        layout = QtWidgets.QVBoxLayout(dialog)
        form_layout = QtWidgets.QFormLayout()

        # Campo para nome
        name_input = QtWidgets.QLineEdit()
        form_layout.addRow("Nome:", name_input)

        # Campo para ícone
        icon_input = QtWidgets.QLineEdit()
        icon_layout = QtWidgets.QHBoxLayout()
        icon_layout.addWidget(icon_input)

        # Botão para procurar ícone
        browse_icon_btn = QtWidgets.QPushButton("Procurar...")
        browse_icon_btn.clicked.connect(
            lambda: self.browse_icon_for_input(icon_input))
        icon_layout.addWidget(browse_icon_btn)

        form_layout.addRow("Ícone (opcional):", icon_layout)
        layout.addLayout(form_layout)

        # Botões OK/Cancelar
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        # Executa o diálogo
        if dialog.exec_():
            name = name_input.text().strip()
            icon_path = icon_input.text().strip()

            if not name:
                QtWidgets.QMessageBox.warning(
                    self, 'Aviso', 'O nome da categoria não pode estar vazio.')
                return

            if name in self.config["categories"]:
                QtWidgets.QMessageBox.warning(
                    self, 'Aviso', 'Esta categoria já existe.')
                return

            # Criamos a categoria no novo formato (com suporte a ícones)
            self.config["categories"][name] = {
                "name": name,
                "icon": icon_path,
                "shortcuts": []  # Lista vazia de atalhos
            }

            self.update_categories_list()

            # Seleciona a nova categoria
            items = self.categories_list.findItems(
                name, QtCore.Qt.MatchExactly)
            if items:
                self.categories_list.setCurrentItem(items[0])

    def edit_category(self):
        """Renomeia uma categoria existente e permite configurar um ícone"""
        current_item = self.categories_list.currentItem()
        if current_item:
            old_name = current_item.text()

            # Criamos um diálogo para configurar a categoria
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle("Configurar Categoria")
            dialog.resize(450, 150)

            layout = QtWidgets.QVBoxLayout(dialog)
            form_layout = QtWidgets.QFormLayout()

            # Campo para nome
            name_input = QtWidgets.QLineEdit(old_name)
            form_layout.addRow("Nome:", name_input)

            # Campo para ícone
            icon_input = QtWidgets.QLineEdit()
            # Se a categoria já tiver um ícone, carregamos
            if isinstance(self.config["categories"].get(old_name), dict) and self.config["categories"][old_name].get("icon"):
                icon_input.setText(self.config["categories"][old_name]["icon"])

            icon_layout = QtWidgets.QHBoxLayout()
            icon_layout.addWidget(icon_input)

            # Botão para procurar ícone
            browse_icon_btn = QtWidgets.QPushButton("Procurar...")
            browse_icon_btn.clicked.connect(
                lambda: self.browse_icon_for_input(icon_input))
            icon_layout.addWidget(browse_icon_btn)

            form_layout.addRow("Ícone (opcional):", icon_layout)
            layout.addLayout(form_layout)

            # Botões OK/Cancelar
            buttons = QtWidgets.QDialogButtonBox(
                QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
                QtCore.Qt.Horizontal)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)

            # Executa o diálogo
            if dialog.exec_():
                new_name = name_input.text().strip()
                icon_path = icon_input.text().strip()

                if not new_name:
                    QtWidgets.QMessageBox.warning(
                        self, 'Aviso', 'O nome da categoria não pode estar vazio.')
                    return

                if new_name != old_name and new_name in self.config["categories"]:
                    QtWidgets.QMessageBox.warning(
                        self, 'Aviso', 'Esta categoria já existe.')
                    return

                # Convertemos a estrutura de categorias para suportar ícones
                if new_name != old_name:
                    # Criamos a nova entrada com o novo nome e ícone
                    if isinstance(self.config["categories"][old_name], list):
                        # Se for lista (formato antigo), convertemos para dict
                        self.config["categories"][new_name] = {
                            "name": new_name,
                            "icon": icon_path,
                            "shortcuts": self.config["categories"][old_name]
                        }
                    else:
                        # Se já for dict, mantemos a estrutura
                        self.config["categories"][new_name] = self.config["categories"][old_name]
                        self.config["categories"][new_name]["name"] = new_name
                        self.config["categories"][new_name]["icon"] = icon_path

                    # Removemos a entrada antiga
                    del self.config["categories"][old_name]
                else:
                    # Apenas atualizamos o ícone
                    if isinstance(self.config["categories"][old_name], list):
                        # Convertemos para dict
                        self.config["categories"][old_name] = {
                            "name": old_name,
                            "icon": icon_path,
                            "shortcuts": self.config["categories"][old_name]
                        }
                    else:
                        # Atualizamos o ícone
                        self.config["categories"][old_name]["icon"] = icon_path

                self.update_categories_list()

                # Seleciona a categoria renomeada/atualizada
                items = self.categories_list.findItems(
                    new_name, QtCore.Qt.MatchExactly)
                if items:
                    self.categories_list.setCurrentItem(items[0])

    def remove_category(self):
        """Remove uma categoria existente"""
        current_item = self.categories_list.currentItem()
        if current_item:
            category = current_item.text()

            reply = QtWidgets.QMessageBox.question(
                self, 'Confirmação',
                f"Deseja remover a categoria '{category}' e todos os seus atalhos?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )

            if reply == QtWidgets.QMessageBox.Yes:
                del self.config["categories"][category]
                self.update_categories_list()
                self.shortcuts_list.clear()

    def add_category_shortcut(self):
        """Adiciona um atalho a uma categoria"""
        current_category = self.categories_list.currentItem()
        if current_category:
            category = current_category.text()

            dialog = ShortcutDialog(self)
            if dialog.exec_():
                name, exe, args = dialog.get_values()
                self.config["categories"][category].append({
                    "name": name,
                    "exe": exe,
                    "args": args
                })

                # Atualiza a lista de atalhos
                self.shortcuts_list.addItem(name)

    def edit_category_shortcut(self):
        """Edita um atalho em uma categoria"""
        current_category = self.categories_list.currentItem()
        current_shortcut = self.shortcuts_list.currentRow()

        if current_category and current_shortcut >= 0:
            category = current_category.text()
            shortcut = self.config["categories"][category][current_shortcut]

            dialog = ShortcutDialog(
                self,
                shortcut["name"],
                shortcut["exe"],
                shortcut["args"]
            )

            if dialog.exec_():
                name, exe, args = dialog.get_values()
                self.config["categories"][category][current_shortcut] = {
                    "name": name,
                    "exe": exe,
                    "args": args
                }

                # Atualiza o item na lista
                self.shortcuts_list.item(current_shortcut).setText(name)

    def remove_category_shortcut(self):
        """Remove um atalho de uma categoria"""
        current_category = self.categories_list.currentItem()
        current_shortcut = self.shortcuts_list.currentRow()

        if current_category and current_shortcut >= 0:
            category = current_category.text()

            reply = QtWidgets.QMessageBox.question(
                self, 'Confirmação',
                "Deseja remover este atalho?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )

            if reply == QtWidgets.QMessageBox.Yes:
                del self.config["categories"][category][current_shortcut]
                self.shortcuts_list.takeItem(current_shortcut)

    def is_in_startup(self):
        """Verifica se o aplicativo está configurado para iniciar com o Windows"""
        import os
        startup_path = os.path.join(os.getenv('APPDATA'),
                                    r'Microsoft\Windows\Start Menu\Programs\Startup')
        script_path = os.path.abspath(sys.argv[0])
        shortcut_path = os.path.join(startup_path, 'FloatingToolbar.lnk')

        return os.path.exists(shortcut_path)

    def set_startup(self, enable):
        """Configura o aplicativo para iniciar com o Windows"""
        import os
        import sys
        import pythoncom
        from win32com.shell import shell, shellcon

        startup_path = os.path.join(os.getenv('APPDATA'),
                                    r'Microsoft\Windows\Start Menu\Programs\Startup')
        script_path = os.path.abspath(sys.argv[0])
        shortcut_path = os.path.join(startup_path, 'FloatingToolbar.lnk')

        if enable:
            # Cria um atalho para o script no diretório de inicialização
            shortcut = pythoncom.CoCreateInstance(
                shell.CLSID_ShellLink,
                None,
                pythoncom.CLSCTX_INPROC_SERVER,
                shell.IID_IShellLink
            )

            shortcut.SetPath(sys.executable)
            shortcut.SetArguments(f'"{script_path}"')
            shortcut.SetWorkingDirectory(os.path.dirname(script_path))

            # Salva o atalho
            persist_file = shortcut.QueryInterface(pythoncom.IID_IPersistFile)
            persist_file.Save(shortcut_path, 0)
        else:
            # Remove o atalho se ele existir
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)

    def accept(self):
        """Salva as configurações ao aceitar o diálogo"""
        # Configura inicialização com Windows
        try:
            autostart = self.startup_check.isChecked()
            self.set_startup(autostart)
            self.config["settings"]["autostart"] = autostart
        except:
            QtWidgets.QMessageBox.warning(
                self, 'Aviso',
                "Não foi possível configurar a inicialização automática. Verifique se o módulo pywin32 está instalado."
            )

        # Salva as configurações atualizadas no arquivo
        self.parent().save_config()

        super().accept()

    def get_config(self):
        """Retorna a configuração atualizada"""
        return self.config


class QuickShortcutDialog(QtWidgets.QDialog):
    """Diálogo para adicionar ou editar um atalho rápido"""

    def __init__(self, parent=None, name="", exe="", args=None, icon="", tooltip=""):
        super().__init__(parent)
        self.setWindowTitle("Configurar Atalho Rápido")
        self.resize(500, 300)

        if args is None:
            args = []

        layout = QtWidgets.QVBoxLayout(self)

        form_layout = QtWidgets.QFormLayout()

        self.name_input = QtWidgets.QLineEdit(name)
        self.exe_input = QtWidgets.QLineEdit(exe)
        self.args_input = QtWidgets.QLineEdit(
            " ".join(args) if isinstance(args, list) else args)
        self.icon_input = QtWidgets.QLineEdit(icon)
        self.tooltip_input = QtWidgets.QLineEdit(tooltip)

        browse_exe_btn = QtWidgets.QPushButton("Procurar...")
        browse_exe_btn.clicked.connect(self.browse_exe)

        browse_icon_btn = QtWidgets.QPushButton("Procurar...")
        browse_icon_btn.clicked.connect(self.browse_icon)

        exe_layout = QtWidgets.QHBoxLayout()
        exe_layout.addWidget(self.exe_input)
        exe_layout.addWidget(browse_exe_btn)

        icon_layout = QtWidgets.QHBoxLayout()
        icon_layout.addWidget(self.icon_input)
        icon_layout.addWidget(browse_icon_btn)

        form_layout.addRow("Nome:", self.name_input)
        form_layout.addRow("Executável:", exe_layout)
        form_layout.addRow("Argumentos:", self.args_input)
        form_layout.addRow("Ícone (opcional):", icon_layout)
        form_layout.addRow("Dica de Ferramenta:", self.tooltip_input)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(buttons)

    def browse_exe(self):
        """Abre diálogo para selecionar o executável"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Selecionar Executável", "", "Executáveis (*.exe);;Todos os Arquivos (*.*)")
        if file_path:
            self.exe_input.setText(file_path)

    def browse_icon(self):
        """Abre diálogo para selecionar o ícone"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Selecionar Ícone", "", "Imagens (*.png *.jpg *.ico);;Todos os Arquivos (*.*)")
        if file_path:
            self.icon_input.setText(file_path)

    def get_values(self):
        """Retorna os valores do atalho rápido"""
        name = self.name_input.text().strip()
        exe = self.exe_input.text().strip()
        args = self.args_input.text().strip().split()
        icon = self.icon_input.text().strip()
        tooltip = self.tooltip_input.text().strip()
        return name, exe, args, icon, tooltip


class ShortcutDialog(QtWidgets.QDialog):
    """Diálogo para adicionar ou editar um atalho"""

    def __init__(self, parent=None, name="", exe="", args=None):
        super().__init__(parent)
        self.setWindowTitle("Configurar Atalho")
        self.resize(500, 200)

        if args is None:
            args = []

        layout = QtWidgets.QVBoxLayout(self)

        form_layout = QtWidgets.QFormLayout()

        self.name_input = QtWidgets.QLineEdit(name)
        self.exe_input = QtWidgets.QLineEdit(exe)
        self.args_input = QtWidgets.QLineEdit(
            " ".join(args) if isinstance(args, list) else args)

        browse_btn = QtWidgets.QPushButton("Procurar...")
        browse_btn.clicked.connect(self.browse_exe)

        exe_layout = QtWidgets.QHBoxLayout()
        exe_layout.addWidget(self.exe_input)
        exe_layout.addWidget(browse_btn)

        form_layout.addRow("Nome:", self.name_input)
        form_layout.addRow("Executável:", exe_layout)
        form_layout.addRow("Argumentos:", self.args_input)

        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
            QtCore.Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(buttons)

    def browse_exe(self):
        """Abre diálogo para selecionar o executável"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Selecionar Executável", "", "Executáveis (*.exe);;Todos os Arquivos (*.*)")
        if file_path:
            self.exe_input.setText(file_path)

    def get_values(self):
        """Retorna os valores do atalho"""
        name = self.name_input.text().strip()
        exe = self.exe_input.text().strip()
        args = self.args_input.text().strip().split()
        return name, exe, args


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    toolbar = FloatingToolbar()
    toolbar.show()
    sys.exit(app.exec_())
