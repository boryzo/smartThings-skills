---
name: smartthings
# Skill do obsługi urządzeń Samsung SmartThings
# Obsługuje: piekarniki, mikrofale, pralki, suszarki
# Komendy: włącz/wyłącz, status, uruchom program, zatrzymaj
# Wymaga: Personal Access Token (PAT) SmartThings
---

# SmartThings

Skill do sterowania urządzeniami Samsung SmartThings (piekarnik, mikrofala, pralka, suszarka) przez lokalny CLI.

## Ścieżka do skryptu
- Script: `{baseDir}/scripts/smartthings.py`

## Obsługiwane akcje
- Włącz urządzenie: `python3 {baseDir}/scripts/smartthings.py on <device>`
- Wyłącz urządzenie: `python3 {baseDir}/scripts/smartthings.py off <device>`
- Status urządzenia: `python3 {baseDir}/scripts/smartthings.py status <device>`
- Uruchom program: `python3 {baseDir}/scripts/smartthings.py start <device> <program>`
- Zatrzymaj program: `python3 {baseDir}/scripts/smartthings.py stop <device>`

## Zachowanie
- Jeśli nie podano urządzenia, wylistuj dostępne urządzenia.
- Jeśli nie podano tokena, poproś o wygenerowanie PAT na https://account.smartthings.com/tokens
- Obsługiwane typy urządzeń: piekarnik, mikrofala, pralka, suszarka.
