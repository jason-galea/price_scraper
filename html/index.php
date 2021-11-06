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
            Welcome to the (Australian PC hardware website) Price Scraper!
        </h2>
    </header>

    <?php include_once("nav.php");?>

    <main>
        <?php
            // TODO: Refactor, make it somewhat object-oriented

            // TODO: Refactor "fetch & display" logic
                // 1. SELECT * FROM some_table;
                // 2. Store EVERYTHING in an array of dicts, one dict = one row
                // 3. Have a static whitelist of column names, per category
                    // (The whitelist controls what is actually displayed in the HTML table)
                // 4. Display data in a table, but some some subtlety
                    // Titles are hrefs to their stored URL
                    // Add "$" to each price, etc.

            // TODO: Make a "home" menu
                // 1. Scrape website
                    // a. "Which site?"
                    // b. "Which hardware category?"
                    // c. --> Pass arguments to script                        
                        // WHEN IMPLEMENTED, THE SCRIPT CAN BE MANAGED ENTIRELY FROM THE SITE
                // 2. View historic data
                    // a. "Graph?"
                        // "Select metric"
                            // Eg. Price, Capacity, Price per TB
                    // b. "Table?"
                        // "Select ???"
                    // c. "Clear table?"
                        // WHEN IMPLEMENTED, THE SCRIPT CAN BE MANAGED ENTIRELY FROM THE SITE

            // Constants
            // TODO: Move these details to a .txt file in ~/
            $SQL_IP = "127.0.0.1";
            // $SQL_IP = "10.1.1.160";
            $SQL_USER = "scraper";
            $SQL_PASS = "Password##123";
            $SQL_DB = "PriceScraper";

            // Variables
            $sqlTable = "HDD"; // TODO: Turn this into a button
            $orderColumn = "HDDPricePerTB"; // TODO: Turn this into a button
            $orderDirection = "ASC"; // TODO: Turn this into a button


            // CONNECT TO MYSQL
            $con = mysqli_connect($SQL_IP, $SQL_USER, $SQL_PASS);
            mysqli_select_db($con, $SQL_DB);


            // CREATE TABLE
            echo "<table>";
            // Fetch table headers
            $result = mysqli_query($con,
                "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '$table';"
            );
            // Insert table headers
            echo "<tr>";
            foreach ($row as $value) {
                // echo "<th><b>$value</b></th>";
                echo "<th>$value</th>";
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