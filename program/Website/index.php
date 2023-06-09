<?php
include('./models/Country.php');

$json = file_get_contents("./data/country.json");
$datas = json_decode($json, true);

$countries = [];

foreach ($datas as $data) {
    array_push($countries, new Country((array) $data));
}
?>

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
    <link rel="stylesheet" href="./css/style.css">
    <link rel="stylesheet" href="./css/home.css">
</head>

<body>
    <?php include("./components/header.php") ?>

    <div id="container">
        <?php foreach ($countries as $data) : ?>
            <div id="<?= $data->id ?>" class="card">
                <div class="leader">
                    <div class="photo">
                        <img class="default" src="<?= $data->photo ?>" alt="<?= $data->photo ?>">
                        <img class="hover" src="<?= $data->photo2 ?>" alt="<?= $data->photo ?>">
                    </div>
                    <div class="info">
                        <h2 class="name"><?= $data->leader ?></h2>
                        <p class="position"><?= $data->position ?></p>
                    </div>
                </div>
                <div class="flag">
                    <img src="<?= $data->country_flag ?>" alt="<?= $data->country_flag ?>">
                </div>
            </div>
        <?php endforeach; ?>
    </div>

</body>

</html>