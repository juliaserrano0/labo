from flask import Flask, render_template, request, send_file, jsonify
import os
import re

app = Flask(__name__)

# Fonction pour valider et convertir JJ/MM/AAAA en JJMMAAAA
def format_date(date_str):
    # Vérifier que la date correspond au format JJ/MM/AAAA
    if not re.match(r"^\d{2}/\d{2}/\d{4}$", date_str):
        return None
    return date_str.replace("/", "")

# Dossier où sont stockés les fichiers Word
RESULTATS_DIR = os.path.join(os.path.dirname(__file__), 'resultats')

# Route pour la page d'accueil
@app.route('/')
def index():
    return render_template('index.html')

# Route pour gérer le téléchargement
@app.route('/download', methods=['POST'])
def download():
    # Récupérer les données du formulaire
    nom = request.form.get('nom', '').strip()
    prenom = request.form.get('prenom', '').strip()
    date_naissance = request.form.get('date_naissance', '').strip()

    # Convertir la date de naissance en JJMMAAAA
    date_naissance = format_date(date_naissance)
    if not date_naissance:
        return jsonify({"message": "La date de naissance doit être au format JJ/MM/AAAA."}), 400

    # Créer le nom du fichier (ex: Dupont_Jean_01011990.docx)
    filename = f"{nom}_{prenom}_{date_naissance}.docx"
    filepath = os.path.join(RESULTATS_DIR, filename)

    # Vérifier si le fichier existe
    if os.path.exists(filepath):
        # Envoyer le fichier en téléchargement
        return send_file(filepath, as_attachment=True)
    else:
        # Renvoyer une réponse JSON si le fichier n'existe pas
        return jsonify({"message": "Aucun résultat trouvé. Vérifiez les informations saisies."}), 404

# Démarrer l'application
if __name__ == '__main__':
    app.run(debug=True, port=5000)
