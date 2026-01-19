import logging
import subprocess
from typing import List
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, 
    QListWidget, QListWidgetItem, QInputDialog, QMessageBox, QLineEdit
)
from PyQt5.QtCore import pyqtSignal, Qt, QThread, QDir

from ui.dialogs.ErrorMessage import ErrorMessage


class WiFiWorker(QThread):
    """Worker thread to handle WiFi operations without freezing the UI"""
    networks_found = pyqtSignal(list)  # Emits list of available networks
    connection_status = pyqtSignal(str, bool)  # Emits (status_message, is_success)
    error_occurred = pyqtSignal(str)  # Emits error message
    
    def __init__(self, operation: str, **kwargs):
        super().__init__()
        self.operation = operation
        self.kwargs = kwargs
    
    def run(self):
        try:
            if self.operation == "scan":
                self._scan_networks()
            elif self.operation == "connect":
                self._connect_to_network()
            elif self.operation == "get_current":
                self._get_current_network()
        except Exception as e:
            logging.error(f"WiFi worker error: {e}")
            self.error_occurred.emit(str(e))
    
    def _scan_networks(self):
        """Scan for available WiFi networks"""
        try:
            # Using nmcli (NetworkManager CLI) which is more reliable
            result = subprocess.run(
                ['sudo', 'nmcli', 'dev', 'wifi', 'list'],
                capture_output=True,
                text=True,
                timeout=10
            )
  
            if result.returncode == 0:
                logging.info(f"Got wifi scan result: {result}")
                networks = self._parse_nmcli_output(result.stdout)
                logging.info(f"Got wifi scan networks: {networks}")
                self.networks_found.emit(networks)
            else:
                self.error_occurred.emit(f"Scan failed: {result.stderr}")
        except FileNotFoundError:
            self.error_occurred.emit("nmcli not found. Please install NetworkManager.")
        except subprocess.TimeoutExpired:
            self.error_occurred.emit("WiFi scan timed out.")
    
    def _parse_nmcli_output(self, output: str) -> List[dict]:
        """Parse nmcli output to extract network information"""
        networks = []
        lines = output.strip().split('\n')
        
        if len(lines) > 0:
            # Skip header line
            for line in lines[1:]:
                # Need to skip the "*" character that indicates what network is connected.
                parts = line.lstrip("* ").split()
                if len(parts) >= 7:
                    network_info = {
                        'ssid': parts[0],
                        'bssid': parts[1],
                        'mode': parts[2],
                        'channel': parts[3],
                        'rate': parts[4],
                        'signal': parts[5],
                        'bars': parts[6]
                    }
                    networks.append(network_info)
        
        return networks
    
    def _connect_to_network(self):
        """Connect to a WiFi network"""
        ssid = self.kwargs.get('ssid')
        password = self.kwargs.get('password', '')
        
        try:
            if password:
                cmd = ['sudo', 'nmcli', 'dev', 'wifi', 'connect', ssid, 'password', password]
            else:
                cmd = ['sudo', 'nmcli', 'dev', 'wifi', 'connect', ssid]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=15
            )
            
            if result.returncode == 0:
                self.connection_status.emit(f"Connected to {ssid}", True)
            else:
                self.connection_status.emit(f"Failed to connect: {result.stderr}", False)
        except Exception as e:
            self.connection_status.emit(f"Connection error: {str(e)}", False)
    
    def _get_current_network(self):
        """Get currently connected WiFi network"""
        try:
            result = subprocess.run(
                ['nmcli', '-t', '-f', 'active,ssid', 'dev', 'wifi'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line.startswith('yes'):
                        ssid = line.split(':', 1)[1].strip() if ':' in line else 'Unknown'
                        self.connection_status.emit(f"Connected to: {ssid}", True)
                        return
                self.connection_status.emit("Not connected to any network", False)
            else:
                self.connection_status.emit("Unable to retrieve connection info", False)
        except Exception as e:
            self.connection_status.emit(f"Error: {str(e)}", False)


class SettingsPage(QWidget):
    """
    Settings page for the application with WiFi management capabilities.
    
    Attributes
    ----------
    wifi_changed = pyqtSignal()
        Signal emitted when WiFi settings are changed
    
    Methods
    -------
    scan_networks()
        Scans for available WiFi networks
    connect_to_network(ssid, password)
        Connects to a specified WiFi network
    refresh_current_network()
        Updates the display of the currently connected network
    """
    
    wifi_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_network = None
        self.wifi_worker = None
        self.init_ui()
        self.refresh_current_network()
    
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Title
        title = QLabel("Settings")
        title_font = title.font()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # WiFi Section
        layout.addWidget(self._create_separator("WiFi Settings"))
        
        # Current Connection Display
        current_label = QLabel("Current Connection:")
        current_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(current_label)
        
        self.current_connection_label = QLabel("Checking connection...")
        self.current_connection_label.setStyleSheet("color: #666666; margin-left: 20px;")
        layout.addWidget(self.current_connection_label)
        
        # Buttons Layout for WiFi Controls
        wifi_controls_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("Refresh Current Network")
        refresh_btn.clicked.connect(self.refresh_current_network)
        wifi_controls_layout.addWidget(refresh_btn)
        
        scan_btn = QPushButton("Scan for Networks")
        scan_btn.clicked.connect(self.scan_networks)
        wifi_controls_layout.addWidget(scan_btn)
        
        layout.addLayout(wifi_controls_layout)
        
        # Available Networks Section
        available_label = QLabel("Available Networks:")
        available_label.setStyleSheet("font-weight: bold; margin-top: 20px;")
        layout.addWidget(available_label)
        
        self.networks_list = QListWidget()
        layout.addWidget(self.networks_list)
        
        # Connection Controls
        connection_controls_layout = QHBoxLayout()
        
        connect_btn = QPushButton("Connect to Selected")
        connect_btn.clicked.connect(self._connect_to_selected)
        connection_controls_layout.addWidget(connect_btn)
        
        # Don't allow users to disconnect the current wifi. 
        #disconnect_btn = QPushButton("Disconnect")
        #disconnect_btn.clicked.connect(self._disconnect_network)
        #connection_controls_layout.addWidget(disconnect_btn)
        
        layout.addLayout(connection_controls_layout)
        
        # Add stretch to push everything to the top
        layout.addStretch()
    
    def _create_separator(self, text: str) -> QLabel:
        """Create a visual separator with text"""
        separator = QLabel(text)
        separator.setStyleSheet("font-size: 14px; font-weight: bold; margin-top: 20px; margin-bottom: 10px;")
        return separator
    
    def scan_networks(self):
        """Scan for available WiFi networks"""
        logging.info("Scanning for WiFi networks...")
        self.networks_list.clear()
        
        # Add loading indicator
        loading_item = QListWidgetItem("Scanning networks...")
        loading_item.setFlags(loading_item.flags() & ~Qt.ItemIsSelectable)
        self.networks_list.addItem(loading_item)
        
        # Create and start worker thread
        self.wifi_worker = WiFiWorker("scan")
        self.wifi_worker.networks_found.connect(self._on_networks_found)
        self.wifi_worker.error_occurred.connect(self._on_wifi_error)
        self.wifi_worker.start()
    
    def _on_networks_found(self, networks: List[dict]):
        """Handle networks found from scan"""
        logging.info(f"Found {len(networks)} networks")
        
        if not networks:
            item = QListWidgetItem("No networks found")
            item.setFlags(item.flags() & ~Qt.ItemIsSelectable)
            self.networks_list.addItem(item)
            return

        for network in networks:
            bssid = network.get('bssid', "Unkown")
            rate = network.get('rate', 'Unknown')
            signal = network.get('signal', 'Unknown')
            item_text = f"{bssid} (Signal: {rate}{signal})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, network)
            self.networks_list.addItem(item)
    
    def refresh_current_network(self):
        """Refresh the currently connected network"""
        logging.info("Refreshing current network info...")
        self.wifi_worker = WiFiWorker("get_current")
        self.wifi_worker.connection_status.connect(self._on_connection_status)
        self.wifi_worker.error_occurred.connect(self._on_wifi_error)
        self.wifi_worker.start()
    
    def _on_connection_status(self, status: str, is_connected: bool):
        """Handle connection status updates"""
        self.current_connection_label.setText(status)
        if is_connected:
            self.current_connection_label.setStyleSheet("color: #00AA00; margin-left: 20px;")
        else:
            self.current_connection_label.setStyleSheet("color: #AA0000; margin-left: 20px;")
        self.current_network = status
    
    def _connect_to_selected(self):
        """Connect to the selected network"""
        current_item = self.networks_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a network to connect to.")
            return
        
        network = current_item.data(Qt.UserRole)
        logging.info(f"Connect clicked with {network} selected")
        if not network:
            QMessageBox.warning(self, "Error", "Invalid network selected.")
            return
        
        # Prompt for password
        # NOTE: Dialog windows don't work well with the virtual keyboard as the dialog eats events sent to the Virtual Keyboard.
        # See: https://qt-project.atlassian.net/browse/QTBUG-56918 for a deeper conversation on this.
        # TODO: Find a way to make the virtual keyboard work with dialogs!
        password, ok = QInputDialog.getText(self, network.get('bssid', 'Unknown'),
                                "Password (Virtual Keyboard Not Supported):", QLineEdit.Normal,
                                QDir.home().dirName())
        
        if ok:
            self._connect_to_network(network, password)
    
    def _connect_to_network(self, network: dict, password: str = ""):
        """Connect to a WiFi network"""
        ssid = network.get('ssid', '')
        bssid = network.get('bssid', '')
        logging.info(f"Attempting to connect to {bssid} - {ssid}...")
        
        # Show progress
        self.networks_list.clear()
        loading_item = QListWidgetItem(f"Connecting to {bssid} - {ssid}...")
        loading_item.setFlags(loading_item.flags() & ~Qt.ItemIsSelectable)
        self.networks_list.addItem(loading_item)
        
        # Create and start worker thread
        self.wifi_worker = WiFiWorker("connect", ssid=ssid, password=password)
        self.wifi_worker.connection_status.connect(self._on_connect_result)
        self.wifi_worker.error_occurred.connect(self._on_wifi_error)
        self.wifi_worker.start()
    
    def _on_connect_result(self, status: str, is_success: bool):
        """Handle connection result"""
        if is_success:
            QMessageBox.information(self, "Success", status)
            self.wifi_changed.emit()
            self.refresh_current_network()
            self.scan_networks()
        else:
            QMessageBox.warning(self, "Connection Failed", status)
            self.scan_networks()

    """
    def _disconnect_network(self):
        ""Disconnect from current network""
        reply = QMessageBox.question(
            self,
            "Disconnect",
            "Are you sure you want to disconnect?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                subprocess.run(
                    ['nmcli', 'dev', 'disconnect'],
                    capture_output=True,
                    timeout=5
                )
                QMessageBox.information(self, "Disconnected", "WiFi disconnected successfully.")
                self.refresh_current_network()
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to disconnect: {str(e)}")
    """

    def _on_wifi_error(self, error: str):
        """Handle WiFi operation errors"""
        logging.error(f"WiFi error: {error}")
        self.networks_list.clear()
        
        error_item = QListWidgetItem(f"Error: {error}")
        error_item.setFlags(error_item.flags() & ~Qt.ItemIsSelectable)
        error_item.setForeground(Qt.red)
        self.networks_list.addItem(error_item)
        
        QMessageBox.warning(self, "WiFi Error", error)