import sys
import os
import random
import json
import subprocess
import re
from datetime import datetime, time as dt_time, timedelta
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QScrollArea,
    QGroupBox, QTimeEdit, QCheckBox, QFileDialog, QTableWidget,
    QTableWidgetItem, QHeaderView, QAbstractItemView, QSizePolicy, QRadioButton,
    QComboBox
)
from PyQt6.QtCore import QThread, pyqtSignal, QObject, QTimer, QTime, Qt
from PyQt6.QtGui import QIntValidator, QAction

# Bot modülleri
import den
import fonksiyonlar

class Kontrol(QObject):
    def __init__(self):
        super().__init__()
        self.durdur = False

class BotThread(QThread):
    log = pyqtSignal(str)
    finished = pyqtSignal(str)
    actually_finished = pyqtSignal(str)

    def __init__(self, device_id, kontrol, params):
        super().__init__()
        self.device_id = device_id
        self.kontrol = kontrol
        self.params = params
        self.generated_values = {}
        self._is_running = True

    def run(self):
        try:
            os.environ["ANDROID_SERIAL"] = self.device_id
            self.log.emit(f"✅ {self.device_id}: Bağlantı başarılı")
            
            self.generated_values['begen'] = random.randint(*self.params['begen'])
            self.generated_values['yorum'] = random.randint(*self.params['yorum'])
            self.generated_values['kaydet'] = random.randint(*self.params['kaydet'])
            self.generated_values['takip'] = random.randint(*self.params['takip'])
            self.generated_values['kaydir'] = random.randint(*self.params['kaydir'])
            self.generated_values['sure'] = random.randint(*self.params['sure'])

            self.log.emit(f"⚙️ {self.device_id}: Üretilen değerler - "
                         f"Beğeni: {self.generated_values['begen']}, "
                         f"Yorum: {self.generated_values['yorum']}, "
                         f"Kaydet: {self.generated_values['kaydet']}, "
                         f"Takip: {self.generated_values['takip']}, "
                         f"Kaydır: {self.generated_values['kaydir']}, "
                         f"Süre: {self.generated_values['sure']}s")

            result = den.hepsi(
                self.generated_values['begen'], 
                self.generated_values['yorum'], 
                self.generated_values['kaydet'],
                self.generated_values['takip'], 
                self.generated_values['kaydir'], 
                self.generated_values['sure'], 
                self.kontrol
            )
            
            if not self.kontrol.durdur:
                self.log.emit(f"✅ {self.device_id}: Bot tamamlandı - {result}")
                self.actually_finished.emit(self.device_id)
            
        except Exception as e:
            self.log.emit(f"❌ {self.device_id}: Hata - {str(e)}")
        finally:
            self._is_running = False
            self.finished.emit(self.device_id)

    def stop(self):
        self._is_running = False
        self.kontrol.durdur = True

    def __del__(self):
        self.wait()

class ScheduleTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(4)
        self.setHorizontalHeaderLabels(["Başlangıç", "Bitiş", "Eylem", "Değerler"])
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setEditTriggers(QAbstractItemView.EditTrigger.DoubleClicked | QAbstractItemView.EditTrigger.EditKeyPressed)
        self.setRowCount(0)

    def add_time_range(self, start_time="09:00:00", end_time="18:00:00", action="run_only", values=None):
        row = self.rowCount()
        self.insertRow(row)
        self.setItem(row, 0, QTableWidgetItem(start_time))
        self.setItem(row, 1, QTableWidgetItem(end_time))
    
        combo = QComboBox()
        combo.addItem("Sadece Botu Çalıştır", "run_only")
        combo.addItem("Sadece Emülatörü Başlat", "launch_only")
        combo.addItem("Sadece Emülatörü Kapat", "quit_only")
        combo.addItem("Emülatörü Başlat + Botu Çalıştır + Emülatörü Kapat", "launch_and_run")
        combo.addItem("Emülatörü Başlat + Bot Çalıştır", "launch_run_stop")
        combo.addItem("Kullanıcı Profilini Aç", "open_profile")
        combo.addItem("En Üstteki Takip Et", "enust_takip")
        combo.setCurrentIndex(combo.findData(action))
        self.setCellWidget(row, 2, combo)
     
        if values:
            values_text = (f"Beğeni: {values.get('begen', '?')}, "
                         f"Yorum: {values.get('yorum', '?')}, "
                         f"Kaydet: {values.get('kaydet', '?')}, "
                         f"Takip: {values.get('takip', '?')}, "
                         f"Kaydır: {values.get('kaydir', '?')}, "
                         f"Süre: {values.get('sure', '?')}s")
        else:
            values_text = "Değerler yok"
         
        self.setItem(row, 3, QTableWidgetItem(values_text))

    def get_schedules(self):
        schedules = []
        for row in range(self.rowCount()):
            start = self.item(row, 0).text()
            end = self.item(row, 1).text()
            action = self.cellWidget(row, 2).currentData()
            values_text = self.item(row, 3).text()
            
            values = {}
            parts = values_text.split(", ")
            for part in parts:
                if ":" in part:
                    key, val = part.split(": ", 1)
                    if key == "Süre":
                        val = val.replace("s", "")
                    values[key.lower()] = int(val) if val.isdigit() else val
            
            schedules.append({
                "start": start, 
                "end": end,
                "action": action,
                "values": {
                    'begen': values.get('beğeni', 0),
                    'yorum': values.get('yorum', 0),
                    'kaydet': values.get('kaydet', 0),
                    'takip': values.get('takip', 0),
                    'kaydir': values.get('kaydır', 0),
                    'sure': values.get('süre', 0)
                }
            })
        return schedules

    def set_schedules(self, schedules):
        self.setRowCount(0)
        for schedule in schedules:
            self.add_time_range(
                schedule.get("start", "09:00:00"), 
                schedule.get("end", "18:00:00"),
                schedule.get("action", "run_only"),
                schedule.get("values")
            )

