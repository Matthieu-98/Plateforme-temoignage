<?php
session_start(); // Active la session pour accéder à l'utilisateur connecté

$utilisateur_id = $_SESSION['utilisateur_id'] ?? null; // Si pas connecté, NULL

// Connexion à la BDD
$pdo = new PDO("mysql:host=localhost;dbname=plateforme_temoin;charset=utf8", "root", "");

// Vérifie que le formulaire a été soumis et qu’un fichier a bien été envoyé
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['videoUpload']) && $_FILES['videoUpload']['error'] === UPLOAD_ERR_OK) {

    $questionnaire_id = $_POST['questionnaire_id']; // ID sélectionné par l'utilisateur
    $tmp_name = $_FILES['videoUpload']['tmp_name']; // Fichier temporaire
    $file_name = basename($_FILES['videoUpload']['name']); // Nom du fichier d'origine

    $target_dir = "uploads/"; // Dossier de destination
    $unique_name = uniqid() . "_" . $file_name; // Nom unique pour éviter les doublons
    $target_file = $target_dir . $unique_name; // Chemin final complet

    // Créer le dossier s'il n'existe pas
    if (!is_dir($target_dir)) {
        mkdir($target_dir, 0755, true);
    }

    // Déplace le fichier du dossier temporaire au bon endroit
    if (move_uploaded_file($tmp_name, $target_file)) {

        // Enregistrement du lien dans la BDD
        $stmt = $pdo->prepare("INSERT INTO temoignages (utilisateur_id, questionnaire_id, fichier_video) VALUES (?, ?, ?)");
        $stmt->execute([$utilisateur_id, $questionnaire_id, $target_file]);

        echo "Témoignage enregistré avec succès. <a href='liste_temoin.php'>Voir les vidéos</a>";

    } else {
        echo "Erreur lors du déplacement du fichier.";
    }

} else {
    echo "Aucun fichier reçu ou erreur.";
}
?>
