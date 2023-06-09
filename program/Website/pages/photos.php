<?php

include('../models/Leader.php');

$json = file_get_contents('../data/leader_photos.json');
$datas = json_decode($json, true);
$leader_photos = [];

if (isset($_GET['id']) == true && $_GET['id'] !== "") {
    $id = $_GET['id'];
    foreach ($datas as $data) {
        if ($data['id'] == $id) array_push($leader_photos, new Leader((array) $data));
    }
} else {
    foreach ($datas as $data) {
        array_push($leader_photos, new Leader((array) $data));
    }
}
shuffle($leader_photos);

?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Photos</title>
    <link rel="stylesheet" href="../css/style.css">
    <link rel="stylesheet" href="../css/photos.css">
</head>

<body>
    <?php include("../components/header.php") ?>

    <form action="#">
        <input type="text" id="id" name="id" placeholder="Input Person's id"/>
        <label for="id">
            <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 15.75l-2.489-2.489m0 0a3.375 3.375 0 10-4.773-4.773 3.375 3.375 0 004.774 4.774zM21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
        </label>
    </form>

    <div id="container">
        <?php foreach ($leader_photos as $data) : ?>
            <?php foreach ($data->photos as $photo) : ?>
                <img class="img" src=".<?= $photo ?>" alt="<?= $photo ?>">
            <?php endforeach; ?>
        <?php endforeach; ?>
    </div>

</body>

</html>