<?php

// FORM VARS
$labels = [
    "website" => [
        "PCCG" => "PC Case Gear",
        "SCORPTEC" => "Scorptec",
        "CENTRECOM" => "Centre Com",
    ],
    "category" => [
        "HDD" => "3.5\" Hard Drive",
        "CPU" => "CPU",
        "GPU" => "GPU",
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

?>