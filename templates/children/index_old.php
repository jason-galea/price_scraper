<!DOCTYPE html>
<html lang="en">
<head>
    <?php include_once("templates/meta.php");?>
    
    <title>Price Scraper</title>
</head>
<body>
    <section class="section">
        <div class="container">
            <h2 class="title">
                Welcome to Price Scraper (TM)!
            </h2>

            <?php include_once("templates/nav.php");?>

            <p class="subtitle">
                This website will scrape and display the price and specs of computer hardware.
                It specifically focuses on Australian computer parts retailers.
            </p>

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

            ?>
        </div>
    </section>
</body>