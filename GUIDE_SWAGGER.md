# Guide de test de l'API Banque avec Swagger

## Démarrage du serveur

```bash
# Installer les dépendances
pip install -r requirements.txt

# Démarrer le serveur
uvicorn main:app --reload
```

Accédez à Swagger UI : http://localhost:8000/docs

## Étapes de test

### 1. Création de comptes test

**Route :** `POST /comptes/`

Créez 2-3 comptes pour tester :

```json
{
  "nom": "Alice Dupont",
  "email": "alice@email.com",
  "code": "password123",
  "solde_initial": 1000
}
```

```json
{
  "nom": "Bob Martin",
  "email": "bob@email.com", 
  "code": "password456",
  "solde_initial": 500
}
```

### 2. Connexion (Authentification)

**Route :** `POST /token`

Utilisez le formulaire OAuth2PasswordRequestForm :
- **username** : alice@email.com
- **password** : password123

Copiez le `access_token` retourné, il sera nécessaire pour les autres requêtes.

### 3. Configuration de l'authentification dans Swagger

1. Cliquez sur le bouton **"Authorize"** en haut à droite
2. Dans la boîte de dialogue, entrez : `Bearer VOTRE_TOKEN_ICI`
3. Cliquez sur **"Authorize"**

### 4. Consultation du compte

**Route :** `GET /mon-compte`

Vérifiez vos informations et solde actuel.

### 5. Dépôt d'argent

**Route :** `POST /depot`

```json
{
  "montant": 200,
  "description": "Salaire"
}
```

### 6. Retrait d'argent

**Route :** `POST /retrait`

```json
{
  "montant": 100,
  "description": "Courses"
}
```

### 7. Recherche de comptes

**Route :** `GET /recherche`

Utilisez le paramètre `q` pour chercher :
- Par nom : `q=Bob`
- Par email : `q=bob@email.com`
- Par ID : `q=ID_DU_COMPTE`

### 8. Transfert vers un autre compte

**Route :** `POST /transfert`

1. D'abord recherchez l'ID du compte destinataire avec `/recherche`
2. Puis effectuez le transfert :

```json
{
  "montant": 150,
  "compte_destination_id": "ID_BOB",
  "description": "Remboursement déjeuner"
}
```

### 9. Consultation de l'historique

**Route :** `GET /transactions`

Voyez toutes vos transactions (dépôts, retraits, transferts émis/reçus).

### 10. Liste de tous les comptes

**Route :** `GET /comptes/`

Affiche tous les comptes existants (nécessite d'être connecté).

## Tests d'erreur à essayer

### Valider la gestion des erreurs :

1. **Connexion avec mauvais mot de passe** : `POST /token` avec password incorrect
2. **Dépôt négatif** : `POST /depot` avec montant < 0
3. **Retrait supérieur au solde** : `POST /retrait` avec montant > solde
4. **Transfert vers soi-même** : `POST /transfert` avec votre propre ID
5. **Transfert vers compte inexistant** : `POST /transfert` avec ID invalide
6. **Email déjà utilisé** : `POST /comptes/` avec email existant
7. **Accès sans token** : Essayez d'accéder aux routes protégées sans vous authentifier

## Fonctionnalités implémentées

✅ **Authentification JWT** avec tokens sécurisés  
✅ **Hashage des mots de passe** avec bcrypt  
✅ **Création de comptes** avec validation email unique  
✅ **Dépôts** avec historique  
✅ **Retraits** avec vérification de solde  
✅ **Transferts** entre comptes avec double écriture  
✅ **Recherche** par nom, email ou ID  
✅ **Historique complet** des transactions  
✅ **Gestion des erreurs** détaillée  
✅ **Documentation auto-générée** Swagger UI  

## Notes importantes

- Les données sont stockées en mémoire (perdues au redémarrage)
- Les tokens expirent après 30 minutes
- Les IDs de comptes sont des UUID tronqués (8 caractères)
