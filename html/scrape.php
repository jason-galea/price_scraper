<!DOCTYPE html>
<html lang="en">
<head>
    <?php include_once("templates/meta.php");?>
    
    <title>Price Scraper</title>
</head>
<body>
    <header>
        <h2>
            Scrape Data
        </h2>
    </header>

    <?php include_once("templates/nav.php");?>

    <main>

        <?php

        // PRINT & PROCESS FORM
        include_once("templates/form_website_category.php");


        // VARS
        // $cmd = "/var/www/script/scrape.py";
        $cmd = "/var/www/script/scrape.py $website $category"; # Example with args
        // $cmd = "/usr/bin/tree"; # Short test
        // $cmd = "/usr/bin/sleep 5"; # Long test
        $temp_file = "/var/www/html/scrape_output.txt";



        // PREPARE
        if (file_exists($temp_file)) {
        echo "<p>Removing temp file \"$temp_file\"...</p>";
            unlink($temp_file);
        }

        // EXECUTE
        echo "<p>Starting script \"$cmd\"...</p>";
        shell_exec("$cmd > $temp_file 2>&1 &"); // BACKGROUND

        // WAIT
        for ($i = 0; $i <= 15; $i++) {
            sleep(1);
            echo "Script has been running for $i seconds...<br>";
            flush();
            ob_flush();

            // PRINT WHEN COMPLETE
            if (file_exists($temp_file) and (file_get_contents($temp_file))) {
                echo "<br>Found temp file \"$temp_file\"<br>";
                echo nl2br(file_get_contents($temp_file));
                echo "<br>";

                echo "<br>Deleting temp file \"$temp_file\"<br>";
                unlink($temp_file);

                break;
            }

            // // DEBUG
            // echo $temp_file."<br>";
            // echo nl2br(file_get_contents($temp_file));
            // // $f = fopen($temp_file, "r");
            // // while(! feof($f)) {
            // //     $line = fgets($f);
            // //     echo $f. "<br>";
            // // }

        }
        
        ?>

    </main>
</body>