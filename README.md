# Baekjoon-Timer
PyQt5 + Selenium 기반 문제풀이 사이트인 백준에서 작동하는 타이머 입니다! 문제풀이 및 실시간 정답/오답/시간초과 감지합니다

---

## 🔧 기능 요약

- 초 단위 실시간 타이머
- `맞았습니다!!` 감지 시 자동 타이머 정지
- `틀렸습니다 / 시간 초과` 감지 시 상태 출력
- 문제 번호 및 이름도 표시
- 투명한 디자인 + 그림자 효과 적용
- 화면 어디서든 마우스로 드래그 이동 가능

## ⚠️ 주의사항

!!! 백준 계정에 로그인된 상태에서 실행하세요. !!!
!!! Chromedriver.exe 와 같은 위치에 존재해야됩니다 !!!
!!! 크롬 자동화 탐지를 피하기 위해 최소한의 우회 옵션 적용 중 (enable-automation 제거). !!!

---

# English

A PyQt5 + Selenium-based timer tool that works with the Baekjoon Online Judge platform.  
It tracks your problem-solving time and detects real-time results such as correct, wrong, and time limit exceeded.

---

## 🔧 Features

- Real-time second-by-second timer
- Automatically pauses when `"맞았습니다!!"` (`"Accepted!"`) is detected
- Displays result messages when `"틀렸습니다"` (`"Wrong Answer"`) or `"시간 초과"` (`"Time Limit Exceeded"`) is detected
- Shows the problem number and title
- Transparent UI with drop shadow effects for a clean look
- Can be dragged around the screen by clicking anywhere

---

## ⚠️ Important Notes

- **You must be logged into your Baekjoon account before running the timer.**
- **`chromedriver.exe` must be located in the same directory as this script.**
- **Minimal evasion techniques are applied to bypass Chrome’s automation detection (e.g., `enable-automation` flag removed).**

---
