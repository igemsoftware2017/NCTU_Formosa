
<?php
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
        //Wait for update
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
        function find_all_name($table, $name) {
        global $db;
        $command_cursor = sprintf("SELECT * FROM bf WHERE short_name GLOB '*%s*'", $name);
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
        function peptides_writer($parabase_id, $peptide_name, $source) {
                $out_put = '';
                $num = count($parabase_id);
                for ($i=1; $i=$num; $i++) {
                        $each_line = '- ' . $parabase_id[$i] . ' | ' . $peptide_name[$i] . ' | ' . $source[$i] . '<br>';
                        $out_put = $out_put . $each_line; 
                }  
                return $out_put;
        }


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
?>