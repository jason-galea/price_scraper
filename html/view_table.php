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
            View Website Data - Table
        </h2>
    </header>
    
    <?php include_once("nav.php"); ?>

    <main>
        <?php
            // Vars
            $website = "PCCG";
            // $website = "SCORPTEC";
            $category = "HDD";
            $result_dir = "/var/www/out";

            // Filter filenames to $website & $category
            $filenames = scandir($result_dir, SCANDIR_SORT_DESCENDING);
            $filenames = preg_grep("~^scrape_result_$website\_$category\_.*.json$~", $filenames); 
            $file = "$result_dir/$filenames[0]";
            // DEBUG
            // echo "<p>";
            // echo "$result_dir <br>";
            // echo "$filenames[0] <br>";
            // echo "$file <br>";
            // echo "</p>";

            // Open file
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
            // DEBUG
            echo "<p>";
            // OPTION 1:
            // echo $json_a[0];
            // OPTION 2:
            // foreach ($json_a as $key => $val) {
            //     echo "Item $key:<br>";
            //     echo "Time: " + $val["Time"] + "<br>";
            //     echo "Retailer: " + $val["Retailer"] + "<br>";
            //     echo "Title: " + $val["Title"] + "<br>";
            //     echo "URL: " + $val["URL"] + "<br>";
            //     echo "PriceAUD: " + $val["PriceAUD"] + "<br>";
            //     echo "Brand: " + $val["Brand"] + "<br>";
            //     echo "Series: " + $val["Series"] + "<br>";
            //     echo "HDDCapacity: " + $val["HDDCapacity"] + "<br>";
            //     echo "HDDPricePerTB: " + $val["HDDPricePerTB"] + "<br>";
            //     echo "<br>";
            // }
            // OPTION 3:
            // print_r($json_a);
            // OPTION 5:
            // foreach ($json_a as $key => $val) {
            //     echo "$key : $val <br>";
            // }
            // OPTION 6:
            // foreach ($json_a as $key => $val) {
            //     echo $val["Time"];
            // }
            // OPTION 7:
            foreach ($json_a as $array_i => $array) {
                echo "Iterating over array #$array_i <br>";
                foreach ($array as $key => $val) {
                    echo "$key : $val <br>";

                }
                echo "<br>";
            }
            echo "</p>";




            // // CREATE TABLE
            // echo "<table>";

            // // Fetch table headers
            // // $result = mysqli_query($con,
            // //     "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '$table';"
            // // );
            // $result = $mySQL->getColumns($sqlTable);

            // // Insert table headers
            // echo "<tr>";
            // // $header_row = mysqli_fetch_row($result);
            // $header_row = $mySQL->getColumns($orderColumn);
            // while ($header_row) {
            //     echo "<th>" + $header_row[0] + "</th>";
            //     // $headers_row = mysqli_fetch_row($result);
            //     $headers_row = mysqli_fetch_row($result);
            // }
            // echo "</tr>";
            
            // // Fetch table contents
            // $result = mysqli_query($con,
            //     "SELECT * FROM $sqlTable ORDER BY $orderColumn $orderDirection;"
            // );
            // $row = mysqli_fetch_row($result);

            // // Insert rows
            // while ($row) { // Loop until $row is NULL
            //     echo "<tr>";
            //     foreach ($row as $value) {
            //         echo "<td>$value</td>";
            //     } 
            //     echo "</tr>";
            //     $row = mysqli_fetch_row($result); // Fetch new row
            // }

            // echo "</table>";
        ?>
    </main>
</body>