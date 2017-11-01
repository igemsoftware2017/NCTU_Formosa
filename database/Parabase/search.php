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
    <a class="lf" href="http://web.it.nctu.edu.tw/~nctu_formosa/Parabase/"><img id="logo" alt="NCTU_Formosa" src="images/logo.png"></a>
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
set_time_limit(900);
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
if (strlen($keyword) < 2) {
        die("<br><br>The query is too short, please try it again. <a href='search.html'><b>GoBack</b>");
}

function main_function($direct, $column, $keyword) {
        global $db;
        $ya = '%' . $keyword . '%';
        $command_cursor = sprintf("SELECT * FROM %s WHERE %s LIKE '%s'", $direct[0], $column, $ya/*$keyword*/);
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
        $ya = '%' . $keyword . '%';
        $command_cursor = sprintf("SELECT * FROM %s WHERE %s LIKE '%s'", $direct[0], $column, $ya/*$keyword*/);
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
        $pos = strpos($Keyword, ' ');
        if ($pos !== false) {
        $Keyword = substr_replace($Keyword, '+', $pos, 1);        
        }
        $Keyword = explode(' ', $Keyword);
        $Keyword = $Keyword[0];
        $html_section2_content = trim($html_section2_content, " ");
        $output = sprintf($first_tag, $Select, $Keyword) . sprintf($html_section2, $html_section2_content) . $second_tag;
        return $output;
}
function is_short_name($name){
        if (false === ($rst = strpos($name, '.'))) {
                return false;
        }
        $condition = explode('.', $name);
        if (count($condition[0]) == 1) {
                return true;
        }
        else {
                return false;
        }
}
function find_long_name($name, $table) {
        global $db;
        $ya = '%' . $name . '%';
        $command_cursor = sprintf("SELECT * FROM bf WHERE %s LIKE '%s'",$table , $ya/*$name*/);
        $command_columns = sprintf("PRAGMA table_info(bf)");
        
        $cursor = $db->prepare($command_cursor);
        $cursor->execute();
        $columns = $db->prepare($command_columns);
        $columns->execute();
        $sensor = $db->prepare($command_cursor);
        $sensor->execute();
        
        $index1 = array();
        $index2 = array();
        $i = 0;
        $u = 0;
        /*Wait for update*/
        foreach ($columns as $column_info) {
                if (in_array('name', $column_info)) {
                        $index1[$i] = $column_info;
                        $i++;    
                }
                elseif (in_array('type', $column_info)) {
                        $index2[$u] = $column_info;
                        $u++;
                }
        }
        $i = 0;
        $long_name_array = array();
        $type_array = array();
        $condition = $sensor->fetchAll();
        if ($condition) {
                foreach ($cursor as $row) {
                        $long_name = $row[$index1[0][0]];
                        $type = $row[$index2[0][0]];
                        $type_array[$i] = $type;
                        $long_name_array[$i] = $long_name;
                        $i++;
                }
        }
        $num_of_name = $i;
        return array($long_name_array, $type_array);
}
function find_long_name2($name, $table) {
        global $db;
        $ya = '%' . $name . '%';
        $command_cursor = sprintf("SELECT * FROM host_pathogen WHERE %s LIKE '%s'",$table , $ya/*$name*/);
        $command_columns = sprintf("PRAGMA table_info(host_pathogen)");
        
        $cursor = $db->prepare($command_cursor);
        $cursor->execute();
        $columns = $db->prepare($command_columns);
        $columns->execute();
        $sensor = $db->prepare($command_cursor);
        $sensor->execute();
        
        $index1 = array();
        $index2 = array();
        $i = 0;
        $u = 0;
        /*Wait for update*/
        foreach ($columns as $column_info) {
                if (in_array('Host', $column_info)) {
                        $index1[$i] = $column_info;
                        $i++;    
                }
                
        }
        $i = 0;
        $long_name_array = array();
        $condition = $sensor->fetchAll();
        if ($condition) {
                foreach ($cursor as $row) {
                        $long_name = $row[$index1[0][0]];

                        $long_name_array[$long_name] = 0;
                        $i++;
                }
        }
        return $long_name_array;
}
function sequence_writer($sequence) {
        $length = strlen($sequence);
        $sequence = '1| ' . $sequence . ' |' . $length;
        return $sequence;
}
function target_writer($targets) {
        $output = 'Target pathogen: <br>';
        foreach ($targets as $target) {
                $output = $output . '- ' . $target . '<br>';
        }
        return $output;
}
function evidence_writer($title, $author, $abstract, $pubmed_id) {
        $title_line = '<div style="margin-bottom:5pt;font-weight:bolder;font-style:italic;">' . $title . '<br></div>';
        $author_line = '- ' . $author . '<br>';
        $abstract_line = '<div style="margin-bottom:5pt;"><br>' . $abstract . '<br></div>';
        $linkout = '<b>LinkOut: [</b>Pmid: ' . '<a href="http://www.ncbi.nlm.nih.gov/pubmed/' . $pubmed_id . '"' .'target="_blank">' . $pubmed_id . '</a><b>]</b>';
        $output = 'Evidence: <br>' . $title_line . $author_line . $abstract_line . $linkout;
        return $output;         
}
function peptides_writer($cursor, $id_link, $index, $index1, $index2) {
        $out_put = '';
        foreach ($cursor as $row) {
                $display1 = $row[$index[0][0]];
                                
                $display1 = sprintf($id_link, $display1, $display1);
                $display2 = $row[$index1[0][0]];
                $display3 = $row[$index2[0][0]];
                $display = '- ' . $display1 . ' | ' . $display2 . ' | ' . $display3 . '<br>';
                $out_put = $put_put . $display;
        return $out_put;  
        
        }      
}

