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


try {
        $db = new PDO("sqlite:Parabase.db");
}
catch (Exception $e) {
        die("Unable to connect to the database, please reflash the webpage again.");
}

/*HTML*/
$html_section2 = '<h3><u>%s</u></h3>';
$html_section2_error = '<h1>Error!</h1>';
$pubmed = 'http://www.ncbi.nlm.nih.gov/pubmed/';

$goto = array(
        'Host'     => array(0 => 'host_pathogen', 1 => 'Pathogen'),
        'Pathogen' => array(0 => array(0 => 'host_pathogen', 1 => 'Host'), 1 => array(0 => 'only_validated_fungus', 1 => 'ParabaseID')),
        'ParabaseID'  => array(0 => 'only_validated_fungus', 1 => 'Pathogen', 2=> 'Sequence'),
        'Sequence' => array(0 => 'only_validated_fungus', 1 => 'ParabaseID', 2 => 'Sequence')
);

$select = $_GET["Select"];
$keyword = $_GET["Keyword"];
$direct = $goto[$select];
$column = $select;
if (! ($select and $keyword)) {
        die("Unable to catch your keyword, please try it again.");
}
function main_function($direct, $column, $keyword) {
        global $db;
        $command_cursor = sprintf("SELECT * FROM %s WHERE %s GLOB '*%s*'", $direct[0], $column, $keyword);
        $command_columns = sprintf("PRAGMA table_info(%s)", $direct[0]);
                                
        $cursor = $db->prepare($command_cursor);
        $cursor->execute();
        $columns = $db->prepare($command_columns);
        $columns->execute();
        $sensor = $db->prepare($command_cursor);
        $sensor->execute();
                
        $index = array();
        $i = 0;
        /*Wait for update*/
        foreach ($columns as $column_info) {
                if (in_array($direct[1], $column_info)) {
                        $index[$i] = $column_info;
                        $i++;    
                }
        }
        return array($cursor, $index, $sensor);
}
function updating($direct, $column, $keyword, $rows) {
        global $db;
        $command_cursor = sprintf("SELECT * FROM %s WHERE %s GLOB '*%s*'", $direct[0], $column, $keyword);
        $command_columns = sprintf("PRAGMA table_info(%s)", $direct[0]);
                                
        $cursor = $db->prepare($command_cursor);
        $cursor->execute();
        $columns = $db->prepare($command_columns);
        $columns->execute();
        $sensor = $db->prepare($command_cursor);
        $sensor->execute();
                
        $index = array();
        /*Wait for update*/
        for ($counter = 1; $counter <= $rows; $counter++) {        
                $i = 0;
                $inner_index = array();
                foreach ($columns as $column_info) {
                        if (in_array($direct[$counter], $column_info)) {
                                $inner_index[$i] = $column_info;
                                $i++;    
                        }
                }
                $index[$counter] = $inner_index;
        }
        return array($cursor, $index, $sensor);
}
function add_href($Select, $Keyword, $html_section2_content) {
        global $html_section2;
        $first_tag = '<a href="search.php?Select=%s&Keyword=%s">';
        $second_tag = '</a>';
        if (strpos($Keyword, '(') !== false) {
                $position = strpos($Keyword, '(');
                $Keyword = substr_replace($Keyword, '', $position);
        }
        $Keyword = trim($Keyword, " ");
        $Keyword = preg_replace('/ /', '+', $Keyword);
        $html_section2_content = trim($html_section2_content, " ");
        $output = sprintf($first_tag, $Select, $Keyword) . sprintf($html_section2, $html_section2_content) . $second_tag;
        return $output;
}

