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
            Home Page
        </h2>
    </header>
    <p>
        <?php
            // TODO: Refactor, make it somewhat object-oriented
            // 

            // Constants
            $SQL_IP = "127.0.0.1";
            // $SQL_IP = "10.1.1.60";
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
            
            // Fetch taable contents
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
    </p>
</body>