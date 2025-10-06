"""Multilingual support for the referral bot"""

import logging
from typing import Dict, Optional, Any
from enum import Enum

logger = logging.getLogger(__name__)

class SupportedLanguage(Enum):
    """Supported languages for the bot"""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    RUSSIAN = "ru"
    ARABIC = "ar"
    CHINESE = "zh"
    JAPANESE = "ja"
    KOREAN = "ko"
    HINDI = "hi"
    TURKISH = "tr"
    DUTCH = "nl"
    POLISH = "pl"

class LanguageDetector:
    """Detect user language based on various signals"""
    
    @staticmethod
    def detect_from_telegram_user(user) -> str:
        """Detect language from Telegram user data"""
        if hasattr(user, 'language_code') and user.language_code:
            # Map common Telegram language codes to our supported languages
            lang_map = {
                'en': SupportedLanguage.ENGLISH.value,
                'es': SupportedLanguage.SPANISH.value,
                'fr': SupportedLanguage.FRENCH.value,
                'de': SupportedLanguage.GERMAN.value,
                'it': SupportedLanguage.ITALIAN.value,
                'pt': SupportedLanguage.PORTUGUESE.value,
                'ru': SupportedLanguage.RUSSIAN.value,
                'ar': SupportedLanguage.ARABIC.value,
                'zh': SupportedLanguage.CHINESE.value,
                'ja': SupportedLanguage.JAPANESE.value,
                'ko': SupportedLanguage.KOREAN.value,
                'hi': SupportedLanguage.HINDI.value,
                'tr': SupportedLanguage.TURKISH.value,
                'nl': SupportedLanguage.DUTCH.value,
                'pl': SupportedLanguage.POLISH.value,
            }
            
            # Handle language codes with region (e.g., 'en-US' -> 'en')
            base_lang = user.language_code.split('-')[0].lower()
            return lang_map.get(base_lang, SupportedLanguage.ENGLISH.value)
        
        return SupportedLanguage.ENGLISH.value

    @staticmethod
    def detect_from_text(text: str) -> str:
        """Basic text-based language detection using common words"""
        if not text:
            return SupportedLanguage.ENGLISH.value
        
        text_lower = text.lower()
        
        # Language detection patterns (common words/phrases)
        patterns = {
            SupportedLanguage.SPANISH.value: ['hola', 'gracias', 'por favor', 'si', 'no', 'buenos dias', 'buenas tardes'],
            SupportedLanguage.FRENCH.value: ['bonjour', 'merci', 'oui', 'non', 'salut', 'bonsoir', 'au revoir'],
            SupportedLanguage.GERMAN.value: ['hallo', 'danke', 'bitte', 'ja', 'nein', 'guten tag', 'auf wiedersehen'],
            SupportedLanguage.ITALIAN.value: ['ciao', 'grazie', 'prego', 'si', 'no', 'buongiorno', 'buonasera'],
            SupportedLanguage.PORTUGUESE.value: ['ola', 'obrigado', 'por favor', 'sim', 'nao', 'bom dia', 'boa tarde'],
            SupportedLanguage.RUSSIAN.value: ['привет', 'спасибо', 'пожалуйста', 'да', 'нет', 'здравствуйте'],
            SupportedLanguage.ARABIC.value: ['مرحبا', 'شكرا', 'من فضلك', 'نعم', 'لا', 'السلام عليكم'],
            SupportedLanguage.CHINESE.value: ['你好', '谢谢', '请', '是', '不是', '早上好'],
            SupportedLanguage.JAPANESE.value: ['こんにちは', 'ありがとう', 'はい', 'いいえ', 'おはよう'],
            SupportedLanguage.KOREAN.value: ['안녕하세요', '감사합니다', '네', '아니요', '좋은 아침'],
            SupportedLanguage.HINDI.value: ['नमस्ते', 'धन्यवाद', 'कृपया', 'हाँ', 'नहीं'],
            SupportedLanguage.TURKISH.value: ['merhaba', 'teşekkür', 'lütfen', 'evet', 'hayır', 'günaydın'],
            SupportedLanguage.DUTCH.value: ['hallo', 'dank je', 'alstublieft', 'ja', 'nee', 'goedemorgen'],
            SupportedLanguage.POLISH.value: ['cześć', 'dziękuję', 'proszę', 'tak', 'nie', 'dzień dobry'],
        }
        
        # Count matches for each language
        scores = {}
        for lang, words in patterns.items():
            score = sum(1 for word in words if word in text_lower)
            if score > 0:
                scores[lang] = score
        
        # Return language with highest score, default to English
        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]
        
        return SupportedLanguage.ENGLISH.value

