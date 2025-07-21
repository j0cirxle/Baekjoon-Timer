import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont, QFontDatabase, QColor
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class TimerThread(QThread):
    time_changed = pyqtSignal(int,str)

    def __init__(self):
        super().__init__()
        self.running = True
        self.paused = True  # 처음부터 멈춤 상태
        self.seconds = 0

    def run(self):
        while self.running:
            self.msleep(200)
            if not self.paused:
                self.sleep(1)
                self.seconds += 1
                
                self.time_changed.emit(self.seconds,"red")
            else:
                self.time_changed.emit(self.seconds,"green")

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

    def pause(self):
        self.paused = True
        self.time_changed.emit(self.seconds,"green")

    def resume(self):
        self.paused = False

    def reset(self):
        self.seconds = 0
        self.paused = True


class SeleniumThread(QThread):
    finished_signal = pyqtSignal(str,str)

    def __init__(self,timer_thread):
        super().__init__()
        self.driver = None
        self.checking_n = True
        self.cnt = 0
        self.timer_thread = timer_thread
    def run(self):
        try:
            chrome_options = Options()
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.get("https://www.acmicpc.net/")
            title = "Baekjoon Online Judge Timer"
            self.check()
            self.finished_signal.emit(f"{title}", "white")

        except Exception as e:
            print("Selenium 에러:", e)
            self.finished_signal.emit(f"Selenium 에러: {str(e)}", "red")

        
    def check(self):
        while True:
            try:
                problems = self.driver.find_elements(By.CSS_SELECTOR, 'td:nth-child(3) > a')
                elements = self.driver.find_elements(By.CSS_SELECTOR, "span.result-text.result-ac")
                elements_wa = self.driver.find_elements(By.CSS_SELECTOR, "span.result-text.result-wa")
                elements_tle = self.driver.find_elements(By.CSS_SELECTOR, "span.result-text.result-tle")

                number = ""
                name = ""

                for el in elements:
                    print(el.text)
                    if "맞았습니다!!" in el.text or "100점" in el.text:
                        self.timer_thread.pause()
                        try:
                            for prob in problems:
                                number = prob.text.strip()
                                name = prob.get_attribute("data-original-title").strip()
                                print(f"{number} - {name}")
                        except Exception as e:
                            print("문제 정보 접근 중 오류:", e)
                            number = ""
                            name = ""
                        self.finished_signal.emit(f"{name} - {number} Your Correct!!","green")
                        self.sleep(10)

                for el in elements_wa:
                    if "틀렸습니다" in el.text:
                        try:
                            for prob in problems:
                                number = prob.text.strip()
                                name = prob.get_attribute("data-original-title").strip()
                                print(f"{number} - {name}")
                        except Exception as e:
                            print("문제 정보 접근 중 오류:", e)
                            number = ""
                            name = ""
                        self.finished_signal.emit(f"{name} - {number} . incorrect or unsolved .","red")
                        self.sleep(1)

                for el in elements_tle:
                    if "시간 초과" in el.text:
                        try:
                            for prob in problems:
                                number = prob.text.strip()
                                name = prob.get_attribute("data-original-title").strip()
                                print(f"{number} - {name}")
                        except Exception as e:
                            print("문제 정보 접근 중 오류:", e)
                            number = ""
                            name = ""
                        self.finished_signal.emit(f"{name} - {number} . time_over .","red")
                        self.sleep(1)

            except Exception as e:
                print("check 함수 오류 발생, 재시도 중:", e)
                self.sleep(1)
                continue

            self.sleep(1)



class DigitalTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.offset = None
        self.initUI()

        self.timer_thread = TimerThread()
        self.timer_thread.time_changed.connect(self.update_time)
        self.timer_thread.start()

        self.selenium_thread = SeleniumThread(self.timer_thread)
        self.selenium_thread.finished_signal.connect(self.on_selenium_finished)
        self.selenium_thread.start()

    def initUI(self):
        self.setWindowFlags(
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(600, 200)

        font_path = "Orbitron-Regular.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            family = QFontDatabase.applicationFontFamilies(font_id)[0]
            font = QFont(family, 60)
        else:
            font = QFont("Arial", 60)

        self.label = QLabel("00:00", self)
        self.label.setFont(font)
        self.label.setStyleSheet("color: white; background-color: transparent;")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setGeometry(0, 0, 600, 120)

        # 그림자 효과 추가
        # 타이머 텍스트용 그림자
        label_shadow = QGraphicsDropShadowEffect(self)
        label_shadow.setBlurRadius(15)
        label_shadow.setColor(QColor(0, 0, 0, 180))
        label_shadow.setOffset(3, 3)
        self.label.setGraphicsEffect(label_shadow)


        self.status_label = QLabel("", self)
        self.status_label.setStyleSheet(
            "color: white; font-size: 12px; background-color: rgba(0,0,0,120); border-radius:5px;"
        )
        
                # 상태 텍스트용 그림자
        status_shadow = QGraphicsDropShadowEffect(self)
        status_shadow.setBlurRadius(10)
        status_shadow.setColor(QColor(0, 0, 0, 160))
        status_shadow.setOffset(2, 2)
        self.status_label.setGraphicsEffect(status_shadow)
        
        self.status_label.setGeometry(10, 120, 580, 25)
        self.status_label.setAlignment(Qt.AlignCenter)

        self.btn_start = QPushButton("시작", self)
        self.btn_start.setGeometry(70, 150, 100, 35)
        self.btn_start.clicked.connect(self.start_timer)

        self.btn_pause = QPushButton("멈춤", self)
        self.btn_pause.setGeometry(230, 150, 100, 35)
        self.btn_pause.clicked.connect(self.pause_timer)

        self.btn_reset = QPushButton("초기화", self)
        self.btn_reset.setGeometry(390, 150, 100, 35)
        self.btn_reset.clicked.connect(self.reset_timer)

    def start_timer(self):
        self.timer_thread.resume()

    def pause_timer(self):
        self.timer_thread.pause()

    def reset_timer(self):
        self.timer_thread.reset()

    def update_time(self, seconds,color):
        m = seconds // 60
        s = seconds % 60
        self.label.setText(f"{m:02}:{s:02}")

        self.label.setStyleSheet(
            f"color: {color};"
        )

    def on_selenium_finished(self, msg,color):
        self.status_label.setText(msg)
        self.status_label.setStyleSheet(
            f"color: {color}; font-size: 12px; background-color: rgba(0,0,0,120); border-radius:5px;"
        )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset is not None:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        self.offset = None

    def closeEvent(self, event):
        self.timer_thread.stop()
        self.selenium_thread.stop_driver()
        self.selenium_thread.quit()
        self.selenium_thread.wait()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DigitalTimer()
    window.show()
    sys.exit(app.exec_())
