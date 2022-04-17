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
            Scrape Website Data
        </h2>
    </header>

    <?php include_once("nav.php");?>

    <main>

        <?php

            // TODO: GET ARGS (Site & Category)
            // echo "<form>";
            // $website = "???";
            // $category = "???";
            // echo "</form>";



            // EXECUTE SCRIPT
            // $cmd = "/var/www/script/scrape.py";
            // $cmd = "/var/www/script/scrape.py $website $category"; # Example with args
            // $cmd = "/usr/bin/tree"; # TESTING BUILTIN
            $cmd = "/var/www/script/TEST.py"; # TESTING PYTHON

            echo "<p>Running script \"$cmd\"...</p>";
            $output = shell_exec($cmd); # This might help force the command to continue?
            $output_clean = nl2br($output);
            echo "<p>Printing command output:<br><br>$output_clean</p>";
            

            
        ?>

    </main>
</body>