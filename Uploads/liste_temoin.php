<?php
// Connexion à la base de données
$pdo = new PDO("mysql:host=localhost;dbname=plateforme_temoin;charset=utf8", "root", "");

// On récupère tous les témoignages et leur questionnaire
$temoins = $pdo->query("
  SELECT t.id, q.titre AS questionnaire, t.fichier_video, t.date_creation 
  FROM temoignages t
  JOIN questionnaires q ON t.questionnaire_id = q.id
  ORDER BY t.date_creation DESC
")->fetchAll(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <title>Vidéos enregistrées</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>

<nav style="background:#eee;padding:10px;text-align:center;">
  <a href="témoignage.php" style="margin:10px;">📤 Envoyer un témoignage</a>
  <a href="liste_temoin.php" style="margin:10px;">📺 Voir les témoignages</a>
  <a href="upload.php" style="margin:10px;">⚙️ Envoi manuel (test)</a>
</nav>


<header>Témoignages enregistrés</header>

<main class="container">
<?php foreach ($temoins as $t): ?>
  <!-- Affichage du titre du questionnaire et de la date -->
  <h3><?= htmlspecialchars($t['questionnaire']) ?> (<?= $t['date_creation'] ?>)</h3>

  <!-- Affichage de la vidéo -->
  <video width="480" controls>
    <source src="<?= htmlspecialchars($t['fichier_video']) ?>" type="video/webm">
    Votre navigateur ne supporte pas la vidéo.
  </video>
  <hr>
<?php endforeach; ?>
</main>

</body>
</html>
