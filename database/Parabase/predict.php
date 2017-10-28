<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" >
<html lang="en">
<head>
<meta charset="UTF-8">
<META NAME="keywords" CONTENT="parabse, Parabase" />
<title>Parabase</title>
<link rel="stylesheet" type="text/css" href="css/header.css" media="screen" />
<link rel="stylesheet" type="text/css" href="css/google-fonts.css" media="screen" />
<link rel="stylesheet" type="text/css" href="css/footer.css" media="screen" />
<link rel="stylesheet" type="text/css" href="css/home.css" media="screen" />
<!--
<script type="text/javascript" src="js/utils.js"></script>
<script type="text/javascript" src="js/blast.js"></script>
<script type="text/javascript" src="js/remote_data_provider.js"></script>
<script type="text/javascript" src="js/home.js"></script>
-->
</head>
<body id="type-d">
<!--<div id="browsers_ajax"></div>-->
<div id="wrap">
            	
    <header id="page_header" role="banner">
        <div class="bg-gray header-div">
        <nav class="top-nav" id="navcontent" role="navigation">
            <a class="lf" href="http://2017.igem.org/Team:NCTU_Formosa"><img id="logo" alt="NCTU_Formosa" src="images/logo.png"></a>
            <span class="rf">            
            <ul id="blnav">
                <li  class="first active"><a href="http://web.it.nctu.edu.tw/~nctu_formosa/Parabase/" title="Parabase Home">Home</a></li>
                <li  class="recent "><a href="">Statistics</a></li>                
                <li  class="saved "><a href="https://www.facebook.com/NCTUFormosa/">Contact Us</a></li>
                <li  class="last documentation "><a href="help.html">Help</a></li>                
            </ul>
            </span>
        </nav>
        </div>                
        </header>
        <div id="content-wrap">
        <div id="content">
<?php
error_reporting(0);

function make_scorecard($file) {
        $temp_score = array();
        $count = 0;
        $i = 0;
        $handle = fopen($file, 'r');
        if ($handle) {
                while (($line = fgets($handle)) !== false) {
                        if ($count == 3) {
                                $temp_array1 = explode('[', $line);
                                $temp_array2 = explode(',', $temp_array1[1]);
                                foreach ($temp_array2 as $temp_value) {
                                        $temp_array3 = explode(']', $temp_value);
                                        $temp_num = $temp_array3[0];
                                        settype($temp_num, 'float');
                                        $temp_score[$i] = $temp_num;
                                        $i++;
                                }
                        }
                        $count++;
                }
                fclose($handle);
        }
        else {
                die("Unable to connect to the database, please reflash the webpage again.");
        }
        
        $scoring = array();
        $count = 0;
        $handle = fopen('dipep.jpg', 'r');
        if ($handle) {
                while (($line = fgets($handle)) !== false) {
                        $line = substr($line, 0, 2);
                        $scoring[$line] = $temp_score[$count];
                        $count++;
                }
                fclose($handle);
        }
        else {
                die("Unable to connect to the database, please reflash the webpage again.");
        }
        $sosco_key = array();
        $keys = array_keys($scoring);
        sort($keys);
        $i = 0;
        foreach ($keys as $key) {
                $sosco_key[$i] = $key;
                $i++;
        }
        return array($sosco_key, $scoring, $temp_score);       
}
function cuc_sc($sequence, $sosco_key, $scoring) {
        $gap = 0;
        $dipeptide_test = array();
        foreach ($sosco_key as $key) {
                $dipeptide_test[$key] = 0;
        }
        $i = 0;
        $condition = strlen($sequence) - ($gap + 1);
        while ($i < $condition) {
                $temp_aa = substr($sequence, $i, 1) . substr($sequence, $i + ($gap + 1), 1);
                $dipeptide_test[$temp_aa]++;
                $i++;
        }
        $g = 0.0;
        foreach ($sosco_key as $key) {
                $g_update = $scoring[$key] * $dipeptide_test[$key];
                settype($g_update, 'float');
                $g = $g + $g_update;
        }
        $score = $g / $condition;
        settype($score, 'float');
        return $score;        
}
function fasta_cleave($file_content) {
        $fasta_array = array();
        $temp = substr($file_content, strpos($file_content, '>'));
        $temp = trim($temp, "\n");
        $temp = explode('>', $temp);
        foreach ($temp as $sequence_name) {
                $sequence_name = rtrim($sequence_name, "\n");
                $sequence_name = explode("\n", $sequence_name);
                if (count($sequence_name) !== 2) {
                        continue;
                }
                $fasta_array[$sequence_name[0]] = $sequence_name[1];
        }
        return $fasta_array;
}
function cleaner($path) {
        foreach (glob ($path."*") as $file) {
                if (time() - filectime($file) > 86400) {
                        unlink($file);
                }
        }
}
function displayer($fasta_array, $sosco_key, $scoring, $html_section, $result_file, $html_section_error) {
        foreach (array_keys($fasta_array) as $sequence_name) {
                try {
                        $each_sequence = $fasta_array[$sequence_name];
                        $score = cuc_sc($each_sequence, $sosco_key, $scoring);
                        $display = sprintf($html_section, $sequence_name, $score);
                        $file_line = ">" . $sequence_name . "\n" . $score . "\n";
                        fwrite($result_file, $file_line);        
                        echo $display;
                }
                catch (Exception $e) {
                        $display = sprintf($html_section_error, $name);
                        $file_line = ">" . $sequence_name . "\n" . 0 . "\n";
                        fwrite($result_file, $file_line);
                        echo $display;
                }
        }
}

/*Clean old files in directory*/
cleaner("upload/");
cleaner("download/");

/*HTML*/
$html_section = '<h1>The score of the peptide <u>%s</u> is <u>%s</u>.</h1>';
$html_section_error = '<h1>The score of the peptide <u>%s</u> can not be calculated.</h1>';
$download_link = '<a download href="%s">Click here for download</a>';

$sc_array = make_scorecard('output_scorecard22.jpg');
$sosco_key = $sc_array[0];
$scoring = $sc_array[1];
$temp_score = $sc_array[2];
$sc_array = null;

$sequence = $_POST["Sequence"];

/*If there is input in textarea, ignore input in file*/
if ($sequence) {
        $entropy = uniqid($more_entropy = true);
        $filename_download = 'download/' . $entropy;
        
        $fasta_array = fasta_cleave($sequence);
        echo sprintf($download_link, $filename_download);
        
        $result_file = fopen($filename_download, 'w');
        displayer($fasta_array, $sosco_key, $scoring, $html_section, $result_file, $html_section_error);
        fclose($result_file);
        exit;
}

if ($_FILES['File']['error'] > 0) {
        die("Unable to catch your input file, please try it again.");
}
else {
        $entropy = uniqid($more_entropy = true);
        $filename_upload = 'upload/' . $entropy;
        $filename_download = 'download/' . $entropy;
        move_uploaded_file($_FILES['File']['tmp_name'], $filename_upload);
        
        $file = fopen($filename_upload, 'r') or die("Unable to catch your input file, please try it again.");
        $file_content = fread($file, filesize($filename_upload));
        $fasta_array = fasta_cleave($file_content);
        $file_content = null;
        fclose($file);
        echo sprintf($download_link, $filename_download);
        
        $result_file = fopen($filename_download, 'w');      
        displayer($fasta_array, $sosco_key, $scoring, $html_section, $result_file, $html_section_error);
        fclose($result_file);
}
?>
</div>
</body>
</html>