class DeviceTab(QWidget):
    def __init__(self, device_id, parent=None):
        super().__init__(parent)
        self.device_id = device_id
        self.parent = parent
        self.thread = None
        self.kontrol = Kontrol()
        self.scheduler_enabled = False
        self.emulator_index = "0"
        self.schedule_option = "run_only"
        self.wait_time = 30
        self.shutdown_delay = 10
        self.emulator_quit_timer = None
        self.user_profile = ""
        
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Device header
        header = QHBoxLayout()
        header.addWidget(QLabel(f"Cihaz: {self.device_id}"))
        
        self.remove_btn = QPushButton("Kaldır")
        self.remove_btn.clicked.connect(self.remove_device)
        header.addWidget(self.remove_btn)
        layout.addLayout(header)

        # Emulator control section
        emulator_group = QGroupBox("Emülatör Kontrol")
        emulator_layout = QHBoxLayout()
        
        emulator_layout.addWidget(QLabel("LDPlayer Index:"))
        self.emulator_index_input = QLineEdit("0")
        self.emulator_index_input.setValidator(QIntValidator(0, 999999))
        emulator_layout.addWidget(self.emulator_index_input)
        
        self.launch_btn = QPushButton("Başlat")
        self.launch_btn.clicked.connect(self.launch_emulator)
        emulator_layout.addWidget(self.launch_btn)
        
        self.quit_btn = QPushButton("Durdur")
        self.quit_btn.clicked.connect(self.quit_emulator)
        emulator_layout.addWidget(self.quit_btn)
        
        emulator_group.setLayout(emulator_layout)
        layout.addWidget(emulator_group)

        # User profile configuration
        user_profile_group = QGroupBox("Instagram Kullanıcı Adı")
        user_profile_layout = QHBoxLayout()
        
        user_profile_layout.addWidget(QLabel("Kullanıcı Adı:"))
        self.user_profile_input = QLineEdit()
        self.user_profile_input.setPlaceholderText("profil_adı")
        self.user_profile_input.textChanged.connect(self.update_user_profile)
        user_profile_layout.addWidget(self.user_profile_input)
        
        self.profile_btn = QPushButton("Profil Aç")
        self.profile_btn.clicked.connect(self.open_profile)
        user_profile_layout.addWidget(self.profile_btn)
        
        user_profile_group.setLayout(user_profile_layout)
        layout.addWidget(user_profile_group)

        # Scheduler section
        schedule_group = QGroupBox("Zamanlayıcı Ayarları")
        schedule_layout = QVBoxLayout()
        
        self.schedule_table = ScheduleTable()
        schedule_layout.addWidget(self.schedule_table)
        
        time_control_layout = QHBoxLayout()
        
        self.start_time = QTimeEdit()
        self.start_time.setDisplayFormat("HH:mm:ss")
        self.start_time.setTime(QTime(9, 0, 0))
        time_control_layout.addWidget(self.start_time)
        
        self.end_time = QTimeEdit()
        self.end_time.setDisplayFormat("HH:mm:ss")
        self.end_time.setTime(QTime(18, 0, 0))
        time_control_layout.addWidget(self.end_time)
        
        add_btn = QPushButton("Ekle")
        add_btn.clicked.connect(self.add_schedule_time)
        time_control_layout.addWidget(add_btn)
        
        remove_btn = QPushButton("Sil")
        remove_btn.clicked.connect(self.remove_schedule_time)
        time_control_layout.addWidget(remove_btn)
        
        edit_btn = QPushButton("Düzenle")
        edit_btn.clicked.connect(self.edit_schedule_time)
        time_control_layout.addWidget(edit_btn)
        
        schedule_layout.addLayout(time_control_layout)
        
        # Schedule options
        options_group = QGroupBox("Zamanlayıcı Eylemi")
        options_layout = QVBoxLayout()

        first_row = QHBoxLayout()
        self.run_only_option = QRadioButton("Sadece Botu Çalıştır")
        self.run_only_option.setChecked(True)
        self.run_only_option.toggled.connect(lambda: self.set_schedule_option("run_only"))
        first_row.addWidget(self.run_only_option)
   
        self.launch_only_option = QRadioButton("Sadece Emülatörü Başlat")
        self.launch_only_option.toggled.connect(lambda: self.set_schedule_option("launch_only"))
        first_row.addWidget(self.launch_only_option)

        self.quit_only_option = QRadioButton("Sadece Emülatörü Kapat")
        self.quit_only_option.toggled.connect(lambda: self.set_schedule_option("quit_only"))
        first_row.addWidget(self.quit_only_option)

        options_layout.addLayout(first_row)

        second_row = QHBoxLayout()
        self.launch_and_run_option = QRadioButton("Emülatörü Başlat + Botu Çalıştır + Emülatörü Kapat")
        self.launch_and_run_option.toggled.connect(lambda: self.set_schedule_option("launch_and_run"))
        second_row.addWidget(self.launch_and_run_option)
       
        self.launch_run_stop_option = QRadioButton("Emülatörü Başlat + Bot Çalıştır")
        self.launch_run_stop_option.toggled.connect(lambda: self.set_schedule_option("launch_run_stop"))
        second_row.addWidget(self.launch_run_stop_option)

        self.open_profile_option = QRadioButton("Kullanıcı Profilini Aç")
        self.open_profile_option.toggled.connect(lambda: self.set_schedule_option("open_profile"))
        second_row.addWidget(self.open_profile_option)

        self.enust_takip_option = QRadioButton("En Üstteki Takip Et")
        self.enust_takip_option.toggled.connect(lambda: self.set_schedule_option("enust_takip"))
        second_row.addWidget(self.enust_takip_option)

        options_layout.addLayout(second_row)
 
        # Wait time settings
        wait_layout = QHBoxLayout()
        wait_layout.addWidget(QLabel("Emülatör başlama bekleme süresi (sn):"))
        self.wait_time_input = QLineEdit("30")
        self.wait_time_input.setValidator(QIntValidator(10, 600))
        wait_layout.addWidget(self.wait_time_input)
        options_layout.addLayout(wait_layout)

        # Shutdown delay settings
        shutdown_layout = QHBoxLayout()
        shutdown_layout.addWidget(QLabel("Emülatör bitiş bekleme süresi (sn):"))
        self.shutdown_delay_input = QLineEdit("10")
        self.shutdown_delay_input.setValidator(QIntValidator(0, 600))
        shutdown_layout.addWidget(self.shutdown_delay_input)
        options_layout.addLayout(shutdown_layout)
 
        options_group.setLayout(options_layout)
        schedule_layout.addWidget(options_group)
        
        self.schedule_toggle = QCheckBox("Zamanlayıcıyı Etkinleştir")
        self.schedule_toggle.stateChanged.connect(self.toggle_scheduler)
        schedule_layout.addWidget(self.schedule_toggle)
        
        schedule_group.setLayout(schedule_layout)
        layout.addWidget(schedule_group)

        # Bot parameters
        params_group = QGroupBox("Bot Parametre Aralıkları")
        params_layout = QVBoxLayout()
        
        params = [
            ("Beğeni", "150", "200"),
            ("Yorum", "0", "0"),
            ("Kaydetme", "0", "0"),
            ("Takip", "8", "10"),
            ("Kaydırma", "90", "120"),
            ("Çalışma Süresi (sn)", "1200", "1600")
        ]
        
        self.inputs = {}
        for name, min_val, max_val in params:
            self.inputs[name] = self.create_param_row(name, min_val, max_val, params_layout)
        
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        # Control buttons
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Başlat")
        self.start_btn.clicked.connect(self.start_bot)
        btn_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Durdur")
        self.stop_btn.clicked.connect(self.stop_bot)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.stop_btn)
        
        # Add the enüst takip button
        self.enust_takip_btn = QPushButton("En Üstteki Takip Et")
        self.enust_takip_btn.clicked.connect(self.enust_takip)
        btn_layout.addWidget(self.enust_takip_btn)
        
        layout.addLayout(btn_layout)

        # Status
        self.status = QLabel("Durum: Hazır")
        layout.addWidget(self.status)

        self.setLayout(layout)

    def update_user_profile(self):
        self.user_profile = self.user_profile_input.text().strip()

    def enust_takip(self):
        try:
            os.environ["ANDROID_SERIAL"] = self.device_id
            fonksiyonlar.enüsttakipet()
            self.parent.log_message(f"✅ {self.device_id}: En üstteki takip et işlemi başarılı")
            self.status.setText("Durum: En üstteki takip et işlemi tamamlandı")
        except Exception as e:
            self.parent.log_message(f"❌ {self.device_id}: En üstteki takip et işlemi başarısız - {str(e)}")
            self.status.setText(f"Durum: Hata - {str(e)}")

    def open_profile(self):
        self.update_user_profile()
        if self.user_profile:
            try:
                # Call the function from fonksiyonlar module
                fonksiyonlar.kullanıcıprofili(self.user_profile)
                self.parent.log_message(f"📱 {self.device_id}: {self.user_profile} profilini açıyor")
                self.status.setText(f"Durum: {self.user_profile} profilini açıyor")
            except Exception as e:
                self.parent.log_message(f"❌ {self.device_id}: Profil açılamadı - {str(e)}")
        else:
            self.parent.log_message(f"❌ {self.device_id}: Kullanıcı adı girilmedi")

    def set_schedule_option(self, option):
        self.schedule_option = option
        self.parent.log_message(f"⚙️ {self.device_id} zamanlayıcı eylemi: {option}")

    def add_schedule_time(self):
        start = self.start_time.time().toString("HH:mm:ss")
        
        try:
            params = self.get_params()
            work_duration = random.randint(*params['sure'])
            start_dt = datetime.strptime(start, "%H:%M:%S")
            end_dt = start_dt + timedelta(seconds=work_duration)
            end = end_dt.strftime("%H:%M:%S")
            
            generated_values = {
                'begen': random.randint(*params['begen']),
                'yorum': random.randint(*params['yorum']),
                'kaydet': random.randint(*params['kaydet']),
                'takip': random.randint(*params['takip']),
                'kaydir': random.randint(*params['kaydir']),
                'sure': work_duration
            }
            
            self.schedule_table.add_time_range(start, end, self.schedule_option, generated_values)
            self.parent.log_message(f"⏰ {self.device_id} için zaman aralığı eklendi: {start}-{end} (Süre: {work_duration}s)")
            
            self.end_time.setTime(QTime.fromString(end, "HH:mm:ss"))
            
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Parametreler geçersiz: {str(e)}")

    def edit_schedule_time(self):
        current_row = self.schedule_table.currentRow()
        if current_row >= 0:
            start = self.start_time.time().toString("HH:mm:ss")
            
            try:
                params = self.get_params()
                work_duration = random.randint(*params['sure'])
                start_dt = datetime.strptime(start, "%H:%M:%S")
                end_dt = start_dt + timedelta(seconds=work_duration)
                end = end_dt.strftime("%H:%M:%S")
                
                generated_values = {
                    'begen': random.randint(*params['begen']),
                    'yorum': random.randint(*params['yorum']),
                    'kaydet': random.randint(*params['kaydet']),
                    'takip': random.randint(*params['takip']),
                    'kaydir': random.randint(*params['kaydir']),
                    'sure': work_duration
                }
                
                self.schedule_table.setItem(current_row, 0, QTableWidgetItem(start))
                self.schedule_table.setItem(current_row, 1, QTableWidgetItem(end))
                
                values_text = (f"Beğeni: {generated_values['begen']}, "
                             f"Yorum: {generated_values['yorum']}, "
                             f"Kaydet: {generated_values['kaydet']}, "
                             f"Takip: {generated_values['takip']}, "
                             f"Kaydır: {generated_values['kaydir']}, "
                             f"Süre: {generated_values['sure']}s")
                
                self.schedule_table.setItem(current_row, 3, QTableWidgetItem(values_text))
                self.parent.log_message(f"⏰ {self.device_id} için zaman aralığı güncellendi: {start}-{end} (Süre: {work_duration}s)")
                
                self.end_time.setTime(QTime.fromString(end, "HH:mm:ss"))
                
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Parametreler geçersiz: {str(e)}")

    def remove_schedule_time(self):
        current_row = self.schedule_table.currentRow()
        if current_row >= 0:
            start = self.schedule_table.item(current_row, 0).text()
            end = self.schedule_table.item(current_row, 1).text()
            self.schedule_table.removeRow(current_row)
            self.parent.log_message(f"⏰ {self.device_id} için zaman aralığı kaldırıldı: {start}-{end}")

    def launch_emulator(self):
        self.emulator_index = self.emulator_index_input.text().strip()
        if not self.emulator_index:
            QMessageBox.warning(self, "Hata", "Emülatör index numarası girin")
            return
            
        try:
            index_num = int(self.emulator_index)
            if index_num < 0:
                raise ValueError("Index negatif olamaz")
                
            ldconsole_path = self.parent.ldplayer_path_input.text().strip()
            if not ldconsole_path:
                QMessageBox.warning(self, "Hata", "LDPlayer yolu ayarlanmamış")
                return
                
            subprocess.run([ldconsole_path, "launch", "--index", self.emulator_index])
            self.parent.log_message(f"🚀 {self.device_id}: Emülatör başlatıldı (Index: {self.emulator_index})")
        except Exception as e:
            self.parent.log_message(f"❌ {self.device_id}: Emülatör başlatılamadı - {str(e)}")

    def quit_emulator(self):
        self.emulator_index = self.emulator_index_input.text().strip()
        if not self.emulator_index:
            QMessageBox.warning(self, "Hata", "Emülatör index numarası girin")
            return
            
        try:
            index_num = int(self.emulator_index)
            if index_num < 0:
                raise ValueError("Index negatif olamaz")
                
            ldconsole_path = self.parent.ldplayer_path_input.text().strip()
            if not ldconsole_path:
                QMessageBox.warning(self, "Hata", "LDPlayer yolu ayarlanmamış")
                return
                
            subprocess.run([ldconsole_path, "quit", "--index", self.emulator_index])
            self.parent.log_message(f"🛑 {self.device_id}: Emülatör durduruldu (Index: {self.emulator_index})")
        except Exception as e:
            self.parent.log_message(f"❌ {self.device_id}: Emülatör durdurulamadı - {str(e)}")

    def stop_emulator(self):
        try:
            self.shutdown_delay = int(self.shutdown_delay_input.text())
            if self.shutdown_delay > 0:
                self.parent.log_message(f"⏳ {self.device_id}: Emülatör {self.shutdown_delay}s sonra kapatılacak...")
                QTimer.singleShot(self.shutdown_delay * 1000, self._stop_emulator_after_delay)
            else:
                self._stop_emulator_after_delay()
        except Exception as e:
            self.parent.log_message(f"❌ {self.device_id}: Emülatör kapatma gecikmesi ayarlanamadı - {str(e)}")
            self._stop_emulator_after_delay()

    def _stop_emulator_after_delay(self):
        try:
            ldconsole_path = self.parent.ldplayer_path_input.text().strip()
            if not ldconsole_path:
                self.parent.log_message(f"❌ {self.device_id}: LDPlayer yolu tanımlı değil")
                return
            subprocess.run([ldconsole_path, "quit", "--index", self.emulator_index])
            self.parent.log_message(f"🛑 {self.device_id}: Emülatör kapatıldı (Index: {self.emulator_index})")
        except Exception as e:
            self.parent.log_message(f"❌ {self.device_id}: Emülatör kapatılamadı - {str(e)}")

    def toggle_scheduler(self, state):
        self.scheduler_enabled = state == Qt.CheckState.Checked.value
        if self.scheduler_enabled:
            self.parent.log_message(f"⏰ {self.device_id} için zamanlayıcı aktif")
        else:
            self.parent.log_message(f"⏰ {self.device_id} için zamanlayıcı pasif")

    def create_param_row(self, name, min_val, max_val, layout):
        row = QHBoxLayout()
        row.addWidget(QLabel(name))
        
        min_input = QLineEdit(min_val)
        min_input.setValidator(QIntValidator(0, 9999))
        row.addWidget(QLabel("Min:"))
        row.addWidget(min_input)
        
        max_input = QLineEdit(max_val)
        max_input.setValidator(QIntValidator(0, 9999))
        row.addWidget(QLabel("Max:"))
        row.addWidget(max_input)
        
        layout.addLayout(row)
        return (min_input, max_input)

    def get_params(self):
        params = {}
        try:
            params['begen'] = (int(self.inputs['Beğeni'][0].text()), int(self.inputs['Beğeni'][1].text()))
            params['yorum'] = (int(self.inputs['Yorum'][0].text()), int(self.inputs['Yorum'][1].text()))
            params['kaydet'] = (int(self.inputs['Kaydetme'][0].text()), int(self.inputs['Kaydetme'][1].text()))
            params['takip'] = (int(self.inputs['Takip'][0].text()), int(self.inputs['Takip'][1].text()))
            params['kaydir'] = (int(self.inputs['Kaydırma'][0].text()), int(self.inputs['Kaydırma'][1].text()))
            params['sure'] = (int(self.inputs['Çalışma Süresi (sn)'][0].text()), int(self.inputs['Çalışma Süresi (sn)'][1].text()))
            
            for name, (min_val, max_val) in params.items():
                if min_val > max_val:
                    raise ValueError(f"{name} için min değer max'tan büyük olamaz")
                    
            return params
            
        except ValueError as e:
            raise ValueError(f"Geçersiz değer: {str(e)}")

    def get_current_schedule_params(self):
        now = datetime.now().time()
        current_time = now.hour * 3600 + now.minute * 60 + now.second
        
        for schedule in self.schedule_table.get_schedules():
            start = QTime.fromString(schedule["start"], "HH:mm:ss")
            end = QTime.fromString(schedule["end"], "HH:mm:ss")
            
            start_sec = start.hour() * 3600 + start.minute() * 60 + start.second()
            end_sec = end.hour() * 3600 + end.minute() * 60 + end.second()
            
            if start_sec <= end_sec:
                if start_sec <= current_time <= end_sec:
                    return schedule["values"]
            else:
                if current_time >= start_sec or current_time <= end_sec:
                    return schedule["values"]
        
        return None

    def get_schedule(self):
        return {
            'enabled': self.scheduler_enabled,
            'time_ranges': self.schedule_table.get_schedules(),
            'option': self.schedule_option,
            'wait_time': self.wait_time,
            'shutdown_delay': self.shutdown_delay,
            'emulator_index': self.emulator_index_input.text(),
            'work_duration': {
                'min': self.inputs['Çalışma Süresi (sn)'][0].text(),
                'max': self.inputs['Çalışma Süresi (sn)'][1].text()
            },
            'user_profile': self.user_profile
        }

    def set_schedule(self, schedule):
        if schedule:
            self.schedule_toggle.setChecked(schedule.get('enabled', False))
            self.schedule_table.set_schedules(schedule.get('time_ranges', []))
            option = schedule.get('option', 'run_only')
            if option == 'launch_and_run':
                self.launch_and_run_option.setChecked(True)
            elif option == 'launch_run_stop':
                self.launch_run_stop_option.setChecked(True)
            elif option == 'open_profile':
                self.open_profile_option.setChecked(True)
            elif option == 'enust_takip':
                self.enust_takip_option.setChecked(True)
            else:
                self.run_only_option.setChecked(True)
            self.wait_time_input.setText(str(schedule.get('wait_time', 30)))
            self.shutdown_delay_input.setText(str(schedule.get('shutdown_delay', 10)))
            
            emulator_index = str(schedule.get('emulator_index', '0'))
            self.emulator_index_input.setText(emulator_index)
            self.emulator_index = emulator_index
            
            work_duration = schedule.get('work_duration', {})
            if work_duration:
                self.inputs['Çalışma Süresi (sn)'][0].setText(str(work_duration.get('min', '1200')))
                self.inputs['Çalışma Süresi (sn)'][1].setText(str(work_duration.get('max', '1600')))
            
            user_profile = schedule.get('user_profile', '')
            self.user_profile_input.setText(user_profile)
            self.user_profile = user_profile

    def check_schedule(self):
        if not self.scheduler_enabled:
            return False
            
        now = datetime.now().time()
        current_time = now.hour * 3600 + now.minute * 60 + now.second
        
        for schedule in self.schedule_table.get_schedules():
            start = QTime.fromString(schedule["start"], "HH:mm:ss")
            end = QTime.fromString(schedule["end"], "HH:mm:ss")
            
            start_sec = start.hour() * 3600 + start.minute() * 60 + start.second()
            end_sec = end.hour() * 3600 + end.minute() * 60 + end.second()
            
            if start_sec <= end_sec:
                if start_sec <= current_time <= end_sec:
                    return schedule
            else:
                if current_time >= start_sec or current_time <= end_sec:
                    return schedule
        return None

    def start_bot(self):
        try:
            self.wait_time = int(self.wait_time_input.text())
            self.shutdown_delay = int(self.shutdown_delay_input.text())
            self.emulator_index = self.emulator_index_input.text().strip()
            self.update_user_profile()
        
            schedule = self.check_schedule()
            if schedule and self.scheduler_enabled:
                self.parent.log_message(f"⏰ {self.device_id}: Zamanlayıcı değerleri kullanılıyor")
                params = {
                    'begen': (schedule['values']['begen'], schedule['values']['begen']),
                    'yorum': (schedule['values']['yorum'], schedule['values']['yorum']),
                    'kaydet': (schedule['values']['kaydet'], schedule['values']['kaydet']),
                    'takip': (schedule['values']['takip'], schedule['values']['takip']),
                    'kaydir': (schedule['values']['kaydir'], schedule['values']['kaydir']),
                    'sure': (schedule['values']['sure'], schedule['values']['sure'])
                }
                action = schedule['action']
            else:
                params = self.get_params()
                action = self.schedule_option
            
            if action == "launch_only":
                self.launch_emulator()
                self.status.setText("Durum: Emülatör başlatıldı")
            elif action == "quit_only":
                self.quit_emulator()
                self.status.setText("Durum: Emülatör kapatıldı")
            elif action == "launch_and_run":
                self.launch_emulator()
                QTimer.singleShot(self.wait_time * 1000, lambda: self.run_bot_with_params(params))
                self.status.setText(f"Durum: Emülatör başlatılıyor ({self.wait_time}s bekleniyor)...")
            elif action == "launch_run_stop":
                self.launch_emulator()
                QTimer.singleShot(self.wait_time * 1000, lambda: self.run_bot_with_params(params, stop_after=True))
                self.status.setText(f"Durum: Emülatör başlatılıyor ({self.wait_time}s bekleniyor)...")
            elif action == "open_profile":
                self.open_profile()
            elif action == "enust_takip":
                self.enust_takip()
            else:  # run_only
                self.run_bot_with_params(params)
    
        except Exception as e:
            QMessageBox.warning(self, "Hata", str(e))

    def run_bot_after_launch(self, params):
        self.parent.log_message(f"⏳ {self.device_id}: {self.wait_time}s bekleme tamamlandı, bot başlatılıyor...")
        self.run_bot_with_params(params)

    def run_bot_with_params(self, params, stop_after=False):
        try:
            if self.thread and self.thread.isRunning():
                self.thread.stop()
                self.thread.wait()
                
            self.thread = BotThread(self.device_id, self.kontrol, params)
            self.thread.log.connect(self.parent.log_message)
            self.thread.finished.connect(self.bot_finished)
            
            if stop_after:
                self.thread.actually_finished.connect(lambda: QTimer.singleShot(
                    self.shutdown_delay * 1000, 
                    self.stop_emulator
                ))
            else:
                self.thread.actually_finished.connect(self.bot_completed_successfully)
            
            self.kontrol.durdur = False
            self.thread.start()
            
            self.start_btn.setEnabled(False)
            self.stop_btn.setEnabled(True)
            self.status.setText("Durum: Çalışıyor...")
            
        except Exception as e:
            QMessageBox.warning(self, "Hata", str(e))

    def stop_bot(self):
        if self.thread and self.thread.isRunning():
            self.kontrol.durdur = True
            self.status.setText("Durum: Durduruluyor...")
            self.stop_btn.setEnabled(False)
            self.thread.stop()
            self.thread.wait()

    def bot_finished(self, device_id):
        if self.thread:
            self.thread.quit()
            self.thread.wait()
            self.thread = None
            
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status.setText("Durum: Hazır")

    def bot_completed_successfully(self, device_id):
        self.parent.log_message(f"✅ {device_id}: İşlem başarıyla tamamlandı")

    def remove_device(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Onay")
        msg_box.setText("Bu cihazı kaldırmak istediğinize emin misiniz?")
        msg_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QMessageBox.StandardButton.No)
        
        if msg_box.exec() == QMessageBox.StandardButton.Yes:
            self.stop_bot()
            if self.thread:
                self.thread.quit()
                self.thread.wait()
            self.parent.remove_device_tab(self.device_id)

