# 📱 Notifications Tempo EDF - Docker

Script dockerisé pour recevoir les jours Tempo EDF via Telegram.

## 🚀 Installation rapide

### 1. Structure des fichiers

```
tempo-edf/
├── docker-compose.yml
├── .env
└── app/
    └── tempo_notifier.py
```

### 2. Configuration Telegram

#### Créer un bot Telegram:
1. Rechercher **@BotFather** sur Telegram
2. Envoyer `/newbot`
3. Copier le **token** reçu

#### Obtenir votre Chat ID:
1. Rechercher **@userinfobot** sur Telegram
2. Il vous donnera votre **Chat ID**

### 3. Configurer le fichier .env

Éditer `.env` avec vos informations:

```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
TZ=Europe/Paris
```

### 4. Créer le dossier app

```bash
mkdir app
# Placer le fichier tempo_notifier.py dans app/
```

### 5. Lancer

```bash
docker-compose up
```

## ⏰ Automatisation avec cron

Pour recevoir une notification tous les jours à 7h:

```bash
crontab -e
```

Ajouter:
```
0 7 * * * cd /chemin/vers/tempo-edf && docker-compose up
```

## 🔧 Test manuel

```bash
docker-compose up
```

Vous devriez recevoir une notification Telegram!

## 📊 Format de notification

```
🔵 TEMPO EDF - 2025-11-15 🔵

Jour BLEU - Tarif avantageux ✅

━━━━━━━━━━━━━━━━━
Rappel des tarifs Tempo:
🔵 Bleu: 300 jours/an (moins cher)
⚪ Blanc: 43 jours/an (prix moyen)  
🔴 Rouge: 22 jours/an (plus cher)
━━━━━━━━━━━━━━━━━
```

## 🐛 Dépannage

### Le conteneur ne démarre pas
```bash
docker-compose logs
```

### Vérifier les variables d'environnement
```bash
docker-compose config
```

### Reconstruire l'image
```bash
docker-compose up --build
```

---

Développé pour XGR Solutions 🚀