switch ($select) {
        case 'Host':
                $name_array = find_long_name2($keyword, 'Host');
                $name_array = array_keys($name_array);
                $sj = $keyword;
                $total_num = count($name_array);
                $result_count = 0;
                $big_out = '';
                
                for ($c=0; $c < $total_num; $c++) {
                        $temp_i = $name_array[$c];
                        $temp_i = rtrim($temp_i, ')');
                        $temp_li = explode(' (', $temp_i);
                        $keyword = $temp_li[0];
                        $common_name = $temp_li[1];
                        $common_name = ltrim($common_name, 'related:');
                        $wiki = 'https://en.wikipedia.org/wiki/' . str_replace(' ', '_', $keyword);

                        $host_name = '<i><b>' . $keyword . '</b></i>';
                        $table_html = "<div id='blueDream'>
                                       <table>
                                       <caption>
                                       Host Information
                                       </caption>
                            
                                       <thead>
                                       </thead>
                
                                       <tfoot>
                                       </tfoot>
                            
                                       <tbody>
                                         <tr>
                                         <th>Host name</th>
                                         <td>%s</td>
                                         </tr>
                                         <tr>
                                         <th>Common name</th>
                                         <td>%s</td>
                                         </tr>
                                         <th>Discription</th>
                                         <td>%s</td>
                                        </tr>
                                <tr>
                                    <th>Pathogens</th>
                                    <td>%s</td>
                                </tr>
                                                                  
                            </tbody>
                          </table>
                        </div>";    



                        $cursor_index = main_function($direct, $column, $keyword);
                        $cursor = $cursor_index[0];
                        $index = $cursor_index[1];
                        $sensor = $cursor_index[2];
                        $cursor_index = null;
                        $condition = $sensor->fetchAll();
                        $pathogen_line = 'Pathogens: .<br>';
                        if ($condition) {
                                foreach ($cursor as $row) {
                                        $play = $row[$index[0][0]];
                                        $play = rtrim($play, ")");
                                        $play = explode("(", $play);
                                        $name = $play[0];
                                        $type = $play[1];
                                        $display1 = add_href($direct[1], $name, $name);
                                        $pathogen_line = $pathogen_line . '- ' . '<i><b>' . $display1 . '&nbsp;</b></i>' . '[' . $type . ']' . '<br>';
                                }
                        }
                        $wiki = 'https://en.wikipedia.org/wiki/' . str_replace(' ', '_', $keyword);
                        $wiki_output = '<i>' . $keyword . '</i>' . ' <b>LinkOut: [ </b>' .sprintf('<a href="%s" target="_blank">', $wiki) . 'Wikipedia' . '</a>' . '<b> ]</b>' ;
                        $out_line = sprintf($table_html, $host_name, $common_name, $wiki_output,$pathogen_line);
                        $big_out = $big_out . $out_line. '<br><br>';
                        $result_count++;
                /*
                else {
                        $display = $html_section2_error;
                        echo $display;
                }
                */
                
                }
                echo "<h2>Host Query: {$sj}" . '&nbsp;&nbsp;&nbsp;&nbsp;' . '<' . $result_count . ' results>' . '</h2>';
                echo $big_out;
                break;
        case 'Pathogen':
                /*-----------------UPDATING---------------*/
                if (is_short_name($keyword)) {
                        $name_num = find_long_name($keyword, 'short_name');
                        $name_array = $name_num[0];
                        $type_array = $name_num[1];
                }
                else {
                        $name_num = find_long_name($keyword, 'name');
                        $name_array = $name_num[0];
                        $type_array = $name_num[1];
                }
                $total_num = count($name_array);
                
                
                $result_count = 0;
                $big_out = '';
                $sj = $keyword;
                //echo "<h2>Pathogen Query: {$sj}" . '&nbsp;&nbsp;&nbsp;&nbsp;' . '<' . $total_num . ' results>' . '</h2>';
                for ($c=0; $c < $total_num; $c++) {
                //foreach ($name_array as $keyword){
                        $keyword = $name_array[$c];
                        $type = $type_array[$c];
                        $pathogen_name = '<i><b>' . $keyword . '</b></i>';
                        //echo $keyword;
                
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
                        $table_html = "
                        <div id='blueDream'>
                        <table>
                        <caption>Pathogen Information</caption>                       
                        <thead>
                        </thead> 
                        <tfoot>
                        </tfoot>
                        <tbody>
                        <tr>
                          <th>Pathogen name</th>
                          <td>%s</td>
                        </tr>
                        <tr>
                          <th>Pathogen type</th>
                          <td>%s</td>
                        </tr>
                        <tr>
                          <th>Discription</th>
                          <td>%s</td>
                        </tr>
                        <tr>
                          <th>Host species</th>
                          <td>%s</td>
                        </tr>
                        <tr>
                          <th>Target peptides</th>
                          <td>%s</td>
                        </tr>
                        </tbody>
                        </table>
                        </div>
                        ";
                        //echo $table_html;
                        //$tbody_html = '<tr><td class="organisationnumber"><p class="word1" style="line-height:0;">%s</p></td><td class="organisationname">%s</td></tr>';
                        $show = $direct[0];
                        //echo "<h2>Host Species</h2>";
                        $cursor_index = main_function($show, $column, $keyword);
                        $cursor = $cursor_index[0];
                        $index = $cursor_index[1];
                        $sensor = $cursor_index[2];
                        $cursor_index = null;
                        $condition = $sensor->fetchAll();
                        $host = array();
                        $h = 0;
                        if ($condition) {
                                foreach ($cursor as $row) {
                                        $play = $row[$index[0][0]];
                                        $play = rtrim($play, ")");
                                        $play = explode(" (", $play);
                                        $name = $play[0];
                                        $related_name = ltrim($play[1], 'related:');
                                        $display1 = add_href($show[1], $name, $name/*$row[$index[0][0]], $row[$index[0][0]]*/);
                                        //$display = sprintf($tbody_html, $display1, $related_name);
                                        $host[$h] = array($display1, $related_name);
                                        $h ++;     
                                }
                                //echo '</tbody>';
                        }
                
                /*<!----------Pathogen---------->*/          
                /*
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
                        */
                        //$tbody_html = '<tr><td class="organisationnumber"><p class="word1" style="line-height:0;">%s</p></td><td class="organisationname">%s</td><td class="organisationname">%s</td></tr>';
                        $id_link = '<a href="search.php?Select=ParabaseID&Keyword=%s">%s</a>';
                
                        $show = $direct[1];
                        //echo '<hr>';
                        //echo "<h2>Antifungal peptides</h2>";
                        $ya = '%' . $keyword . '%';
                        $command_cursor = sprintf("SELECT * FROM %s WHERE %s LIKE '%s'", $show[0], $column, $ya/*$keyword*/);
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
                                $out = 'Target peptides: <br>';
                                foreach ($cursor as $row) {
                                        $display1 = $row[$index[0][0]];
                                
                                        $display1 = sprintf($id_link, $display1, $display1);
                                        $display2 = $row[$index1[0][0]];
                                        $display3 = $row[$index2[0][0]];
                                        if (strpos($display3, '[') !== false) {
                                                $display3 = '<i>' . substr_replace($display3, '', strpos($display3, '[')) . '</i>' . substr($display3, strpos($display3, '['));
                                        }
                                        else {
                                                $display3 = '<i>' . $display3 . '</i>';
                                        }
                                
                                        $out = $out . '- ' . $display1 . ' | ' . '<b>' . $display2 . '</b>' . ' | ' . $display3 . '<br>';                       
                                }
                        
                        
                                $target_peptide_lines = $out;
                        }
                        else {
                                $display = $html_section2_error;
                                //die($display);
                                continue;
                        }
                        $host_line = 'Host species: <br>';
                        foreach ($host as $hos) {
                                $host_line = $host_line . '- ' . '<i><b>' . $hos[0] . ' '. '</b></i>';
                                if ($hos[1] !== '') {
                                        $hos[1] = trim($hos[1], ' ');
                                        $host_line = $host_line . '[' . $hos[1] . ']' . '<br>';        
                                }
                                else {
                                        $host_line = $host_line . '<br>';
                                }
                        }
                        $wiki = 'https://en.wikipedia.org/wiki/' . str_replace(' ', '_', $keyword);
                        $wiki_output = '<i>' . $keyword . '</i>' . ' <b>LinkOut: [ </b>' .sprintf('<a href="%s" target="_blank">', $wiki) . 'Wikipedia' . '</a>' . '<b> ]</b>' ;
                        $displayer = sprintf($table_html, $pathogen_name, $type, $wiki_output, $host_line, $out);
                        //echo $displayer;
                        $result_count++;
                        //echo '<br><br>';
                        $big_out = $big_out . $displayer . '<br><br>';     
                }
                echo "<h2>Pathogen Query: {$sj}" . '&nbsp;&nbsp;&nbsp;&nbsp;' . '<' . $result_count . ' results>' . '</h2>';
                echo $big_out;
                break;                
        case 'ParabaseID':
                $keyword = ucwords($keyword);
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
                $table_html = "<div id='blueDream'>
                          <table>
                            <caption>
                              Sequence Information
                            </caption>
                            
                            <thead>
                            </thead>
                
                            <tfoot>
                            </tfoot>
                            
                            <tbody>
                                <tr>
                                  
                                    <td>%s</td>
                                </tr>
                                                            
                            </tbody>
                          </table>
                        </div>";
                
                $id_link = '<a href="search.php?Select=ParabaseID&Keyword=%s">%s</a>';
                $result_count = 0;
                $sequence_line = 'Sequences: <br>';

                $ya = '%' . $keyword . '%';
                $command_cursor = sprintf("SELECT * FROM %s WHERE %s LIKE '%s'", 'only_validated_fungus', 'Sequence', $ya/*$keyword*/);
                $command_columns = sprintf("PRAGMA table_info(%s)", 'only_validated_fungus');
                
                
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
                        $out = 'Sequences: <br>';
                        foreach ($cursor as $row) {
                                $display1 = $row[$index[0][0]];
                                
                                $display1 = sprintf($id_link, $display1, $display1);
                                $display2 = $row[$index1[0][0]];
                                $display3 = $row[$index2[0][0]];
                                if (strpos($display3, '[') !== false) {
                                        $display3 = '<i>' . substr_replace($display3, '', strpos($display3, '[')) . '</i>' . substr($display3, strpos($display3, '['));
                                }
                                else {
                                        $display3 = '<i>' . $display3 . '</i>';
                                }
                                
                                $out = $out . '- ' . $display1 . ' | ' . '<b>' . $display2 . '</b>' . ' | ' . $display3 . '<br>';
                                $result_count++;                       
                        }
                        
                        
                        $target_peptide_lines = $out;
                }




                /*
                if ($condition) {
                        foreach ($cursor as $row) {
                                $pathogens = $row[$index[0][0]];
                                $pathogens = preg_replace('/;/', ',', $pathogens);
                                $pathogens = explode(',', $pathogens);
                                foreach ($pathogens as $pathogen) {
                                        if (! $pathogen) {
                                                continue;
                                        }
                                        $display = '<a href="search.php?Select=ParabaseID&Keyword=%s">';
                                        $line = sprintf($display, $pathogen) . $pathogen . '<a>'; 

                                        
                                        $sequence_line = $sequence_line . $line . ' | ' . '<br>';
                                        $result_count++;                              
                                }                              
                        }

                }
                else {
                        $display = $html_section2_error;
                        echo $display;
                }
                */
                echo "<h2>Sequence Query: {$keyword}" . '&nbsp;&nbsp;&nbsp;&nbsp;<' . $result_count . ' results><h2>';
                echo sprintf($table_html, $target_peptide_lines);
                break;
        default:
                $display = $html_section2_error;
                echo $display;
}
?>
</div>
</body>
</html>