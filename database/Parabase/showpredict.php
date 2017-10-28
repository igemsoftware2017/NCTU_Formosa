<!DOCTYPE html>
<html lang="en">
<head>
    <title>NCTU_Formosa Parabase</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="Parabase.css">
    <link rel="icon" href="favicon.ico" type="image/x-icon">
</head>
<body>

<?php
error_reporting(0);

try {
        $db = new PDO("sqlite:Parabase.db");
}
catch (Exception $e) {
        die("Unable to connect to the database, please reflash the webpage again.");
}
$statement = $db->prepare("SELECT * FROM peptide_pathogen_antifungal_ver2");
$statement->execute();
while ($row = $statement->fetch(PDO::FETCH_ASSOC)) {
	echo $row['Peptide'] . "<br>";
	echo $row['seq'] . "<br>";
}
$statement = null;
?>

</body>
</html>