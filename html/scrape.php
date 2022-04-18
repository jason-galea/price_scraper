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
            Scrape Data
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


        // VARS
        $cmd = "/var/www/script/scrape.py";
        // $cmd = "/var/www/script/scrape.py $website $category"; # Example with args
        // $cmd = "/usr/bin/tree"; # TESTING BUILTIN
        // $cmd = "/var/www/script/TEST.py"; # TESTING PYTHON


        // EXECUTE SCRIPT (v1)
        // echo "<p>Running script \"$cmd\"...</p>";
        // $output = shell_exec($cmd); # This might help force the command to continue?
        // $output_clean = nl2br($output);
        // echo "<p>Printing command output:<br><br>$output_clean</p>";


        // EXECUTE SCRIPT (v2)
        $temp_file = "/var/www/html/scrape_output.txt";
        // TEMP FILE
        // echo "<p>Removing temp file \"$temp_file\"...</p>";
        // if (file_exists($temp_file)) {
        //     unlink($temp_file);
        // }
        // echo "<p>Creating temp file \"$temp_file\"...</p>";
        // if (! file_exists($temp_file)) {
        //     file_put_contents($temp_file, "test 1");
        // }

        // START SCRIPT IN BACKGROUND
        echo "<p>Starting script \"$cmd\"...</p>";
        // https://stackoverflow.com/questions/45953/php-execute-a-background-process
        // system("echo 'test 2' > $temp_file"); // WORKS
        // system("echo 'test 3' > $temp_file 2>&1 &"); // WORKS
        // system("$cmd > $temp_file 2>&1 &"); // DOESN'T WORK!
        shell_exec("$cmd >> $temp_file 2>&1 &"); // WORKS (With sleep)

        for ($i = 0; $i <= 15; $i++) {
            sleep(1);
            echo "Script has been running for $i seconds...<br>";
            flush();
            ob_flush();

            // - Check if temp file exists:
            //     - Delete file
            //     - Print contents
            //     - End loop
            if (file_exists($temp_file) and (file_get_contents($temp_file))) {
                echo "<br>Temp file found! Printing output:<br>";
                echo nl2br(file_get_contents($temp_file));
                echo "<br>";

                // unlink($temp_file);

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