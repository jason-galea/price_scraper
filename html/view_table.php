<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="style.css"/>
    
    <title>Price Scraper</title>
</head>
<body>
    <header>
        <h2>
            View Data - Table
        </h2>
    </header>
    
    <?php
        include_once("nav.php");
        include_once("nav_view.php");
    ?>

    <main>

        <?php

        // PRINT FORM
        include_once("web_cat_form.php");

        // CHECK FORM
        if (isset($_POST["website"]) and isset($_POST["category"])) {
            $website = $_POST["website"];
            $category = $_POST["category"];
            echo "<p>Showing \"$category\" data from \"$website\"</p>";
        } else {
            exit();
        }



        // VARS
        $result_dir = "/var/www/out";



        // GET FILENAME
        $filenames = scandir($result_dir, SCANDIR_SORT_DESCENDING);
        $filenames = preg_grep("~^scrape_result_$website\_$category\_.*.json$~", $filenames); 
        $file = "$result_dir/$filenames[0]";
        // DEBUG
        echo "<p>";
        // echo "$result_dir <br>";
        // echo "$filenames[0] <br>";
        echo "$file <br>";
        echo "</p>";



        // OPEN FILE
        $json_s = file_get_contents($file, True);
        if ($json_s === false) {
            echo "ERROR: Unable to open file \"$file\"";
            exit();
        }
        // DEBUG
        // echo "<p>";
        // echo $json_s;
        // echo "</p>";



        // Convert string to JSON object
        $json_a = json_decode($json_s, true);
        if ($json_a === null) {
            echo "ERROR: Unable to convert JSON string to object";
            exit();
        }
        // // DEBUG
        // foreach ($json_a as $array_i => $array) {
        //     echo "<p>";
        //     echo "Iterating over array #$array_i <br>";
        //     foreach ($array as $key => $val) {
        //         echo "$key : $val <br>";
        //     }
        //     echo "</p>";
        // }



        // CREATE TABLE
        echo "<table>";

        // Print headings
        echo "<tr>";
        foreach ($json_a[0] as $key => $val) {
            switch ($key) {
                // Fail conditions
                case "website":
                case "URL":
                case "Brand":
                case "Series":
                    break;
                default:
                    echo "<th>$key</th>";
                    
            }
        }
        echo "</tr>";

        // Print  rows
        foreach ($json_a as $array_i => $array) {
            echo "<tr>";
            foreach ($array as $key => $val) {
                switch ($key) {
                    // Fail conditions
                    case "website":
                    case "URL":
                    case "Brand":
                    case "Series":
                        break;
                    // Special cases
                    case "Title":
                        $URL = $array["URL"];
                        echo "<td><a href=\"$URL\">$val</a></td>";
                        break;
                    default:
                        echo "<td>$val</td>";
                        
                }
            }
            echo "</tr>";
        }
        echo "</table>";

        ?>

    </main>
</body>