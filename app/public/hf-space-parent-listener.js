/**
 * Script pour la fenêtre parente des Spaces Hugging Face
 * Ce script écoute les messages de l'iframe et met à jour l'URL de la fenêtre parente
 * 
 * Instructions d'utilisation :
 * 1. Ajoutez ce script à votre Space Hugging Face dans le fichier app.py ou dans un composant Gradio
 * 2. Ou utilisez-le dans une page HTML qui contient votre iframe
 */

(function () {
    'use strict';

    // Écouter les messages de l'iframe
    window.addEventListener('message', function (event) {

        // Vérifier le type de message
        if (event.data && event.data.type) {
            switch (event.data.type) {
                case 'urlChange':
                case 'anchorChange':
                case 'HF_SPACE_URL_UPDATE':
                    handleUrlChange(event.data);
                    break;
                default:
                // Message type inconnu, ignorer
            }
        }
    });

    function handleUrlChange(data) {
        try {
            const hash = data.hash || data.anchorId;
            const url = data.url;

            if (hash) {
                // Mettre à jour l'URL avec la nouvelle ancre
                const newUrl = new URL(window.location);
                newUrl.hash = hash;

                // Utiliser replaceState pour éviter d'ajouter une entrée dans l'historique
                window.history.replaceState(null, '', newUrl.toString());

                // Optionnel : faire défiler vers l'élément correspondant dans la page parente
                const targetElement = document.querySelector(hash);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }
        } catch (error) {
            // Erreur silencieuse lors de la mise à jour de l'URL
        }
    }

    // Fonction utilitaire pour tester la communication
    window.testIframeCommunication = function () {
        const iframe = document.querySelector('iframe');
        if (iframe) {
            iframe.contentWindow.postMessage({ type: 'test' }, '*');
        }
    };

})();
