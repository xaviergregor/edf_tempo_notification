#!/usr/bin/env python3
"""
Notification Telegram - Jours Tempo EDF (Version Complète)
Récupère la couleur du jour ET du lendemain et envoie une notification
"""

import requests
import os
import sys
from datetime import datetime

# Configuration depuis variables d'environnement
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# APIs Tempo
API_TODAY = "https://www.api-couleur-tempo.fr/api/today"
API_TOMORROW = "https://www.api-couleur-tempo.fr/api/tomorrow"


def get_tempo_info():
    """Récupère les informations Tempo (aujourd'hui + demain)"""
    try:
        # Récupérer aujourd'hui
        print("🔍 Récupération de la couleur du jour...")
        response_today = requests.get(API_TODAY, timeout=10)
        response_today.raise_for_status()
        today = response_today.json()
        
        # Récupérer demain
        print("🔍 Récupération de la couleur de demain...")
        response_tomorrow = requests.get(API_TOMORROW, timeout=10)
        response_tomorrow.raise_for_status()
        tomorrow = response_tomorrow.json()
        
        return {
            'today': {
                'couleur': today.get('libCouleur', 'INCONNU').upper(),
                'date': today.get('dateJour', datetime.now().strftime('%Y-%m-%d')),
                'periode': today.get('periode', 'N/A')
            },
            'tomorrow': {
                'couleur': tomorrow.get('libCouleur', 'INCONNU').upper(),
                'date': tomorrow.get('dateJour', 'N/A'),
                'periode': tomorrow.get('periode', 'N/A')
            }
        }
    except Exception as e:
        print(f"❌ Erreur API: {e}")
        return None


def format_message(tempo_info):
    """Formate le message de notification avec aujourd'hui ET demain"""
    today = tempo_info['today']
    tomorrow = tempo_info['tomorrow']
    
    emojis = {'BLEU': '🔵', 'BLANC': '⚪', 'ROUGE': '🔴', 'INCONNU': '❓'}
    messages = {
        'BLEU': 'Tarif avantageux ✅',
        'BLANC': 'Tarif normal ⚠️',
        'ROUGE': 'Tarif élevé ⛔',
        'INCONNU': 'Information non disponible'
    }
    
    today_emoji = emojis.get(today['couleur'], '❓')
    tomorrow_emoji = emojis.get(tomorrow['couleur'], '❓')
    today_msg = messages.get(today['couleur'], 'Info non disponible')
    tomorrow_msg = messages.get(tomorrow['couleur'], 'Info non disponible')
    
    return f"""
{today_emoji} <b>TEMPO EDF - {today['date']}</b> {today_emoji}

<b>AUJOURD'HUI:</b> Jour {today['couleur']}
{today_msg}

<b>DEMAIN:</b> {tomorrow_emoji} Jour {tomorrow['couleur']}
{tomorrow_msg}

━━━━━━━━━━━━━━━━━
<b>Rappel des tarifs Tempo:</b>
🔵 <b>Bleu</b>: 300 jours/an (le moins cher)
⚪ <b>Blanc</b>: 43 jours/an (prix moyen)
🔴 <b>Rouge</b>: 22 jours/an (le plus cher)

<i>Période: {today['periode']}</i>
━━━━━━━━━━━━━━━━━
""".strip()


def send_telegram(message):
    """Envoie la notification via Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ Configuration Telegram manquante!")
        print("Vérifiez les variables TELEGRAM_BOT_TOKEN et TELEGRAM_CHAT_ID")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        print("✅ Notification Telegram envoyée!")
        return True
    except Exception as e:
        print(f"❌ Erreur Telegram: {e}")
        return False


def main():
    print("╔════════════════════════════════════════╗")
    print("║   TEMPO EDF - Notification Telegram    ║")
    print("╚════════════════════════════════════════╝")
    print()
    
    tempo_info = get_tempo_info()
    
    if not tempo_info:
        print("❌ Impossible de récupérer les informations Tempo")
        sys.exit(1)
    
    print(f"✅ Aujourd'hui: {tempo_info['today']['couleur']}")
    print(f"✅ Demain: {tempo_info['tomorrow']['couleur']}")
    print()
    
    message = format_message(tempo_info)
    print("📱 Message à envoyer:")
    print("=" * 40)
    # Afficher sans les balises HTML pour le terminal
    print(message.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', ''))
    print("=" * 40)
    print()
    
    send_telegram(message)


if __name__ == "__main__":
    main()