class Arayuz(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Instagram Bot Kontrol Paneli")
        self.setGeometry(300, 300, 900, 700)
        self.device_tabs = {}
        self.scheduler_timer = QTimer(self)
        self.scheduler_timer.timeout.connect(self.check_schedules)
        self.last_triggered_schedule = {}
        
        self.init_ui()
        self.load_settings()
        self.scheduler_timer.start(60000)

    def init_ui(self):
        layout = QVBoxLayout()

        # Device management
        device_layout = QHBoxLayout()
        
        self.emulator_combo = QComboBox()
        self.emulator_combo.setPlaceholderText("Açık emülatörler")
        device_layout.addWidget(self.emulator_combo)
        
        refresh_btn = QPushButton("Yenile")
        refresh_btn.clicked.connect(self.refresh_emulators)
        device_layout.addWidget(refresh_btn)
        
        self.device_input = QLineEdit("emulator-5556")
        self.device_input.setPlaceholderText("Emülatör ID (örn: emulator-5554)")
        device_layout.addWidget(self.device_input)
        
        add_btn = QPushButton("Cihaz Ekle")
        add_btn.clicked.connect(self.add_device)
        device_layout.addWidget(add_btn)
        
        global_btn = QPushButton("Tüm Zamanlayıcıları Aç")
        global_btn.clicked.connect(self.toggle_all_schedulers)
        device_layout.addWidget(global_btn)
        
        layout.addLayout(device_layout)

        # LDPlayer path configuration
        ldplayer_layout = QHBoxLayout()
        ldplayer_layout.addWidget(QLabel("LDPlayer Path:"))
        self.ldplayer_path_input = QLineEdit("C:\\LDPlayer\\LDPlayer9\\ldconsole.exe")
        ldplayer_layout.addWidget(self.ldplayer_path_input)
        
        browse_btn = QPushButton("Gözat")
        browse_btn.clicked.connect(self.browse_ldplayer_path)
        ldplayer_layout.addWidget(browse_btn)
        
        test_btn = QPushButton("Test Et")
        test_btn.clicked.connect(self.test_ldplayer_path)
        ldplayer_layout.addWidget(test_btn)
        
        layout.addLayout(ldplayer_layout)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        layout.addWidget(self.tabs)

        # Global controls
        control_layout = QHBoxLayout()
        start_all_btn = QPushButton("Tümünü Başlat")
        start_all_btn.clicked.connect(self.start_all_bots)
        control_layout.addWidget(start_all_btn)
        
        stop_all_btn = QPushButton("Tümünü Durdur")
        stop_all_btn.clicked.connect(self.stop_all_bots)
        control_layout.addWidget(stop_all_btn)
        
        save_btn = QPushButton("Ayarları Kaydet")
        save_btn.clicked.connect(self.save_settings)
        control_layout.addWidget(save_btn)
        
        layout.addLayout(control_layout)

        # Log area
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        self.setLayout(layout)
        self.refresh_emulators()

    def refresh_emulators(self):
        try:
            self.emulator_combo.clear()
            
            try:
                result = subprocess.run(["adb", "devices"], capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    devices = []
                    for line in result.stdout.splitlines()[1:]:
                        if line.strip() and "offline" not in line:
                            device_id = line.split("\t")[0]
                            if device_id not in self.device_tabs:
                                devices.append(device_id)
                    
                    if devices:
                        self.emulator_combo.addItems(devices)
                        self.emulator_combo.insertSeparator(len(devices))
            
            except Exception as e:
                self.log_message(f"❌ ADB cihazları algılanamadı: {str(e)}")
            
            ldconsole_path = self.ldplayer_path_input.text().strip()
            if ldconsole_path and os.path.exists(ldconsole_path):
                try:
                    result = subprocess.run([ldconsole_path, "list"], capture_output=True, text=True, shell=True)
                    if result.returncode == 0:
                        lines = result.stdout.splitlines()
                        for line in lines:
                            if line.strip():
                                parts = line.split(",")
                                if len(parts) >= 2:
                                    index = parts[0].strip()
                                    name = parts[1].strip()
                                    self.emulator_combo.addItem(f"{name} (Index: {index})", index)
                except Exception as e:
                    self.log_message(f"❌ LDPlayer listesi alınamadı: {str(e)}")
            
            if self.emulator_combo.count() == 0:
                self.emulator_combo.addItem("Açık emülatör bulunamadı")
            
            self.emulator_combo.setCurrentIndex(0)
            
        except Exception as e:
            self.log_message(f"❌ Emülatörler yenilenirken hata: {str(e)}")

    def browse_ldplayer_path(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "LDConsole.exe dosyasını seçin", 
            "C:\\", 
            "Executable Files (*.exe)"
        )
        if file_path:
            self.ldplayer_path_input.setText(file_path)
            self.refresh_emulators()

    def test_ldplayer_path(self):
        path = self.ldplayer_path_input.text().strip()
        if not path:
            QMessageBox.warning(self, "Hata", "LDPlayer yolu girin")
            return
            
        if not os.path.exists(path):
            QMessageBox.warning(self, "Hata", "Belirtilen yol geçerli değil!")
            return
            
        try:
            result = subprocess.run([path, "list"], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                QMessageBox.information(self, "Başarılı", "LDPlayer başarıyla bulundu!\nKullanılabilir emülatörler:\n" + result.stdout)
                self.refresh_emulators()
            else:
                QMessageBox.warning(self, "Hata", f"LDPlayer bulunamadı veya hata oluştu:\n{result.stderr}")
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"LDPlayer test edilemedi:\n{str(e)}")

    def toggle_all_schedulers(self):
        enabled = not all(tab.scheduler_enabled for tab in self.device_tabs.values())
        for tab in self.device_tabs.values():
            tab.schedule_toggle.setChecked(enabled)
        
        self.log_message(f"⏰ Tüm zamanlayıcılar {'açıldı' if enabled else 'kapatıldı'}")

    def check_schedules(self):
        for device_id, tab in self.device_tabs.items():
            current_schedule = tab.check_schedule()
            last = self.last_triggered_schedule.get(device_id)
            if current_schedule:
                if last == current_schedule:
                    continue
                if not (tab.thread and tab.thread.isRunning()):
                    tab.start_bot()
                    self.last_triggered_schedule[device_id] = current_schedule
            else:
                self.last_triggered_schedule[device_id] = None

    def log_message(self, message):
        self.log_area.append(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def add_device(self, device_id=None):
        if not device_id:
            if self.emulator_combo.currentIndex() >= 0 and not self.emulator_combo.currentText().startswith("Açık emülatör bulunamadı"):
                if self.emulator_combo.currentData():
                    index = self.emulator_combo.currentData()
                    ldconsole_path = self.ldplayer_path_input.text().strip()
                    if ldconsole_path and os.path.exists(ldconsole_path):
                        try:
                            subprocess.run([ldconsole_path, "launch", "--index", str(index)], shell=True)
                            self.log_message(f"🚀 LDPlayer başlatılıyor (Index: {index})")
                            QTimer.singleShot(10000, lambda: self._add_device_after_launch(index))
                            return
                        except Exception as e:
                            self.log_message(f"❌ LDPlayer başlatılamadı: {str(e)}")
                else:
                    device_id = self.emulator_combo.currentText().split()[0]
            else:
                device_id = self.device_input.text().strip()
                if not device_id:
                    QMessageBox.warning(self, "Hata", "Cihaz ID girin")
                    return
                
        if device_id in self.device_tabs:
            QMessageBox.warning(self, "Uyarı", "Bu cihaz zaten ekli")
            return
            
        tab = DeviceTab(device_id, self)
        scroll = QScrollArea()
        scroll.setWidget(tab)
        scroll.setWidgetResizable(True)
        
        self.tabs.addTab(scroll, device_id)
        self.device_tabs[device_id] = tab
        self.device_input.clear()
        self.log_message(f"✅ {device_id} eklendi")

    def _add_device_after_launch(self, index):
        try:
            ldconsole_path = self.ldplayer_path_input.text().strip()
            result = subprocess.run([ldconsole_path, "adb", "--index", str(index), "--command", "devices"], 
                                  capture_output=True, text=True, shell=True)
            
            if result.returncode == 0:
                for line in result.stdout.splitlines()[1:]:
                    if line.strip() and "offline" not in line:
                        device_id = line.split("\t")[0]
                        if device_id not in self.device_tabs:
                            self.add_device(device_id)
                            self.device_tabs[device_id].emulator_index_input.setText(str(index))
                            return
                
                self.log_message(f"❌ Başlatılan emülatörün ({index}) cihaz ID'si alınamadı")
            else:
                self.log_message(f"❌ Emülatör cihaz ID'si alınamadı: {result.stderr}")
        except Exception as e:
            self.log_message(f"❌ Emülatör eklenirken hata: {str(e)}")

    def close_tab(self, index):
        device_id = self.tabs.tabText(index)
        self.remove_device_tab(device_id)

    def remove_device_tab(self, device_id):
        if device_id in self.device_tabs:
            tab = self.device_tabs[device_id]
            tab.stop_bot()
            
            for i in range(self.tabs.count()):
                if self.tabs.tabText(i) == device_id:
                    self.tabs.removeTab(i)
                    break
                    
            del self.device_tabs[device_id]
            self.log_message(f"❌ {device_id} kaldırıldı")

    def start_all_bots(self):
        if any(tab.thread and tab.thread.isRunning() for tab in self.device_tabs.values()):
            return
            
        self.log_message("⏳ Tüm botlar başlatılıyor...")
        for device_id, tab in self.device_tabs.items():
            tab.start_bot()

    def stop_all_bots(self):
        self.log_message("⏹️ Tüm botlar durduruluyor...")
        for device_id, tab in self.device_tabs.items():
            tab.stop_bot()

    def save_settings(self):
        settings = {
            "devices": [],
            "params": {},
            "schedules": {},
            "ldplayer_path": self.ldplayer_path_input.text()
        }

        for device_id, tab in self.device_tabs.items():
            settings["devices"].append(device_id)
            try:
                settings["params"][device_id] = tab.get_params()
                settings["schedules"][device_id] = tab.get_schedule()
            except Exception as e:
                self.log_message(f"❌ {device_id} ayarları kaydedilirken hata: {str(e)}")

        try:
            with open("bot_ayarlar.json", "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
            self.log_message("💾 Ayarlar kaydedildi")
        except Exception as e:
            self.log_message(f"❌ Ayarlar kaydedilemedi: {str(e)}")

    def load_settings(self):
        try:
            if os.path.exists("bot_ayarlar.json"):
                with open("bot_ayarlar.json", "r", encoding="utf-8") as f:
                    settings = json.load(f)

                self.ldplayer_path_input.setText(settings.get("ldplayer_path", "C:\\LDPlayer\\LDPlayer9\\ldconsole.exe"))

                for device_id in settings.get("devices", []):
                    self.add_device(device_id)
                    tab = self.device_tabs.get(device_id)
                    if tab:
                        params = settings["params"].get(device_id, {})
                        for name in tab.inputs:
                            if name in params:
                                tab.inputs[name][0].setText(str(params[name][0]))
                                tab.inputs[name][1].setText(str(params[name][1]))
                        
                        schedule = settings["schedules"].get(device_id, {})
                        tab.set_schedule(schedule)
                
                self.log_message("🔃 Ayarlar yüklendi")
                
        except Exception as e:
            self.log_message(f"❌ Ayarlar yüklenemedi: {str(e)}")

    def closeEvent(self, event):
        self.stop_all_bots()
        for device_id, tab in self.device_tabs.items():
            if tab.thread:
                tab.thread.stop()
                tab.thread.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet("""
        QComboBox, QTableWidget, QTableWidget QTableCornerButton::section,
        QHeaderView::section, QLineEdit, QGroupBox, QTimeEdit {
            background-color: white;
            color: black;
            selection-background-color: #d0d0d0;
            selection-color: black;
        }
        QComboBox QAbstractItemView {
            background-color: white;
            color: black;
            selection-background-color: #d0d0d0;
            selection-color: black;
        }
        QTableWidget::item:selected {
            background-color: #d0d0d0;
            color: black;
        }
        QPushButton {
            background-color: #f0f0f0;
            color: black;
        }
    """)
    window = Arayuz()
    window.show()
    sys.exit(app.exec())