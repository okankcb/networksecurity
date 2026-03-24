import sys
from networksecurity.logging import logger

# Création d'une exception personnalisée
class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        self.error_message = error_message
        
        # Récupère les informations de l'erreur (type, objet, traceback)
        _, _, exc_tb = error_details.exc_info()
        
        # Numéro de ligne où l'erreur s'est produite
        self.lineno = exc_tb.tb_lineno
        
        # Nom du fichier où l'erreur s'est produite
        self.file_name = exc_tb.tb_frame.f_code.co_filename 
    
    def __str__(self):
        return "Une erreur est survenue dans le script Python [{0}] à la ligne [{1}] avec le message [{2}]".format(
            self.file_name, self.lineno, str(self.error_message)
        )
