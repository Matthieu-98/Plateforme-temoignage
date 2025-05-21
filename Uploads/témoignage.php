<?php
// Connexion à MySQL avec PDO
$pdo = new PDO("mysql:host=localhost;dbname=plateforme_temoin;charset=utf8", "root", "");

// On récupère tous les questionnaires disponibles
$questionnaires = $pdo->query("SELECT id, titre FROM questionnaires")->fetchAll(PDO::FETCH_ASSOC);

// Démarrage de session pour simuler un utilisateur connecté
session_start();
$_SESSION['utilisateur_id'] = 1; // En réel, cet ID serait récupéré à la connexion
?>

<!-- HTML pour afficher le formulaire -->
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Témoignage vidéo</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>

<nav style="background:#eee;padding:10px;text-align:center;">
  <a href="témoignage.php" style="margin:10px;">📤 Envoyer un témoignage</a>
  <a href="liste_temoin.php" style="margin:10px;">📺 Voir les témoignages</a>
  <a href="upload.php" style="margin:10px;">⚙️ Envoi manuel (test)</a>
</nav>


<header>Partagez vos expériences en vidéo</header>

<main class="container">
  <form action="upload.php" method="POST" enctype="multipart/form-data">
    <!-- Menu déroulant avec les questionnaires -->
    <label for="questionnaire_id">Questionnaire :</label>
    <select name="questionnaire_id" id="questionnaire_id" required>
      <?php foreach ($questionnaires as $q): ?>
        <option value="<?= $q['id'] ?>"><?= htmlspecialchars($q['titre']) ?></option>
      <?php endforeach; ?>
    </select><br><br>

    <!-- Sélection d'un fichier vidéo -->
    <label for="videoUpload">Téléversez votre vidéo :</label>
    <input type="file" name="videoUpload" accept="video/*" required><br><br>

    <!-- Bouton d'envoi -->
    <input type="submit" class="btn-publier" value="Envoyer la vidéo">
  </form>
</main>

</body>
</html>

