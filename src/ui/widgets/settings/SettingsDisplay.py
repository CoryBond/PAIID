
import logging
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QScrollArea, QPushButton, QStackedWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QFont

from typing import List, Optional

from ui.widgets.common.QLine import QHLine
from ui.widgets.home.ImageMeta import ImageMetaInfo
from ui.widgets.settings.SettingsPage import SettingsPage


class SettingsDisplay(QScrollArea):
    """
    QT Widget to display a single page worth of settings.

    Attributes
    ----------
    wifi_changed : pyqtSignal
        Signal emitted when WiFi settings change

    Methods
    ----------
    show_wifi_settings()
        Shows the WiFi settings page
    show_main_settings()
        Shows the main settings page
    """
    wifi_changed = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.init_ui()


    def init_ui(self):
        """Initialize the UI with stacked widget for different settings pages"""
        self.stacked_widget = QStackedWidget()
        self.setWidget(self.stacked_widget)
        
        # Main settings page
        self.main_settings_widget = self.create_main_settings_widget()
        self.stacked_widget.addWidget(self.main_settings_widget)
        
        # WiFi settings page
        self.wifi_settings_page = SettingsPage()
        self.wifi_settings_page.wifi_changed.connect(self._on_wifi_changed)
        self.stacked_widget.addWidget(self.wifi_settings_page)
        
        # Show main settings by default
        self.show_main_settings()


    def create_main_settings_widget(self) -> QWidget:
        """Create the main settings widget with navigation"""
        main_widget = QWidget()
        layout = QVBoxLayout()
        main_widget.setLayout(layout)
        
        # Title
        title = QLabel("Settings")
        title_font = title.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Settings Options
        options_label = QLabel("Available Settings:")
        options_font = options_label.font()
        options_font.setPointSize(12)
        options_font.setBold(True)
        options_label.setFont(options_font)
        layout.addWidget(options_label)
        
        # WiFi Settings Button
        wifi_btn = QPushButton("WiFi Settings")
        wifi_btn.setMinimumHeight(50)
        wifi_btn.clicked.connect(self.show_wifi_settings)
        layout.addWidget(wifi_btn)
        
        # Add more settings options here as needed
        # Example: Display Settings, Audio Settings, etc.
        
        layout.addStretch()
        return main_widget


    def show_wifi_settings(self):
        """Navigate to WiFi settings page"""
        self.stacked_widget.setCurrentWidget(self.wifi_settings_page)


    def show_main_settings(self):
        """Navigate back to main settings page"""
        self.stacked_widget.setCurrentWidget(self.main_settings_widget)


    def _on_wifi_changed(self):
        """Handle WiFi change signal"""
        self.wifi_changed.emit()


    def create_scrollable_widget(self):
        """Create a scrollable widget container"""
        layout = QVBoxLayout()
        childWidget = QWidget()
        childWidget.setLayout(layout)
        return childWidget