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
<link rel="stylesheet" type="text/css" href="css/form.css" />
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
      <li  class="recent "><a href="statistics.html">Statistics</a></li>                
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

try {
        $db = new PDO("sqlite:Parabase.db");
}
catch (Exception $e) {
        die("Unable to connect to the database, please reflash the webpage again.");
}

/*HTML*/
$html_section2 = '%s';
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
function is_short_name($name){
        if (false === ($rst = strpos($name, '.'))) {
                return false;
        }
        $condition = explode('.', $name);
        if (count($condition) == 2) {
                return true;
        }
        else {
                return false;
        }
}
function find_long_name($short_name) {
        global $db;
        $command_cursor = sprintf("SELECT * FROM bf WHERE short_name GLOB '*%s*'", $short_name);
        $command_columns = sprintf("PRAGMA table_info(bf)");
        
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
        $i = 0;
        $long_name_array = array();
        $condition = $sensor->fetchAll();
        if ($condition) {
                foreach ($cursor as $row) {
                        $long_name = $row[$index[0][0]];
                        $long_name_array[$i] = $long_name;
                        $i++;
                }
        }
        $num_of_name = $i;
        return array($long_name_array, $num_of_name);
}
/*
function sequence_writer($sequence) {
        
}
*/
function sequence_writer($sequence) {
        $length = strlen($sequence);
        $sequence = '1| ' . $sequence . ' |' . $length;
        return $sequence;
}
function target_writer($targets) {
        $output = '';
        foreach ($targets as $target) {
                $output = $output . '- ' . $target . '<br>';
        }
        return $output;
}
function evidence_writer($title, $author, $abstract, $pubmed_id) {
        $title_line = '<div style="margin-bottom:5pt;font-weight:bolder;font-style:italic;">' . $title . '<br></div>';
        $author_line = '- ' . $author . '<br>';
        $abstract_line = '<div style="margin-bottom:5pt;">' . $abstract . '<br></div>';
        $linkout = '<b>LinkOut: [</b>Pmid: ' . '<a href="http://www.ncbi.nlm.nih.gov/pubmed/' . $pubmed_id . '">' . $pubmed_id . '</a><b>]</b>';
        $output = $title_line . $author_line . $abstract_line . $linkout;
        return $output;         
}


