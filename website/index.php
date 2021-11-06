<html>
<head>
    <title>PHP Test</title>
</head>
<body>
    <header>
        <h2>
            Home Page
        </h2>
    </header>
    <?php
        // Constants
        $SQL_IP = "127.0.0.1";
        // $SQL_IP = "10.1.1.60";
        $SQL_USER = "scraper";
        $SQL_PASS = "Password##123";
        $SQL_DB = "PriceScraper";

        // Variables
        $sqlTable = "HDD";

        $orderColumn = "HDDPricePerTB";
        $orderDirection = "ASC";


        // CONNECT TO MYSQL
        $con = mysqli_connect($SQL_IP, $SQL_USER, $SQL_PASS);
        mysqli_select_db($con, $SQL_DB);


        // CREATE TABLE
        echo "<table>";
        // Fetch column names
        $result = mysqli_query($con,
            "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '$table';"
        );
        // Insert one row of column names
        echo "<tr>";
            foreach ($row as $value) {
                echo "<td><b>$value</b></td>";
            } 
            echo "</tr>";
        
        // Fetch contents
        $result = mysqli_query($con,
            "SELECT * FROM $sqlTable ORDER BY $orderColumn $orderDirection;"
        );
        $row = mysqli_fetch_row($result);

        // Insert all rows of contents
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
</body>
</html>