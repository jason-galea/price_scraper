<?php

// FORM VARS
$labels = [
    "website" => [
        "pccg" => "PC Case Gear",
        "scorptec" => "Scorptec",
        "centrecom" => "Centre Com",
    ],
    "category" => [
        "hdd" => "3.5\" Hard Drive",
        "ssd" => "SSD",
        "cpu" => "CPU",
        "gpu" => "GPU",
    ],
];
$current_filename = basename($__NAME__);


// PRINT FORM
echo "<br><form method='post' action='$current_filename'>";
foreach ($labels as $dict_key => $dict) {
    echo "<p>Please select a $dict_key:</p>";
    foreach ($dict as $label => $detail) {
        echo "<input type='radio' id='$label' name='$dict_key' value='$label'>";
        echo "<label for='$label'>$detail</label><br>";
    }
}
echo "<br><input type='submit' value='Submit'></form>";


// CHECK FORM
if (isset($_POST["website"]) and isset($_POST["category"])) {
    $website = $_POST["website"];
    $category = $_POST["category"];
    echo "<p>Received website \"$website\" and category \"$category\"</p>";
} else {
    exit();
}

?>