switch ($select) {
        case 'Host':
                $table_html = '
                <table class="layout display responsive-table">
                    <thead>
                        <tr>
                            <th>Host Name</th>
                            <th>Domain Type</th>
                       </tr>
                    </thead>
                    <tbody>';
                $tbody_html = '<tr><td class="organisationnumber"><p class="word1" style="line-height:0;">%s</p></td><td class="organisationname">%s</td></tr>';
                echo "<h1>Host Query: {$keyword}</h1>";
                echo "<h2>Affect Pathogen</h2>";
                echo $table_html;
                $cursor_index = main_function($direct, $column, $keyword);
                $cursor = $cursor_index[0];
                $index = $cursor_index[1];
                $sensor = $cursor_index[2];
                $cursor_index = null;
                $condition = $sensor->fetchAll();
                if ($condition) {
                        foreach ($cursor as $row) {
                                $play = $row[$index[0][0]];
                                $play = rtrim($play, ")");
                                $play = explode("(", $play);
                                $name = $play[0];
                                $type = $play[1];
                                
                                
                                $display1 = add_href($direct[1], $name, $name);
                                $display = sprintf($tbody_html, $display1, $type);
                                echo $display;
                        }
                        echo '</tobdy>';
                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }
                break;
        case 'Pathogen':
                /*-----------------UPDATING---------------*/
                if (is_short_name($keyword)) {
                        $name_num = find_long_name($keyword);
                        $name_array = $name_num[0];
                        $num_of_name = $name_num[1];
                        if ($num_of_name == 1) {
                                $keyword = $name_array[0];
                        }
                        elseif ($num_of_name > 1) {
                                echo 'There is multiple pathogens fit with this query: ';
                                echo '<br>';
                                foreach ($name_array as $name) {
                                        echo $name . '<br>';
                                }
                                die();
                        }
                }
                                
                
                echo "<h1>Pathogen Query: {$keyword}</h1>";
                /*
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
                */
                
                /*------------Host----------------*/
                $table_html = '
                <table class="layout display responsive-table">
                    <thead>
                        <tr>
                            <th>Host Name</th>
                            <th>Related Common Name</th>
                       </tr>
                    </thead>
                    <tbody>';
                echo $table_html;
                $tbody_html = '<tr><td class="organisationnumber"><p class="word1" style="line-height:0;">%s</p></td><td class="organisationname">%s</td></tr>';
                $show = $direct[0];
                echo "<h2>Host Species</h2>";
                $cursor_index = main_function($show, $column, $keyword);
                $cursor = $cursor_index[0];
                $index = $cursor_index[1];
                $sensor = $cursor_index[2];
                $cursor_index = null;
                $condition = $sensor->fetchAll();
                        
                if ($condition) {
                        foreach ($cursor as $row) {
                                $play = $row[$index[0][0]];
                                $play = rtrim($play, ")");
                                $play = explode(" (", $play);
                                $name = $play[0];
                                $related_name = ltrim($play[1], 'related:');
                                $display1 = add_href($show[1], $name, $name/*$row[$index[0][0]], $row[$index[0][0]]*/);
                                $display = sprintf($tbody_html, $display1, $related_name);
                                echo $display;
                                
                                
                        }
                        echo '</tbody>';
                        
                }
                /*<!----------Pathogen---------->*/          
                $table_html = '
                <table class="layout display responsive-table">
                    <thead>
                        <tr>
                            <th>Parabase ID</th>
                            <th>Peptide Name</th>
                            <th>Source</th>
                       </tr>
                    </thead>
                    <tbody>';
                $tbody_html = '<tr><td class="organisationnumber"><p class="word1" style="line-height:0;">%s</p></td><td class="organisationname">%s</td><td class="organisationname">%s</td></tr>';
                $id_link = '<a href="search.php?Select=ParabaseID&Keyword=%s">%s</a>';
                echo $table_html;
                $show = $direct[1];
                echo '<hr>';
                echo "<h2>Antifungal peptides</h2>";
                $command_cursor = sprintf("SELECT * FROM %s WHERE %s GLOB '*%s*'", $show[0], $column, $keyword);
                $command_columns = sprintf("PRAGMA table_info(%s)", $show[0]);
                
                
                $cursor = $db->prepare($command_cursor);
                $cursor->execute();
                $columns = $db->prepare($command_columns);
                $columns->execute();
                $sensor = $db->prepare($command_cursor);
                $sensor->execute();
                
                $index = array();
                $index2 = array();
                $index3 = array();
                $i = 0;
                $n = 0;
                $x = 0;
                foreach ($columns as $column_info) {
                        if (in_array('ParabaseID', $column_info)) {
                                $index[$i] = $column_info;
                                $i++;    
                        }
                        elseif (in_array('Peptide', $column_info)) {
                                $index1[$n] = $column_info;
                                $n++;    
                        }
                        elseif (in_array('Source', $column_info)) {
                                $index2[$x] = $column_info;
                                $x++;    
                        }
                }
                $condition = $sensor->fetchAll();
                if ($condition) {
                        foreach ($cursor as $row) {
                                $display1 = $row[$index[0][0]];
                                
                                $display1 = sprintf($id_link, $display1, $display1);
                                $display2 = $row[$index1[0][0]];
                                $display3 = $row[$index2[0][0]];
                                $display = sprintf($tbody_html, $display1, $display2, $display3);
                                echo $display;
                                
                        }
                        echo '</tbody>';
                }
                else {
                        $display = $html_section2_error;
                        die($display);
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
                echo "<h2>{$select}:{$keyword}</h2>";
                $table_html = "
<div id='blueDream'>
    <table>
    <caption>Peptide Information</caption>
                            
    <thead>
    </thead> 
    <tfoot>
    </tfoot>
    <tbody>
    <tr>
        <th>Peptide name</th>
        <td>%s</td>
    </tr>
    <tr>
        <th>Source</th>
        <td>%s</td>
    </tr>
    <tr>
        <th>Sequence</th>
        <td>%s</td>
    </tr>
    <tr>
        <th>Target Pathogen</th>
        <td>%s</td>
    </tr>
    <tr>
        <th>Evidence</th>
        <td>%s</td>
    </tr>
    </tbody>
    </table>
</div>
";              
                /*
                $command_cursor = sprintf("SELECT Peptide, Sequence, Title, Abstract FROM %s WHERE %s GLOB '*%s*'", $direct[0], $column, $keyword);
                */
                
                
                $peptide_info = array();
                $command_cursor = sprintf("SELECT * FROM %s WHERE %s = '%s'", 'only_validated_fungus', 'ParabaseID', $keyword);
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
                                $peptide_info['name'] = $display;
                        }
                }
                else {
                        $display = $html_section2_error;
                        die($display);
                }
                $command_cursor = sprintf("SELECT * FROM %s WHERE %s = '%s'", 'only_validated_fungus', 'ParabaseID', $keyword);
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
                                $peptide_info['source'] = $display;
                        }
                }
                else {
                        $display = $html_section2_error;
                }
                
                $command_cursor = sprintf("SELECT * FROM %s WHERE %s = '%s'", 'only_validated_fungus', 'ParabaseID', $keyword);
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
                                $peptide_info['sequence'] = $display;
                        }
                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }               
                /*-----------------------------------------------------*/             
                $cursor_index = main_function($direct, $column, $keyword);
                $cursor = $cursor_index[0];
                $index = $cursor_index[1];
                $sensor = $cursor_index[2];
                $cursor_index = null;
                $condition = $sensor->fetchAll();
                $target_array = array();
                $t = 0;
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
                                        $target_array[$t] = $display;
                                        $t++;
                                }
                                
                        }
                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }
                
                $command_cursor = sprintf("SELECT * FROM %s WHERE %s = '%s'", 'only_validated_fungus', 'ParabaseID', $keyword);
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
                        if (in_array('Title', $column_info)) {
                                $index[$i] = $column_info;
                                $i++;    
                        }
                }
                $condition = $sensor->fetchAll();
                if ($condition) {
                        foreach ($cursor as $row) {
                                $display = $row[$index[0][0]];
                                $peptide_info['title'] = $display;
                        }
                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }
                $command_cursor = sprintf("SELECT * FROM %s WHERE %s = '%s'", 'only_validated_fungus', 'ParabaseID', $keyword);
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
                        if (in_array('authors', $column_info)) {
                                $index[$i] = $column_info;
                                $i++;    
                        }
                }
                $condition = $sensor->fetchAll();
                if ($condition) {
                        foreach ($cursor as $row) {
                                $display = $row[$index[0][0]];
                                $peptide_info['author'] = $display;
                        }
                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }
                $command_cursor = sprintf("SELECT * FROM %s WHERE %s = '%s'", 'only_validated_fungus', 'ParabaseID', $keyword);
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
                                $peptide_info['abstract'] = $display;
                        }
                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }
                
                $command_cursor = sprintf("SELECT * FROM %s WHERE %s = '%s'", 'only_validated_fungus', 'ParabaseID', $keyword);
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
                                $peptide_info['pubmed_id'] = $display;
                        }
                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }
                /*evidence_writer($title, $author, $abstract, $pubmed_id)*/
                $title = $peptide_info['title'];
                $author = $peptide_info['author'];
                $abstract = $peptide_info['abstract'];
                $pubmed_id = $peptide_info['pubmed_id'];
                
                $peptide_name = '<b>' . $peptide_info['name'] . '</b>';
                $source = $peptide_info['source'];
                $sequence = sequence_writer($peptide_info['sequence']);
                $evidence = evidence_writer($title, $author, $abstract, $pubmed_id);
                $targets = target_writer($target_array);
                $output = sprintf($table_html, $peptide_name, $source, $sequence, $targets, $evidence);
                echo $output;                
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