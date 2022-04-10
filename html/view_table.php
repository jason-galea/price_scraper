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
            // TODO: Make a "home" menu
                // 1. Scrape website data
                    // a. "Which site?"
                    // b. "Which hardware category?"
                    // c. --> Pass arguments to script                        
                        // WHEN IMPLEMENTED, THE SCRIPT CAN BE MANAGED ENTIRELY FROM THE SITE
                // 2. View website data
                    // a. "Graph?"
                        // "Select metric"
                            // Eg. Price, Capacity, Price per TB
                    // b. "Table?"
                        // "Select ???"
                    // c. "Clear table?"
                        // WHEN IMPLEMENTED, THE SCRIPT CAN BE MANAGED ENTIRELY FROM THE SITE

            // TODO: Read JSON
            // List JSON files in dir

            // For each filename, convert into time and check when is most recent (highest)
            
            $most_recent_file = "/var/www/out/scrape_result_PCCG_HDD_2022-04-11_00-12-52.json";

            // Open most recent file
            $json_string = file_get_contents($most_recent_file, True);
            // echo "<p>";
            // echo $json_string;
            // echo "</p>";

            // Convert string to JSON object

            $json_object = json_decode($json_string);
            var_dump(json_decode($json_object));
            // echo "<p>";
            // echo $json_object;
            // echo "</p>";
            var_dump(json_decode($json_object, true));

            // echo "<p>";
            // echo $json_object;
            // echo "</p>";




            // // CREATE TABLE
            echo "<table>";

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

            echo "</table>";
        ?>
    </main>
</body>