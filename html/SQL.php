<?php

    // TODO: Refactor "fetch & display" logic
        // 1. SELECT * FROM some_table;
        // 2. Store EVERYTHING in an array of dicts, one dict = one row
        // 3. Have a static whitelist of column names, per category
            // (The whitelist controls what is actually displayed in the HTML table)
        // 4. Display data in a table, but some some subtlety
            // Titles are hrefs to their stored URL
            // Add "$" to each price, etc.

    class SQL {
        // Static Vars
        // TODO: Move these details to a .txt file in ~/
        private $IP = "127.0.0.1";
        // private $IP = "10.1.1.160";
        private $USER = "scraper";
        private $PASS = "Password##123";
        private $DB = "PriceScraper";

        private $con;

        function __construct() {
            // Connect to SQL server
            $this->con = mysqli_connect($this->IP, $this->USER, $this->PASS);
            mysqli_select_db($this->con, $this->DB);
        }

        function getColumns($table) {

            // Fetch result
            $result = mysqli_query($this->con,
                "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '$table';"
            );

            // Define output structure

            // return

        }

        function getData($table) {

            // Fetch result
            $result = mysqli_query($this->con,
                "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '$table';"
            );

            // Define output structure

            // return

        }
    }
?>