switch ($select) {
        case 'Host':
                echo "<h1>{$select}:{$keyword}</h1>";
                echo "<h2>{$direct[1]}</h2>";
                $cursor_index = main_function($direct, $column, $keyword);
                $cursor = $cursor_index[0];
                $index = $cursor_index[1];
                $sensor = $cursor_index[2];
                $cursor_index = null;
                $condition = $sensor->fetchAll();
                if ($condition) {
                        foreach ($cursor as $row) {
                                $display = add_href($direct[1], $row[$index[0][0]], $row[$index[0][0]]);
                                echo $display;
                        }
                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }
                break;
        case 'Pathogen':
                echo "<h1>{$select}:{$keyword}</h1>";
                foreach ($direct as $show) {
                        echo "<h2>{$show[1]}</h2>";
                        $cursor_index = main_function($show, $column, $keyword);
                        $cursor = $cursor_index[0];
                        $index = $cursor_index[1];
                        $sensor = $cursor_index[2];
                        $cursor_index = null;
                        $condition = $sensor->fetchAll();
                        
                        if ($condition) {
                                foreach ($cursor as $row) {
                                        $display = add_href($show[1], $row[$index[0][0]], $row[$index[0][0]]);
                                        echo $display;
                                }
                                echo '<hr>';
                        }
                }
                break;
        /*
        case 'Peptide':
                echo "<h1>{$select}:{$keyword}</h1>";
                echo "<h2>{$direct[1]}</h2>";             
                $c_row = 2;
                $cursor_index = updating($direct, $column, $keyword, $c_row);
                $cursor = $cursor_index[0];
                $index = $cursor_index[1];
                $sensor = $cursor_index[2];
                $cursor_index = null;
                $condition = $sensor->fetchAll();
                
                if ($condition) {
                        foreach ($cursor as $row) {
                                for ($i = 1; $i <= $c_row; $i++) {
                                        $pathogens = $row[$index[$i][0][0]];
                                        $pathogens = preg_replace('/;/', ',', $pathogens);
                                        $pathogens = explode(',', $pathogens);
                                        foreach ($pathogens as $pathogen) {
                                                if (! $pathogen) {
                                                        continue;
                                                }
                                                $display = add_href($direct[$i], $pathogen, $pathogen);
                                                echo $display;
                                        }
                                }
                                
                        }
                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }
                break;
        */
        case 'ParabaseID':
                echo "<h1>{$select}:{$keyword}</h1>";
                /*
                $command_cursor = sprintf("SELECT Peptide, Sequence, Title, Abstract FROM %s WHERE %s GLOB '*%s*'", $direct[0], $column, $keyword);
                */
                
                $command_cursor = sprintf("SELECT * FROM %s WHERE %s GLOB '*%s*'", 'only_validated_fungus', 'ParabaseID', $keyword);
                $command_columns = sprintf("PRAGMA table_info(%s)", 'only_validated_fungus');
                $cursor = $db->prepare($command_cursor);
                $cursor->execute();
                $columns = $db->prepare($command_columns);
                $columns->execute();
                $sensor = $db->prepare($command_cursor);
                $sensor->execute();
                
                $index = array();
                $i = 0;
                foreach ($columns as $column_info) {
                        if (in_array('Peptide', $column_info)) {
                                $index[$i] = $column_info;
                                $i++;    
                        }
                }
                $condition = $sensor->fetchAll();
                if ($condition) {
                        foreach ($cursor as $row) {
                                $display = $row[$index[0][0]];
                                echo '<h1>Peptide name:</h1>';
                                echo '<h2>' . $display . '</h2>';
                        }
                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }
                $command_cursor = sprintf("SELECT * FROM %s WHERE %s GLOB '*%s*'", 'only_validated_fungus', 'ParabaseID', $keyword);
                $command_columns = sprintf("PRAGMA table_info(%s)", 'only_validated_fungus');
                $cursor = $db->prepare($command_cursor);
                $cursor->execute();
                $columns = $db->prepare($command_columns);
                $columns->execute();
                $sensor = $db->prepare($command_cursor);
                $sensor->execute();
                
                $index = array();
                $i = 0;
                foreach ($columns as $column_info) {
                        if (in_array('Source', $column_info)) {
                                $index[$i] = $column_info;
                                $i++;    
                        }
                }
                $condition = $sensor->fetchAll();
                if ($condition) {
                        foreach ($cursor as $row) {
                                $display = $row[$index[0][0]];
                                echo '<h1>Source:</h1>';
                                echo '<h2>' . $display . '</h2>';
                        }
                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }
                
                $command_cursor = sprintf("SELECT * FROM %s WHERE %s GLOB '*%s*'", 'only_validated_fungus', 'ParabaseID', $keyword);
                $command_columns = sprintf("PRAGMA table_info(%s)", 'only_validated_fungus');
                $cursor = $db->prepare($command_cursor);
                $cursor->execute();
                $columns = $db->prepare($command_columns);
                $columns->execute();
                $sensor = $db->prepare($command_cursor);
                $sensor->execute();
                
                $index = array();
                $i = 0;
                foreach ($columns as $column_info) {
                        if (in_array('Sequence', $column_info)) {
                                $index[$i] = $column_info;
                                $i++;    
                        }
                }
                $condition = $sensor->fetchAll();
                if ($condition) {
                        foreach ($cursor as $row) {
                                $display = $row[$index[0][0]];
                                echo '<h1>Sequence:</h1>';
                                echo '<h2>' . $display . '</h2>';
                        }
                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }               
                /*-----------------------------------------------------*/
                echo "<h1>{$direct[1]}:</h1>";             
                $cursor_index = main_function($direct, $column, $keyword);
                $cursor = $cursor_index[0];
                $index = $cursor_index[1];
                $sensor = $cursor_index[2];
                $cursor_index = null;
                $condition = $sensor->fetchAll();
                
                if ($condition) {
                        foreach ($cursor as $row) {
                                $pathogens = $row[$index[0][0]];
                                $pathogens = preg_replace('/;/', ',', $pathogens);
                                $pathogens = explode(',', $pathogens);
                                foreach ($pathogens as $pathogen) {
                                        if (! $pathogen) {
                                                continue;
                                        }
                                        $display = add_href($direct[1], $pathogen, $pathogen);
                                        echo $display;
                                }
                                
                        }
                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }
                
                $command_cursor = sprintf("SELECT * FROM %s WHERE %s GLOB '*%s*'", 'only_validated_fungus', 'ParabaseID', $keyword);
                $command_columns = sprintf("PRAGMA table_info(%s)", 'only_validated_fungus');
                $cursor = $db->prepare($command_cursor);
                $cursor->execute();
                $columns = $db->prepare($command_columns);
                $columns->execute();
                $sensor = $db->prepare($command_cursor);
                $sensor->execute();
                
                $index = array();
                $i = 0;
                foreach ($columns as $column_info) {
                        if (in_array('Abstract', $column_info)) {
                                $index[$i] = $column_info;
                                $i++;    
                        }
                }
                $condition = $sensor->fetchAll();
                if ($condition) {
                        foreach ($cursor as $row) {
                                $display = $row[$index[0][0]];
                                echo '<h1>Paper Abstract:</h1>';
                                echo '<h3>' . $display . '</h3>';
                        }
                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }
                
                $command_cursor = sprintf("SELECT * FROM %s WHERE %s GLOB '*%s*'", 'only_validated_fungus', 'ParabaseID', $keyword);
                $command_columns = sprintf("PRAGMA table_info(%s)", 'only_validated_fungus');
                $cursor = $db->prepare($command_cursor);
                $cursor->execute();
                $columns = $db->prepare($command_columns);
                $columns->execute();
                $sensor = $db->prepare($command_cursor);
                $sensor->execute();
                
                $index = array();
                $i = 0;
                foreach ($columns as $column_info) {
                        if (in_array('PubMed', $column_info)) {
                                $index[$i] = $column_info;
                                $i++;    
                        }
                }
                $condition = $sensor->fetchAll();
                if ($condition) {
                        foreach ($cursor as $row) {
                                $display = $row[$index[0][0]];
                                $pubmed_href = $pubmed . $display;
                                echo "<a href='{$pubmed_href}'><h2>PubMed link</h2></a>";
                        }
                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }
                
                break;
        
        case 'Sequence':
                echo "<h1>{$direct[1]}</h1>";
                
                $cursor_index = main_function($direct, $column, $keyword);
                $cursor = $cursor_index[0];
                $index = $cursor_index[1];
                $sensor = $cursor_index[2];
                $cursor_index = null;
                $condition = $sensor->fetchAll();
                
                if ($condition) {
                        foreach ($cursor as $row) {
                                $pathogens = $row[$index[0][0]];
                                $pathogens = preg_replace('/;/', ',', $pathogens);
                                $pathogens = explode(',', $pathogens);
                                foreach ($pathogens as $pathogen) {
                                        if (! $pathogen) {
                                                continue;
                                        }
                                        $display = add_href($direct[1], $pathogen, $pathogen);
                                        echo $display;
                                }                              
                        }
                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }
                break;     
        default:
                $display = $html_section2_error;
                echo $display;
}
?>
</div>
</body>
</html>