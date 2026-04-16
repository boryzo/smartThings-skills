#!/usr/bin/env python3
"""
CLI do obsługi urządzeń Samsung SmartThings: piekarnik, mikrofala, pralka, suszarka
Wymaga Personal Access Token (PAT) z https://account.smartthings.com/tokens
"""
import argparse
import os
import sys
import requests
import json

CONFIG_FILE = os.path.expanduser("~/.smartthings.json")
API_URL = "https://api.smartthings.com/v1"

# --- Helpers ---
def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print("Brak konfiguracji. Uruchom: python3 smartthings.py config")
        sys.exit(1)
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def get_headers(token):
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

def list_devices(token):
    url = f"{API_URL}/devices"
    resp = requests.get(url, headers=get_headers(token))
    if resp.status_code != 200:
        print(f"Błąd API: {resp.status_code} {resp.text}")
        sys.exit(1)
    devices = resp.json().get("items", [])
    for d in devices:
        print(f"{d['deviceId']} | {d['label']} | {d['deviceTypeName']} | {d['manufacturerName']}")
    return devices

def device_by_name(token, name):
    devices = list_devices(token)
    for d in devices:
        if name.lower() in d['label'].lower():
            return d
    print(f"Nie znaleziono urządzenia: {name}")
    sys.exit(1)

def send_command(token, device_id, capability, command, args=None):
    url = f"{API_URL}/devices/{device_id}/commands"
    cmd = {
        "commands": [
            {
                "component": "main",
                "capability": capability,
                "command": command,
                "arguments": args or []
            }
        ]
    }
    resp = requests.post(url, headers=get_headers(token), json=cmd)
    if resp.status_code not in (200, 202):
        print(f"Błąd wysyłania komendy: {resp.status_code} {resp.text}")
        sys.exit(1)
    print("Komenda wysłana.")

def print_appliance_status(device_type, status):
    """
    Wyciąga i prezentuje czytelnie status urządzenia AGD.
    """
    if device_type == "Washer":
        cycle = status.get('washerOperatingState', {}).get('machineState', {}).get('value')
        progress = status.get('custom.washerJobState', {}).get('jobState', {}).get('value')
        remaining = status.get('washerOperatingState', {}).get('completionTime', {}).get('value')
        print(f"Stan pralki: {cycle or progress}")
        if remaining:
            print(f"Pozostały czas: {remaining}")
    elif device_type == "Dryer":
        cycle = status.get('dryerOperatingState', {}).get('machineState', {}).get('value')
        progress = status.get('custom.dryerJobState', {}).get('jobState', {}).get('value')
        remaining = status.get('dryerOperatingState', {}).get('completionTime', {}).get('value')
        print(f"Stan suszarki: {cycle or progress}")
        if remaining:
            print(f"Pozostały czas: {remaining}")
    elif device_type == "Oven":
        oven_state = status.get('ovenOperatingState', {}).get('machineState', {}).get('value')
        setpoint = status.get('ovenSetpoint', {}).get('setpoint', {}).get('value')
        print(f"Stan piekarnika: {oven_state}")
        if setpoint:
            print(f"Temperatura zadana: {setpoint}")
    elif device_type == "Microwave":
        mw_state = status.get('microwaveOperatingState', {}).get('machineState', {}).get('value')
        print(f"Stan mikrofali: {mw_state}")
    else:
        print("Nieznany typ urządzenia lub brak obsługiwanego statusu.")

def get_status(token, device_id, device_type=None):
    url = f"{API_URL}/devices/{device_id}/status"
    resp = requests.get(url, headers=get_headers(token))
    if resp.status_code != 200:
        print(f"Błąd pobierania statusu: {resp.status_code} {resp.text}")
        sys.exit(1)
    status = resp.json().get('components', {}).get('main', {})
    print(json.dumps(status, indent=2, ensure_ascii=False))
    if device_type:
        print_appliance_status(device_type, status)

def do_config():
    print("=== Konfiguracja SmartThings ===")
    token = input("Podaj swój Personal Access Token (PAT): ").strip()
    save_config({"token": token})
    print(f"Zapisano token do {CONFIG_FILE}")

# --- Main CLI ---
def main():
    parser = argparse.ArgumentParser(description="CLI do obsługi urządzeń SmartThings")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("config", help="Konfiguracja tokena PAT")
    subparsers.add_parser("list", help="Wylistuj urządzenia")

    on_parser = subparsers.add_parser("on", help="Włącz urządzenie")
    on_parser.add_argument("device", help="Nazwa urządzenia")

    off_parser = subparsers.add_parser("off", help="Wyłącz urządzenie")
    off_parser.add_argument("device", help="Nazwa urządzenia")

    status_parser = subparsers.add_parser("status", help="Status urządzenia")
    status_parser.add_argument("device", help="Nazwa urządzenia")

    start_parser = subparsers.add_parser("start", help="Uruchom program")
    start_parser.add_argument("device", help="Nazwa urządzenia")
    start_parser.add_argument("program", help="Nazwa programu")

    stop_parser = subparsers.add_parser("stop", help="Zatrzymaj program")
    stop_parser.add_argument("device", help="Nazwa urządzenia")

    args = parser.parse_args()

    if args.command == "config":
        do_config()
        return

    config = load_config()
    token = config["token"]

    if args.command == "list":
        list_devices(token)
    elif args.command == "on":
        d = device_by_name(token, args.device)
        send_command(token, d['deviceId'], "switch", "on")
    elif args.command == "off":
        d = device_by_name(token, args.device)
        send_command(token, d['deviceId'], "switch", "off")
    elif args.command == "status":
        d = device_by_name(token, args.device)
        # Rozpoznaj typ urządzenia
        device_type = d.get('deviceTypeName') or d.get('type')
        get_status(token, d['deviceId'], device_type)
    elif args.command == "start":
        d = device_by_name(token, args.device)
        # Przykład: piekarnik - "ovenOperatingState", "start"
        send_command(token, d['deviceId'], "ovenOperatingState", "start", [args.program])
    elif args.command == "stop":
        d = device_by_name(token, args.device)
        send_command(token, d['deviceId'], "ovenOperatingState", "stop")

if __name__ == "__main__":
    main()