class MultilingualMessages:
    """Message translations for different languages"""
    
    MESSAGES = {
        SupportedLanguage.ENGLISH.value: {
            "welcome_new_user": """
🎉 Welcome to the referral system!

To get started:
1. First, join our channel: {channel_link}
2. Once you join, I'll give you your unique referral link
3. Share your link with friends to earn rewards!

Click the link above to join the channel, then come back here.
""",
            "welcome_existing_member": """
🎉 Welcome back! I can see you're already a member of {channel_name}.

Here's your unique referral link:
{referral_link}

📋 **Your Mission:**
Share this link with friends and get {target} people to join the channel using your link to earn your reward!

🔗 **How it works:**
1. Share your referral link with friends
2. When they click it and join the channel, you get credit
3. Reach {target} successful referrals to claim your reward

Use /status to check your progress anytime!
""",
            "channel_joined_success": """
✅ Great! You've successfully joined {channel_name}!

Here's your unique referral link:
{referral_link}

📋 **Your Mission:**
Share this link with friends and get {target} people to join the channel using your link to earn your reward!

🔗 **How it works:**
1. Share your referral link with friends
2. When they click it and join the channel, you get credit
3. Reach {target} successful referrals to claim your reward

Use /status to check your progress anytime!
""",
            "referral_welcome": """
👋 Welcome! You were referred by a friend.

Please join our channel to continue: {channel_link}

After joining, you'll get your own referral link to start earning rewards too!
""",
            "status_message": """
📊 **Your Referral Status**

👥 Active Referrals: {active_referrals}/{target}
📈 Total Referrals Made: {total_referrals}
🎯 Target: {target} referrals
🔥 Remaining: {remaining}
📊 Progress: {progress}%

{progress_bar}

{status_text}
""",
            "reward_available": """
🎉 **CONGRATULATIONS!** 🎉

You've reached your referral target! Your reward is ready to claim.

Use /claim to get your reward!
""",
            "reward_claimed": """
🏆 **REWARD CLAIMED!** 🏆

{reward_message}

Thank you for helping grow our community! Keep sharing your referral link to help even more people discover our channel.

Your referral link is still active: {referral_link}
""",
            "help_message": """
🤖 **Referral Bot Commands**

/start - Get your referral link and instructions
/status - Check your referral progress
/claim - Claim your reward (when target is reached)
/help - Show this help message
/language - Change language settings

📋 **How the referral system works:**
1. Get your unique referral link from /start
2. Share it with friends
3. When friends join using your link, you get credit
4. Reach the target number of referrals to earn rewards
5. Use /claim to get your reward

💡 **Tips:**
- Share your link in groups, social media, or with friends
- Only active channel members count towards your target
- If someone leaves the channel, they won't count anymore
- You can check your progress anytime with /status
""",
            "error_not_channel_member": """
❌ You need to be a member of the channel first!

Join here: {channel_link}

After joining, come back and use /start again.
""",
            "error_reward_already_claimed": """
✅ You've already claimed your reward!

Your referral link is still active if you want to keep helping grow the community: {referral_link}
""",
            "error_reward_not_available": """
❌ You haven't reached the referral target yet.

Current progress: {active_referrals}/{target}

Use /status to see your detailed progress.
""",
            "language_selection": """
🌍 **Select Your Language / Selecciona tu idioma / Choisissez votre langue**

Choose your preferred language:
""",
            "language_changed": """
✅ Language changed to English!

All future messages will be in English.
""",
            "progress_bar_full": "🟩",
            "progress_bar_empty": "⬜",
            "status_target_reached": "🎉 Target reached! Use /claim to get your reward!",
            "status_no_referrals": "🚀 Start sharing your referral link to earn rewards!",
            "status_progress": "🔥 Great progress! Just {remaining} more referrals to go!",
        },
        
        SupportedLanguage.SPANISH.value: {
            "welcome_new_user": """
🎉 ¡Bienvenido al sistema de referidos!

Para comenzar:
1. Primero, únete a nuestro canal: {channel_link}
2. Una vez que te unas, te daré tu enlace de referido único
3. ¡Comparte tu enlace con amigos para ganar recompensas!

Haz clic en el enlace de arriba para unirte al canal, luego regresa aquí.
""",
            "welcome_existing_member": """
🎉 ¡Bienvenido de vuelta! Veo que ya eres miembro de {channel_name}.

Aquí está tu enlace de referido único:
{referral_link}

📋 **Tu Misión:**
¡Comparte este enlace con amigos y consigue que {target} personas se unan al canal usando tu enlace para ganar tu recompensa!

🔗 **Cómo funciona:**
1. Comparte tu enlace de referido con amigos
2. Cuando hagan clic y se unan al canal, obtienes crédito
3. Alcanza {target} referidos exitosos para reclamar tu recompensa

¡Usa /status para verificar tu progreso en cualquier momento!
""",
            "channel_joined_success": """
✅ ¡Genial! ¡Te has unido exitosamente a {channel_name}!

Aquí está tu enlace de referido único:
{referral_link}

📋 **Tu Misión:**
¡Comparte este enlace con amigos y consigue que {target} personas se unan al canal usando tu enlace para ganar tu recompensa!

🔗 **Cómo funciona:**
1. Comparte tu enlace de referido con amigos
2. Cuando hagan clic y se unan al canal, obtienes crédito
3. Alcanza {target} referidos exitosos para reclamar tu recompensa

¡Usa /status para verificar tu progreso en cualquier momento!
""",
            "referral_welcome": """
👋 ¡Bienvenido! Fuiste referido por un amigo.

Por favor únete a nuestro canal para continuar: {channel_link}

¡Después de unirte, obtendrás tu propio enlace de referido para comenzar a ganar recompensas también!
""",
            "status_message": """
📊 **Estado de tus Referidos**

👥 Referidos Activos: {active_referrals}/{target}
📈 Total de Referidos Hechos: {total_referrals}
🎯 Objetivo: {target} referidos
🔥 Restantes: {remaining}
📊 Progreso: {progress}%

{progress_bar}

{status_text}
""",
            "reward_available": """
🎉 **¡FELICITACIONES!** 🎉

¡Has alcanzado tu objetivo de referidos! Tu recompensa está lista para reclamar.

¡Usa /claim para obtener tu recompensa!
""",
            "reward_claimed": """
🏆 **¡RECOMPENSA RECLAMADA!** 🏆

{reward_message}

¡Gracias por ayudar a hacer crecer nuestra comunidad! Sigue compartiendo tu enlace de referido para ayudar a que aún más personas descubran nuestro canal.

Tu enlace de referido sigue activo: {referral_link}
""",
            "help_message": """
🤖 **Comandos del Bot de Referidos**

/start - Obtén tu enlace de referido e instrucciones
/status - Verifica tu progreso de referidos
/claim - Reclama tu recompensa (cuando se alcance el objetivo)
/help - Muestra este mensaje de ayuda
/language - Cambiar configuración de idioma

📋 **Cómo funciona el sistema de referidos:**
1. Obtén tu enlace único de referido desde /start
2. Compártelo con amigos
3. Cuando los amigos se unan usando tu enlace, obtienes crédito
4. Alcanza el número objetivo de referidos para ganar recompensas
5. Usa /claim para obtener tu recompensa

💡 **Consejos:**
- Comparte tu enlace en grupos, redes sociales, o con amigos
- Solo los miembros activos del canal cuentan para tu objetivo
- Si alguien deja el canal, ya no contará
- Puedes verificar tu progreso en cualquier momento con /status
""",
            "error_not_channel_member": """
❌ ¡Necesitas ser miembro del canal primero!

Únete aquí: {channel_link}

Después de unirte, regresa y usa /start otra vez.
""",
            "error_reward_already_claimed": """
✅ ¡Ya has reclamado tu recompensa!

Tu enlace de referido sigue activo si quieres seguir ayudando a hacer crecer la comunidad: {referral_link}
""",
            "error_reward_not_available": """
❌ Aún no has alcanzado el objetivo de referidos.

Progreso actual: {active_referrals}/{target}

Usa /status para ver tu progreso detallado.
""",
            "language_selection": """
🌍 **Selecciona tu Idioma / Select Your Language / Choisissez votre langue**

Elige tu idioma preferido:
""",
            "language_changed": """
✅ ¡Idioma cambiado a Español!

Todos los mensajes futuros serán en español.
""",
            "progress_bar_full": "🟩",
            "progress_bar_empty": "⬜",
            "status_target_reached": "🎉 ¡Objetivo alcanzado! ¡Usa /claim para obtener tu recompensa!",
            "status_no_referrals": "🚀 ¡Comienza a compartir tu enlace de referido para ganar recompensas!",
            "status_progress": "🔥 ¡Gran progreso! ¡Solo {remaining} referidos más para llegar!",
        },
        
        SupportedLanguage.FRENCH.value: {
            "welcome_new_user": """
🎉 Bienvenue dans le système de parrainage !

Pour commencer :
1. D'abord, rejoignez notre chaîne : {channel_link}
2. Une fois que vous rejoignez, je vous donnerai votre lien de parrainage unique
3. Partagez votre lien avec des amis pour gagner des récompenses !

Cliquez sur le lien ci-dessus pour rejoindre la chaîne, puis revenez ici.
""",
            "welcome_existing_member": """
🎉 Bon retour ! Je vois que vous êtes déjà membre de {channel_name}.

Voici votre lien de parrainage unique :
{referral_link}

📋 **Votre Mission :**
Partagez ce lien avec des amis et obtenez {target} personnes pour rejoindre la chaîne en utilisant votre lien pour gagner votre récompense !

🔗 **Comment ça marche :**
1. Partagez votre lien de parrainage avec des amis
2. Quand ils cliquent et rejoignent la chaîne, vous obtenez du crédit
3. Atteignez {target} parrainages réussis pour réclamer votre récompense

Utilisez /status pour vérifier votre progression à tout moment !
""",
            "channel_joined_success": """
✅ Génial ! Vous avez rejoint {channel_name} avec succès !

Voici votre lien de parrainage unique :
{referral_link}

📋 **Votre Mission :**
Partagez ce lien avec des amis et obtenez {target} personnes pour rejoindre la chaîne en utilisant votre lien pour gagner votre récompense !

🔗 **Comment ça marche :**
1. Partagez votre lien de parrainage avec des amis
2. Quand ils cliquent et rejoignent la chaîne, vous obtenez du crédit
3. Atteignez {target} parrainages réussis pour réclamer votre récompense

Utilisez /status pour vérifier votre progression à tout moment !
""",
            "referral_welcome": """
👋 Bienvenue ! Vous avez été parrainé par un ami.

Veuillez rejoindre notre chaîne pour continuer : {channel_link}

Après avoir rejoint, vous obtiendrez votre propre lien de parrainage pour commencer à gagner des récompenses aussi !
""",
            "status_message": """
📊 **Statut de vos Parrainages**

👥 Parrainages Actifs : {active_referrals}/{target}
📈 Total de Parrainages Réalisés : {total_referrals}
🎯 Objectif : {target} parrainages
🔥 Restant : {remaining}
📊 Progression : {progress}%

{progress_bar}

{status_text}
""",
            "reward_available": """
🎉 **FÉLICITATIONS !** 🎉

Vous avez atteint votre objectif de parrainage ! Votre récompense est prête à être réclamée.

Utilisez /claim pour obtenir votre récompense !
""",
            "reward_claimed": """
🏆 **RÉCOMPENSE RÉCLAMÉE !** 🏆

{reward_message}

Merci d'aider à faire grandir notre communauté ! Continuez à partager votre lien de parrainage pour aider encore plus de personnes à découvrir notre chaîne.

Votre lien de parrainage est toujours actif : {referral_link}
""",
            "help_message": """
🤖 **Commandes du Bot de Parrainage**

/start - Obtenez votre lien de parrainage et les instructions
/status - Vérifiez votre progression de parrainage
/claim - Réclamez votre récompense (quand l'objectif est atteint)
/help - Affichez ce message d'aide
/language - Changer les paramètres de langue

📋 **Comment fonctionne le système de parrainage :**
1. Obtenez votre lien de parrainage unique depuis /start
2. Partagez-le avec des amis
3. Quand les amis rejoignent en utilisant votre lien, vous obtenez du crédit
4. Atteignez le nombre cible de parrainages pour gagner des récompenses
5. Utilisez /claim pour obtenir votre récompense

💡 **Conseils :**
- Partagez votre lien dans des groupes, sur les réseaux sociaux, ou avec des amis
- Seuls les membres actifs de la chaîne comptent pour votre objectif
- Si quelqu'un quitte la chaîne, il ne comptera plus
- Vous pouvez vérifier votre progression à tout moment avec /status
""",
            "error_not_channel_member": """
❌ Vous devez d'abord être membre de la chaîne !

Rejoignez ici : {channel_link}

Après avoir rejoint, revenez et utilisez /start à nouveau.
""",
            "error_reward_already_claimed": """
✅ Vous avez déjà réclamé votre récompense !

Votre lien de parrainage est toujours actif si vous voulez continuer à aider à faire grandir la communauté : {referral_link}
""",
            "error_reward_not_available": """
❌ Vous n'avez pas encore atteint l'objectif de parrainage.

Progression actuelle : {active_referrals}/{target}

Utilisez /status pour voir votre progression détaillée.
""",
            "language_selection": """
🌍 **Sélectionnez votre langue / Select Your Language / Elija su idioma**

Choisissez votre langue préférée :
""",
            "language_changed": """
✅ Langue changée en Français !

Tous les futurs messages seront en français.
""",
            "progress_bar_full": "🟩",
            "progress_bar_empty": "⬜",
            "status_target_reached": "🎉 Objectif atteint ! Utilisez /claim pour obtenir votre récompense !",
            "status_no_referrals": "🚀 Commencez à partager votre lien de parrainage pour gagner des récompenses !",
            "status_progress": "🔥 Bonne progression ! Encore {remaining} parrainages pour atteindre l'objectif !",
        },
        
        SupportedLanguage.GERMAN.value: {
            "welcome_new_user": """
🎉 Willkommen im Empfehlungssystem!

So fangen Sie an:
1. Treten Sie zuerst unserem Kanal bei: {channel_link}
2. Sobald Sie beigetreten sind, gebe ich Ihnen Ihren einzigartigen Empfehlungslink
3. Teilen Sie Ihren Link mit Freunden, um Belohnungen zu verdienen!

Klicken Sie auf den Link oben, um dem Kanal beizutreten, dann kommen Sie hierher zurück.
""",
            "welcome_existing_member": """
🎉 Willkommen zurück! Ich sehe, dass Sie bereits Mitglied von {channel_name} sind.

Hier ist Ihr einzigartiger Empfehlungslink:
{referral_link}

📋 **Ihre Mission:**
Teilen Sie diesen Link mit Freunden und lassen Sie {target} Personen dem Kanal über Ihren Link beitreten, um Ihre Belohnung zu erhalten!

🔗 **So funktioniert es:**
1. Teilen Sie Ihren Empfehlungslink mit Freunden
2. Wenn sie darauf klicken und dem Kanal beitreten, erhalten Sie Punkte
3. Erreichen Sie {target} erfolgreiche Empfehlungen, um Ihre Belohnung zu beanspruchen

Verwenden Sie /status, um Ihren Fortschritt jederzeit zu überprüfen!
""",
            "channel_joined_success": """
✅ Großartig! Sie sind {channel_name} erfolgreich beigetreten!

Hier ist Ihr einzigartiger Empfehlungslink:
{referral_link}

📋 **Ihre Mission:**
Teilen Sie diesen Link mit Freunden und lassen Sie {target} Personen dem Kanal über Ihren Link beitreten, um Ihre Belohnung zu erhalten!

🔗 **So funktioniert es:**
1. Teilen Sie Ihren Empfehlungslink mit Freunden
2. Wenn sie darauf klicken und dem Kanal beitreten, erhalten Sie Punkte
3. Erreichen Sie {target} erfolgreiche Empfehlungen, um Ihre Belohnung zu beanspruchen

Verwenden Sie /status, um Ihren Fortschritt jederzeit zu überprüfen!
""",
            "referral_welcome": """
👋 Willkommen! Sie wurden von einem Freund empfohlen.

Bitte treten Sie unserem Kanal bei, um fortzufahren: {channel_link}

Nach dem Beitritt erhalten Sie Ihren eigenen Empfehlungslink, um auch Belohnungen zu verdienen!
""",
            "status_message": """
📊 **Ihr Empfehlungsstatus**

👥 Aktive Empfehlungen: {active_referrals}/{target}
📈 Gesamte Empfehlungen: {total_referrals}
🎯 Ziel: {target} Empfehlungen
🔥 Verbleibend: {remaining}
📊 Fortschritt: {progress}%

{progress_bar}

{status_text}
""",
            "reward_available": """
🎉 **GLÜCKWUNSCH!** 🎉

Sie haben Ihr Empfehlungsziel erreicht! Ihre Belohnung ist bereit zum Abholen.

Verwenden Sie /claim, um Ihre Belohnung zu erhalten!
""",
            "reward_claimed": """
🏆 **BELOHNUNG ABGEHOLT!** 🏆

{reward_message}

Danke, dass Sie helfen, unsere Gemeinschaft wachsen zu lassen! Teilen Sie weiterhin Ihren Empfehlungslink, um noch mehr Menschen unseren Kanal entdecken zu lassen.

Ihr Empfehlungslink ist weiterhin aktiv: {referral_link}
""",
            "help_message": """
🤖 **Empfehlungs-Bot Befehle**

/start - Holen Sie sich Ihren Empfehlungslink und Anweisungen
/status - Überprüfen Sie Ihren Empfehlungsfortschritt
/claim - Fordern Sie Ihre Belohnung an (wenn das Ziel erreicht ist)
/help - Zeigt diese Hilfemeldung an
/language - Spracheinstellungen ändern

📋 **Wie das Empfehlungssystem funktioniert:**
1. Holen Sie sich Ihren einzigartigen Empfehlungslink mit /start
2. Teilen Sie ihn mit Freunden
3. Wenn Freunde über Ihren Link beitreten, erhalten Sie Punkte
4. Erreichen Sie die Zielanzahl an Empfehlungen, um Belohnungen zu verdienen
5. Verwenden Sie /claim, um Ihre Belohnung zu erhalten

💡 **Tipps:**
- Teilen Sie Ihren Link in Gruppen, sozialen Medien oder mit Freunden
- Nur aktive Kanalmitglieder zählen für Ihr Ziel
- Wenn jemand den Kanal verlässt, zählt er nicht mehr
- Sie können Ihren Fortschritt jederzeit mit /status überprüfen
""",
            "error_not_channel_member": """
❌ Sie müssen zuerst Mitglied des Kanals sein!

Treten Sie hier bei: {channel_link}

Kehren Sie danach zurück und verwenden Sie /start erneut.
""",
            "error_reward_already_claimed": """
✅ Sie haben Ihre Belohnung bereits abgeholt!

Ihr Empfehlungslink ist weiterhin aktiv, wenn Sie helfen möchten, die Gemeinschaft wachsen zu lassen: {referral_link}
""",
            "error_reward_not_available": """
❌ Sie haben das Empfehlungsziel noch nicht erreicht.

Aktueller Fortschritt: {active_referrals}/{target}

Verwenden Sie /status, um Ihren detaillierten Fortschritt zu sehen.
""",
            "language_selection": """
🌍 **Wählen Sie Ihre Sprache / Select Your Language / Elija su idioma**

Wählen Sie Ihre bevorzugte Sprache:
""",
            "language_changed": """
✅ Sprache auf Deutsch geändert!

Alle zukünftigen Nachrichten werden auf Deutsch sein.
""",
            "progress_bar_full": "🟩",
            "progress_bar_empty": "⬜",
            "status_target_reached": "🎉 Ziel erreicht! Verwenden Sie /claim, um Ihre Belohnung zu erhalten!",
            "status_no_referrals": "🚀 Beginnen Sie mit dem Teilen Ihres Empfehlungslinks, um Belohnungen zu verdienen!",
            "status_progress": "🔥 Guter Fortschritt! Nur noch {remaining} Empfehlungen bis zum Ziel!",
        },
        
        SupportedLanguage.ITALIAN.value: {
            "welcome_new_user": """
🎉 Benvenuto nel sistema di referral!

Per iniziare:
1. Prima, unisciti al nostro canale: {channel_link}
2. Una volta iscritto, ti darò il tuo link di referral unico
3. Condividi il tuo link con gli amici per guadagnare ricompense!

Clicca sul link sopra per unirti al canale, poi torna qui.
""",
            "welcome_existing_member": """
🎉 Bentornato! Vedo che sei già membro di {channel_name}.

Ecco il tuo link di referral unico:
{referral_link}

📋 **La tua Missione:**
Condividi questo link con gli amici e fai iscrivere {target} persone al canale usando il tuo link per guadagnare la tua ricompensa!

🔗 **Come funziona:**
1. Condividi il tuo link di referral con gli amici
2. Quando cliccano e si uniscono al canale, ottieni crediti
3. Raggiungi {target} referral di successo per richiedere la tua ricompensa

Usa /status per controllare i tuoi progressi in qualsiasi momento!
""",
            "channel_joined_success": """
✅ Grande! Ti sei unito con successo a {channel_name}!

Ecco il tuo link di referral unico:
{referral_link}

📋 **La tua Missione:**
Condividi questo link con gli amici e fai iscrivere {target} persone al canale usando il tuo link per guadagnare la tua ricompensa!

🔗 **Come funziona:**
1. Condividi il tuo link di referral con gli amici
2. Quando cliccano e si uniscono al canale, ottieni crediti
3. Raggiungi {target} referral di successo per richiedere la tua ricompensa

Usa /status per controllare i tuoi progressi in qualsiasi momento!
""",
            "referral_welcome": """
👋 Benvenuto! Sei stato invitato da un amico.

Per favore unisciti al nostro canale per continuare: {channel_link}

Dopo esserti unito, riceverai il tuo link di referral per iniziare a guadagnare ricompense anche tu!
""",
            "status_message": """
📊 **Il tuo Stato dei Referral**

👥 Referral Attivi: {active_referrals}/{target}
📈 Referral Totali Effettuati: {total_referrals}
🎯 Obiettivo: {target} referral
🔥 Rimanenti: {remaining}
📊 Progresso: {progress}%

{progress_bar}

{status_text}
""",
            "reward_available": """
🎉 **CONGRATULAZIONI!** 🎉

Hai raggiunto il tuo obiettivo di referral! La tua ricompensa è pronta per essere richiesta.

Usa /claim per ottenere la tua ricompensa!
""",
            "reward_claimed": """
🏆 **RICOMPENSA RICHIESTA!** 🏆

{reward_message}

Grazie per aver aiutato a far crescere la nostra comunità! Continua a condividere il tuo link di referral per aiutare ancora più persone a scoprire il nostro canale.

Il tuo link di referral è ancora attivo: {referral_link}
""",
            "help_message": """
🤖 **Comandi del Bot di Referral**

/start - Ottieni il tuo link di referral e le istruzioni
/status - Controlla i tuoi progressi dei referral
/claim - Richiedi la tua ricompensa (quando l'obiettivo è raggiunto)
/help - Mostra questo messaggio di aiuto
/language - Cambia le impostazioni della lingua

📋 **Come funziona il sistema di referral:**
1. Ottieni il tuo link di referral unico da /start
2. Condividilo con gli amici
3. Quando gli amici si uniscono usando il tuo link, ottieni crediti
4. Raggiungi il numero obiettivo di referral per guadagnare ricompense
5. Usa /claim per ottenere la tua ricompensa

💡 **Suggerimenti:**
- Condividi il tuo link in gruppi, social media, o con amici
- Solo i membri attivi del canale contano per il tuo obiettivo
- Se qualcuno lascia il canale, non conterà più
- Puoi controllare i tuoi progressi in qualsiasi momento con /status
""",
            "error_not_channel_member": """
❌ Devi prima essere membro del canale!

Unisciti qui: {channel_link}

Dopo esserti unito, torna indietro e usa /start di nuovo.
""",
            "error_reward_already_claimed": """
✅ Hai già richiesto la tua ricompensa!

Il tuo link di referral è ancora attivo se vuoi continuare ad aiutare a far crescere la comunità: {referral_link}
""",
            "error_reward_not_available": """
❌ Non hai ancora raggiunto l'obiettivo di referral.

Progresso attuale: {active_referrals}/{target}

Usa /status per vedere i tuoi progressi dettagliati.
""",
            "language_selection": """
🌍 **Seleziona la tua Lingua / Select Your Language / Elija su idioma**

Scegli la tua lingua preferita:
""",
            "language_changed": """
✅ Lingua cambiata in Italiano!

Tutti i futuri messaggi saranno in italiano.
""",
            "progress_bar_full": "🟩",
            "progress_bar_empty": "⬜",
            "status_target_reached": "🎉 Obiettivo raggiunto! Usa /claim per ottenere la tua ricompensa!",
            "status_no_referrals": "🚀 Inizia a condividere il tuo link di referral per guadagnare ricompense!",
            "status_progress": "🔥 Buon progresso! Solo {remaining} referral in più per raggiungere l'obiettivo!",
        },
        
        SupportedLanguage.PORTUGUESE.value: {
            "welcome_new_user": """
🎉 Bem-vindo ao sistema de referência!

Para começar:
1. Primeiro, junte-se ao nosso canal: {channel_link}
2. Assim que você se juntar, eu lhe darei seu link de referência único
3. Compartilhe seu link com amigos para ganhar recompensas!

Clique no link acima para se juntar ao canal, depois volte aqui.
""",
            "welcome_existing_member": """
🎉 Bem-vindo de volta! Vejo que você já é membro de {channel_name}.

Aqui está o seu link de referência único:
{referral_link}

📋 **Sua Missão:**
Compartilhe este link com amigos e faça com que {target} pessoas se juntem ao canal usando seu link para ganhar sua recompensa!

🔗 **Como funciona:**
1. Compartilhe seu link de referência com amigos
2. Quando eles clicarem e se juntarem ao canal, você ganha créditos
3. Alcance {target} referências bem-sucedidas para reivindicar sua recompensa

Use /status para verificar seu progresso a qualquer momento!
""",
            "channel_joined_success": """
✅ Ótimo! Você se juntou com sucesso a {channel_name}!

Aqui está o seu link de referência único:
{referral_link}

📋 **Sua Missão:**
Compartilhe este link com amigos e faça com que {target} pessoas se juntem ao canal usando seu link para ganhar sua recompensa!

🔗 **Como funciona:**
1. Compartilhe seu link de referência com amigos
2. Quando eles clicarem e se juntarem ao canal, você ganha créditos
3. Alcance {target} referências bem-sucedidas para reivindicar sua recompensa

Use /status para verificar seu progresso a qualquer momento!
""",
            "referral_welcome": """
👋 Bem-vindo! Você foi indicado por um amigo.

Por favor, junte-se ao nosso canal para continuar: {channel_link}

Depois de se juntar, você receberá seu próprio link de referência para começar a ganhar recompensas também!
""",
            "status_message": """
📊 **Seu Status de Referência**

👥 Referências Ativas: {active_referrals}/{target}
📈 Total de Referências Feitas: {total_referrals}
🎯 Objetivo: {target} referências
🔥 Restantes: {remaining}
📊 Progresso: {progress}%

{progress_bar}

{status_text}
""",
            "reward_available": """
🎉 **PARABÉNS!** 🎉

Você atingiu seu objetivo de referência! Sua recompensa está pronta para ser reivindicada.

Use /claim para obter sua recompensa!
""",
            "reward_claimed": """
🏆 **RECOMPENSA REIVINDICADA!** 🏆

{reward_message}

Obrigado por ajudar a crescer nossa comunidade! Continue compartilhando seu link de referência para ajudar ainda mais pessoas a descobrir nosso canal.

Seu link de referência ainda está ativo: {referral_link}
""",
            "help_message": """
🤖 **Comandos do Bot de Referência**

/start - Obtenha seu link de referência e instruções
/status - Verifique seu progresso de referência
/claim - Reivindique sua recompensa (quando o objetivo for atingido)
/help - Mostra esta mensagem de ajuda
/language - Alterar configurações de idioma

📋 **Como o sistema de referência funciona:**
1. Obtenha seu link de referência único de /start
2. Compartilhe-o com amigos
3. Quando amigos se juntarem usando seu link, você ganha créditos
4. Alcance o número alvo de referências para ganhar recompensas
5. Use /claim para obter sua recompensa

💡 **Dicas:**
- Compartilhe seu link em grupos, redes sociais ou com amigos
- Apenas membros ativos do canal contam para seu objetivo
- Se alguém sair do canal, eles não contarão mais
- Você pode verificar seu progresso a qualquer momento com /status
""",
            "error_not_channel_member": """
❌ Você precisa ser membro do canal primeiro!

Junte-se aqui: {channel_link}

Depois de se juntar, volte e use /start novamente.
""",
            "error_reward_already_claimed": """
✅ Você já reivindicou sua recompensa!

Seu link de referência ainda está ativo se você quiser continuar ajudando a crescer a comunidade: {referral_link}
""",
            "error_reward_not_available": """
❌ Você ainda não atingiu o objetivo de referência.

Progresso atual: {active_referrals}/{target}

Use /status para ver seu progresso detalhado.
""",
            "language_selection": """
🌍 **Selecione seu Idioma / Select Your Language / Elija su idioma**

Escolha seu idioma preferido:
""",
            "language_changed": """
✅ Idioma alterado para Português!

Todas as futuras mensagens serão em português.
""",
            "progress_bar_full": "🟩",
            "progress_bar_empty": "⬜",
            "status_target_reached": "🎉 Objetivo atingido! Use /claim para obter sua recompensa!",
            "status_no_referrals": "🚀 Comece a compartilhar seu link de referência para ganhar recompensas!",
            "status_progress": "🔥 Ótimo progresso! Apenas mais {remaining} referências para atingir o objetivo!",
        },
        
        SupportedLanguage.RUSSIAN.value: {
            "welcome_new_user": """
🎉 Добро пожаловать в систему рефералов!

Чтобы начать:
1. Сначала присоединитесь к нашему каналу: {channel_link}
2. Как только вы присоединитесь, я дам вам уникальную реферальную ссылку
3. Делитесь своей ссылкой с друзьями, чтобы заработать награды!

Нажмите на ссылку выше, чтобы присоединиться к каналу, затем вернитесь сюда.
""",
            "welcome_existing_member": """
🎉 С возвращением! Вижу, что вы уже участник {channel_name}.

Вот ваша уникальная реферальная ссылка:
{referral_link}

📋 **Ваша миссия:**
Поделитесь этой ссылкой с друзьями и приведите {target} человек в канал, используя вашу ссылку, чтобы получить награду!

🔗 **Как это работает:**
1. Поделитесь своей реферальной ссылкой с друзьями
2. Когда они нажмут и присоединятся к каналу, вы получите кредит
3. Достигните {target} успешных рефералов, чтобы получить награду

Используйте /status, чтобы проверить свой прогресс в любое время!
""",
            "channel_joined_success": """
✅ Отлично! Вы успешно присоединились к {channel_name}!

Вот ваша уникальная реферальная ссылка:
{referral_link}

📋 **Ваша миссия:**
Поделитесь этой ссылкой с друзьями и приведите {target} человек в канал, используя вашу ссылку, чтобы получить награду!

🔗 **Как это работает:**
1. Поделитесь своей реферальной ссылкой с друзьями
2. Когда они нажмут и присоединятся к каналу, вы получите кредит
3. Достигните {target} успешных рефералов, чтобы получить награду

Используйте /status, чтобы проверить свой прогресс в любое время!
""",
            "referral_welcome": """
👋 Добро пожаловать! Вас пригласил друг.

Пожалуйста, присоединитесь к нашему каналу, чтобы продолжить: {channel_link}

После присоединения вы получите свою собственную реферальную ссылку, чтобы тоже начать зарабатывать награды!
""",
            "status_message": """
📊 **Ваш статус рефералов**

👥 Активные рефералы: {active_referrals}/{target}
📈 Всего рефералов: {total_referrals}
🎯 Цель: {target} рефералов
🔥 Осталось: {remaining}
📊 Прогресс: {progress}%

{progress_bar}

{status_text}
""",
            "reward_available": """
🎉 **ПОЗДРАВЛЯЕМ!** 🎉

Вы достигли своей цели по рефералам! Ваша награда готова к получению.

Используйте /claim, чтобы получить награду!
""",
            "reward_claimed": """
🏆 **НАГРАДА ПОЛУЧЕНА!** 🏆

{reward_message}

Спасибо, что помогаете развивать наше сообщество! Продолжайте делиться своей реферальной ссылкой, чтобы помочь еще большему количеству людей открыть для себя наш канал.

Ваша реферальная ссылка все еще активна: {referral_link}
""",
            "help_message": """
🤖 **Команды бота рефералов**

/start - Получить реферальную ссылку и инструкции
/status - Проверить прогресс рефералов
/claim - Получить награду (когда цель достигнута)
/help - Показать это справочное сообщение
/language - Изменить настройки языка

📋 **Как работает система рефералов:**
1. Получите уникальную реферальную ссылку через /start
2. Поделитесь ею с друзьями
3. Когда друзья присоединяются по вашей ссылке, вы получаете кредиты
4. Достигните целевого количества рефералов, чтобы заработать награды
5. Используйте /claim, чтобы получить награду

💡 **Советы:**
- Делитесь своей ссылкой в группах, социальных сетях или с друзьями
- Только активные участники канала учитываются в вашей цели
- Если кто-то покидает канал, он больше не учитывается
- Вы можете проверить свой прогресс в любое время с помощью /status
""",
            "error_not_channel_member": """
❌ Сначала вы должны быть участником канала!

Присоединяйтесь здесь: {channel_link}

После присоединения вернитесь и снова используйте /start.
""",
            "error_reward_already_claimed": """
✅ Вы уже получили свою награду!

Ваша реферальная ссылка все еще активна, если вы хотите продолжать помогать развивать сообщество: {referral_link}
""",
            "error_reward_not_available": """
❌ Вы еще не достигли цели по рефералам.

Текущий прогресс: {active_referrals}/{target}

Используйте /status, чтобы увидеть подробный прогресс.
""",
            "language_selection": """
🌍 **Выберите ваш язык / Select Your Language / Elija su idioma**

Выберите предпочитаемый язык:
""",
            "language_changed": """
✅ Язык изменен на русский!

Все будущие сообщения будут на русском языке.
""",
            "progress_bar_full": "🟩",
            "progress_bar_empty": "⬜",
            "status_target_reached": "🎉 Цель достигнута! Используйте /claim, чтобы получить награду!",
            "status_no_referrals": "🚀 Начните делиться своей реферальной ссылкой, чтобы заработать награды!",
            "status_progress": "🔥 Отличный прогресс! Еще {remaining} рефералов до цели!",
        },
        
        SupportedLanguage.ARABIC.value: {
            "welcome_new_user": """
🎉 مرحباً بك في نظام الإحالة!

للبدء:
1. أولاً، انضم إلى قناتنا: {channel_link}
2. بمجرد انضمامك، سأعطيك رابط الإحالة الفريد الخاص بك
3. شارك رابطك مع الأصدقاء لكسب المكافآت!

انقر على الرابط أعلاه للانضمام إلى القناة، ثم عد إلى هنا.
""",
            "welcome_existing_member": """
🎉 مرحباً بك مجدداً! أرى أنك عضو في {channel_name}.

إليك رابط الإحالة الفريد الخاص بك:
{referral_link}

📋 **مهمتك:**
شارك هذا الرابط مع الأصدقاء واحصل على {target} شخص للانضمام إلى القناة باستخدام رابطك لكسب مكافأتك!

🔗 **كيف يعمل:**
1. شارك رابط الإحالة الخاص بك مع الأصدقاء
2. عندما ينقرون ويضموا القناة، تحصل على ائتمان
3. اصل إلى {target} إحالات ناجحة للمطالبة بمكافأتك

استخدم /status للتحقق من تقدمك في أي وقت!
""",
            "channel_joined_success": """
✅ عظيم! لقد انضممت بنجاح إلى {channel_name}!

إليك رابط الإحالة الفريد الخاص بك:
{referral_link}

📋 **مهمتك:**
شارك هذا الرابط مع الأصدقاء واحصل على {target} شخص للانضمام إلى القناة باستخدام رابطك لكسب مكافأتك!

🔗 **كيف يعمل:**
1. شارك رابط الإحالة الخاص بك مع الأصدقاء
2. عندما ينقرون ويضموا القناة، تحصل على ائتمان
3. اصل إلى {target} إحالات ناجحة للمطالبة بمكافأتك

استخدم /status للتحقق من تقدمك في أي وقت!
""",
            "referral_welcome": """
👋 مرحباً بك! تمت دعوتك بواسطة صديق.

يرجى الانضمام إلى قناتنا للمتابعة: {channel_link}

بعد الانضمام، ستحصل على رابط الإحالة الخاص بك لبدء كسب المكافآت أيضاً!
""",
            "status_message": """
📊 **حالة الإحالات الخاصة بك**

👥 الإحالات النشطة: {active_referrals}/{target}
📈 إجمالي الإحالات المحققة: {total_referrals}
🎯 الهدف: {target} إحالة
🔥 المتبقي: {remaining}
📊 التقدم: {progress}%

{progress_bar}

{status_text}
""",
            "reward_available": """
🎉 **تهانينا!** 🎉

لقد وصلت إلى هدفك في الإحالات! مكافأتك جاهزة للمطالبة.

استخدم /claim للحصول على مكافأتك!
""",
            "reward_claimed": """
🏆 **تم المطالبة بالمكافأة!** 🏆

{reward_message}

شكراً لك على مساعدتك في نمو مجتمعنا! استمر في مشاركة رابط الإحالة الخاص بك لمساعدة المزيد من الناس على اكتشاف قناتنا.

رابط الإحالة الخاص بك لا يزال نشطاً: {referral_link}
""",
            "help_message": """
🤖 **أوامر بوت الإحالة**

/start - احصل على رابط الإحالة الخاص بك والتعليمات
/status - تحقق من تقدم الإحالات الخاصة بك
/claim - اطلب مكافأتك (عند بلوغ الهدف)
/help - إظهار رسالة المساعدة هذه
/language - تغيير إعدادات اللغة

📋 **كيف يعمل نظام الإحالة:**
1. احصل على رابط الإحالة الفريد الخاص بك من /start
2. شاركه مع الأصدقاء
3. عندما ينضم الأصدقاء باستخدام رابطك، تحصل على ائتمان
4. اصل إلى العدد المستهدف من الإحالات لكسب المكافآت
5. استخدم /claim للحصول على مكافأتك

💡 **نصائح:**
- شارك رابطك في المجموعات، وسائل التواصل الاجتماعي، أو مع الأصدقاء
- فقط أعضاء القناة النشطون يحسبون لهدفك
- إذا غادر شخص ما القناة، فلن يُحسب بعد الآن
- يمكنك التحقق من تقدمك في أي وقت باستخدام /status
""",
            "error_not_channel_member": """
❌ تحتاج إلى أن تكون عضواً في القناة أولاً!

انضم هنا: {channel_link}

بعد الانضمام، عد واستخدم /start مرة أخرى.
""",
            "error_reward_already_claimed": """
✅ لقد طلبت مكافأتك بالفعل!

رابط الإحالة الخاص بك لا يزال نشطاً إذا كنت ترغب في مواصلة مساعدة نمو المجتمع: {referral_link}
""",
            "error_reward_not_available": """
❌ لم تصل بعد إلى هدف الإحالات.

التقدم الحالي: {active_referrals}/{target}

استخدم /status لرؤية تقدمك المفصل.
""",
            "language_selection": """
🌍 **اختر لغتك / Select Your Language / Elija su idioma**

اختر لغتك المفضلة:
""",
            "language_changed": """
✅ تم تغيير اللغة إلى العربية!

جميع الرسائل المستقبلية ستكون باللغة العربية.
""",
            "progress_bar_full": "🟩",
            "progress_bar_empty": "⬜",
            "status_target_reached": "🎉 تم بلوغ الهدف! استخدم /claim للحصول على مكافأتك!",
            "status_no_referrals": "🚀 ابدأ في مشاركة رابط الإحالة الخاص بك لكسب المكافآت!",
            "status_progress": "🔥 تقدم رائع! فقط {remaining} إحالات أخرى للوصول إلى الهدف!",
        }
    }
    
    def get_message(self, language: str, key: str, fallback: str = None, **kwargs) -> str:
        """Get a message in the specified language with optional formatting"""
        # Get the language messages, fallback to English if not found
        lang_messages = self.MESSAGES.get(language, self.MESSAGES[SupportedLanguage.ENGLISH.value])
        
        # Get the message template, fallback to English if not found
        message = lang_messages.get(key)
        if not message and fallback:
            return fallback
        elif not message:
            # Try to get from English as final fallback
            english_messages = self.MESSAGES[SupportedLanguage.ENGLISH.value]
            message = english_messages.get(key, f"Missing message: {key}")
        
        # Format the message with provided kwargs
        try:
            return message.format(**kwargs)
        except KeyError as e:
            # If formatting fails, return the message without formatting
            logger.warning(f"Failed to format message {key} for language {language}: {e}")
            return message
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get available languages with their names"""
        return {
            SupportedLanguage.ENGLISH.value: "English 🇬🇧",
            SupportedLanguage.SPANISH.value: "Español 🇪🇸",
            SupportedLanguage.FRENCH.value: "Français 🇫🇷",
            SupportedLanguage.GERMAN.value: "Deutsch 🇩🇪",
            SupportedLanguage.ITALIAN.value: "Italiano 🇮🇹",
            SupportedLanguage.PORTUGUESE.value: "Português 🇵🇹",
            SupportedLanguage.RUSSIAN.value: "Русский 🇷🇺",
            SupportedLanguage.ARABIC.value: "العربية 🇸🇦",
            SupportedLanguage.CHINESE.value: "中文 🇨🇳",
            SupportedLanguage.JAPANESE.value: "日本語 🇯🇵",
            SupportedLanguage.KOREAN.value: "한국어 🇰🇷",
            SupportedLanguage.HINDI.value: "हिन्दी 🇮🇳",
            SupportedLanguage.TURKISH.value: "Türkçe 🇹🇷",
            SupportedLanguage.DUTCH.value: "Nederlands 🇳🇱",
            SupportedLanguage.POLISH.value: "Polski 🇵🇱",
        }

class LanguageManager:
    """Manage user language preferences using in-memory storage for now"""
    
    def __init__(self, database):
        self.db = database
        self._user_languages = {}  # In-memory storage for user languages
        self._init_language_table()
    
    def _init_language_table(self):
        """Initialize language preferences (using in-memory storage)"""
        try:
            logger.info("Language manager initialized with in-memory storage")
        except Exception as e:
            logger.error(f"Error initializing language manager: {e}")
    
    def set_user_language(self, user_id: int, language_code: str, detected: bool = False) -> bool:
        """Set user's preferred language"""
        try:
            self._user_languages[user_id] = language_code
            return True
        except Exception as e:
            logger.error(f"Error setting user language: {e}")
            return False
    
    def get_user_language(self, user_id: int) -> str:
        """Get user's preferred language"""
        try:
            return self._user_languages.get(user_id, SupportedLanguage.ENGLISH.value)
        except Exception as e:
            logger.error(f"Error getting user language: {e}")
            return SupportedLanguage.ENGLISH.value
    
    def detect_and_set_language(self, user_id: int, telegram_user, message_text: str = None) -> str:
        """Detect and set user language based on available signals"""
        # First try to get existing preference
        existing_lang = self.get_user_language(user_id)
        if existing_lang != SupportedLanguage.ENGLISH.value:
            return existing_lang
        
        # Detect from Telegram user data
        detected_lang = LanguageDetector.detect_from_telegram_user(telegram_user)
        
        # If we have message text, also try text detection
        if message_text and message_text.strip():
            text_lang = LanguageDetector.detect_from_text(message_text)
            # Prefer text detection if it's not English (more specific)
            if text_lang != SupportedLanguage.ENGLISH.value:
                detected_lang = text_lang
        
        # Set the detected language
        self.set_user_language(user_id, detected_lang, detected=True)
        return detected_lang