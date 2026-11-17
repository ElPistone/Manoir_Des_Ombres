########################################
# LE MANOIR DES OMBRES — langue.rpy
# Choix de la langue (français / anglais)
########################################

# Le jeu est écrit en français. En anglais, chaque texte passe par T(), qui
# cherche sa traduction dans TRAD_EN (traduction_en.rpy) ; un texte sans
# traduction reste en français plutôt que de disparaître.
default persistent.langue = "fr"

init -10 python:
    TRAD_EN = {}       # rempli par traduction_en.rpy
    ACCEPTE_EN = {}    # réponses admises au clavier, en anglais

    def T(texte):
        """Traduit un texte du jeu dans la langue choisie."""
        if persistent.langue == "en" and texte:
            return TRAD_EN.get(texte, texte)
        return texte

    # Les répliques du narrateur passent toutes par T()
    config.say_menu_text_filter = T

    # Messages de confirmation intégrés à Ren'Py (Quitter, Menu principal...)
    CONFIRMATIONS_FR = {}
    for _nom, _fr in [
            ("ARE_YOU_SURE", "Êtes-vous sûr ?"),
            ("QUIT", "Voulez-vous vraiment quitter ?"),
            ("MAIN_MENU", "Revenir au menu principal ? La partie en cours sera perdue si elle n'est pas sauvegardée."),
            ("OVERWRITE_SAVE", "Écraser cette sauvegarde ?"),
            ("LOADING", "Charger cette partie ? La partie en cours sera perdue si elle n'est pas sauvegardée."),
            ("DELETE_SAVE", "Supprimer cette sauvegarde ?"),
            ("END_REPLAY", "Arrêter la relecture ?")]:
        if hasattr(layout, _nom):
            CONFIRMATIONS_FR[getattr(layout, _nom)] = _fr

    def message_confirmation(message):
        if persistent.langue == "fr":
            return CONFIRMATIONS_FR.get(message, message)
        return message
