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
    
    <?php include_once("nav.php");?>

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


            // Import classes
            include_once("SQL.php");

            // Variables
            $sqlTable = "HDD"; // TODO: Turn this into a button
            $orderColumn = "HDDPricePerTB"; // TODO: Turn this into a button
            $orderDirection = "ASC"; // TODO: Turn this into a button


            // CONNECT TO MYSQL
            $con = mysqli_connect($SQL, $SQL_USER, $SQL_PASS);
            mysqli_select_db($con, $SQL_DB);


            // CREATE TABLE
            echo "<table>";
            // Fetch table headers
            $result = mysqli_query($con,
                "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '$table';"
            );
            // Insert table headers
            echo "<tr>";
            $header_row = mysqli_fetch_row($result);
            while ($header_row) {
                echo "<th>" + $header_row[0] + "</th>";
                $headers_row = mysqli_fetch_row($result);
            }
            echo "</tr>";
            
            // Fetch table contents
            $result = mysqli_query($con,
                "SELECT * FROM $sqlTable ORDER BY $orderColumn $orderDirection;"
            );
            $row = mysqli_fetch_row($result);

            // Insert rows
            while ($row) { // Loop until $row is NULL
                echo "<tr>";
                foreach ($row as $value) {
                    echo "<td>$value</td>";
                } 
                echo "</tr>";
                $row = mysqli_fetch_row($result); // Fetch new row
            }

            echo "</table>";
        ?>
    </main>
</body>