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

            // GET ARGS (Site & Category)



            // EXECUTE SCRIPT
            // $cmd = "/var/www/script/scrape.py"; # Absolute
            // $cmd = "../script/scrape.py"; # Relative
            // $cmd = "/usr/bin/tree"; # TESTING
            $cmd = "/var/www/script/TEST.py"; # TESTING

            echo "<p>";
            echo "Running script \"$cmd\"<br>";
            $cmd_escaped = escapeshellcmd($cmd);
            $output = shell_exec($cmd_escaped);
            // echo (shell_exec($cmd_escaped)); # Still no linebreaks
            echo "</p>";

            echo "<p>";
            echo "Printing command output:<br>";
            echo $output;
            echo "</p>";

        ?>

    </main>
</body>