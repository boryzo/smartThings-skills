---
name: smartthings
# Skill do obsługi urządzeń Samsung SmartThings
# Obsługuje: piekarniki, mikrofale, pralki, suszarki
# Komendy: włącz/wyłącz, status, uruchom program, zatrzymaj
# Wymaga: Personal Access Token (PAT) SmartThings
---

# SmartThings

Skill do sterowania urządzeniami Samsung SmartThings (piekarnik, mikrofala, pralka, suszarka) przez lokalny CLI.


# Skill: SmartThings

CLI for controlling Samsung SmartThings appliances (washers, dryers, ovens, microwaves, cooktops).

## Configuration

1. Generate a Personal Access Token (PAT) at https://account.smartthings.com/tokens
2. Copy the token to the file `~/.smartthings.json`:

```
{
	"token": "YOUR_TOKEN_HERE"
}
```

## Usage

```bash
python3 skills/smartthings/scripts/smartthings.py [command] [device_name]
```

### Commands:

- `list` — list devices
- `status <device>` — show device status
- `start <device>` — start a program
- `stop <device>` — stop a program
- `on|off <device>` — turn on/off (if supported)
- `config` — configure token

### Examples:

```bash
python3 skills/smartthings/scripts/smartthings.py list
python3 skills/smartthings/scripts/smartthings.py status Washer
python3 skills/smartthings/scripts/smartthings.py start Oven
```

## Supported devices and states

- Washer: state, program, time, temperature, spin
- Dryer: state, program, time, dryness level
- Oven: state, mode, temperature, time, door
- Microwave: state, mode, time, power
- Cooktop: state, power level, timer

## Requirements

- Python 3
- requests

## Author

Borys Wisniewski
