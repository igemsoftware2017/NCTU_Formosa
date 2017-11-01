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
<script src="http://code.jquery.com/jquery-latest.min.js"></script>
<script>
$(function(){
    var len = 50; 
    $(".word1").each(function(i){
        if($(this).text().length>len){
            $(this).attr("title",$(this).text());
            var text=$(this).text().substring(0,len-1)+"...";
            $(this).text(text);
        }
    });
});
</script>
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
        <style type="text/css">
#container{
width:1500px;
height:20px;
display:-moz-box;
display:-webkit-box;
display:-ms-flexbox;
display:-webkit-flex;
display:flex;
-moz-box-orient:horizontal;
-webkit-box-orient:horizontal;
position:relative;
top:20px;


}



#item2{

width:760px;
height:20px;
background: -webkit-linear-gradient(left,#0000FF,#FFFFFF,#FF0000);
background: -o-linear-gradient(right,#0000FF,#FFFFFF,#FF0000);
background: -moz-linear-gradient(right,#0000FF,#FFFFFF,#FF0000);
background: linear-gradient(to right,#0000FF,#FFFFFF,#FF0000);
}
.sequence{
margin-top:40px;
}
</style>


<div id="container"><div id="item1"><span>Low Propensity&nbsp;&nbsp;</span></div><div id="item2"></div><div id="item3"><span>&nbsp;&nbsp;High Propensity</span></div></div>
<div class="sequence">
<pre>
<?php

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
        $position_array = array();
        
        foreach ($sosco_key as $key) {
                $dipeptide_test[$key] = 0;
        }
        $i = 0;
        $condition = strlen($sequence) - ($gap + 1);
        while ($i < $condition) {
                $temp_aa = substr($sequence, $i, 1) . substr($sequence, $i + ($gap + 1), 1);
                $dipeptide_test[$temp_aa]++;
                $position_array[$i] = $temp_aa; 
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
        $max_propensity = 1000.0;
        $min_propensity = 0.0; 
        $x = 0;
        $end = count($position_array);
        $color_array = array();
        while ($x <= $end) {
                if ($x == 0) {
                        $position_score = $scoring[$position_array[$x]];
                        $color_array[$x] = $position_score;
                        $x++;
                        continue;
                }
                elseif ($x == $end) {
                        $position_score = $scoring[$position_array[$x-1]];
                        $color_array[$x] = $position_score;
                        $x++;
                        continue;
                }
                else {
                        $position_score_1 = $scoring[$position_array[$x-1]];
                        $position_score_2 = $scoring[$position_array[$x]];
                        $position_score = ($position_score_1 + $position_score_2) / 2;
                        $color_array[$x] = $position_score;
                        $x++;
                }
        }
        $color_code = array();
        $x = 0;
        foreach($color_array as $color) {
                if ($color >= 350) {
                        $color = 350 - $color;
                        $ini_distance = $max_propensity - 350;
                        $color = $color + $ini_distance;
                        $normalize_distance = intval(($color / $ini_distance) * 256);
                        $bicode = dechex($normalize_distance);
                        if (strlen($bicode) == 1) {
                                $bicode = '0' . $bicode;
                        }
                        elseif (strlen($bicode) == 3) {
                                $bicode = 'FF';
                        }
                        $code = 'FF' . $bicode . $bicode;
                        $color_code[$x] = $code;
                        $x ++;
                        continue;
                }
                elseif ($color < 350 and $color >= 0) {
                        
                        $ini_distance = 350 - $min_propensity;
                        $normalize_distance = intval(($color / 188) * 256);
                        $bicode = dechex($normalize_distance);
                        if (strlen($bicode) == 1) {
                                $bicode = '0' . $bicode;
                        }
                        elseif (strlen($bicode) == 3) {
                                $bicode = 'FF';
                        }
                        $code = $bicode . $bicode . "FF";
                        $color_code[$x] = $code;
                        $x ++;
                        continue;
                }
        }      

        
        
        
        return array($score, $color_code);        
}
function displayer($each_sequence, $sosco_key, $scoring) {
        $cuc_array = cuc_sc($each_sequence, $sosco_key, $scoring);
        $score = $cuc_array[0];
        $color_code = $cuc_array[1];
        $x = 0;
        while ($x < strlen($each_sequence)){
                $letter = substr($each_sequence, $x, 1);
                $each_color = '<span style="color:#%s">' . $letter . '</span>';
                $each_color = sprintf($each_color, $color_code[$x]);
                echo $each_color;     
                $x++;
        }             
        echo '<br>';
}
$sc_array = make_scorecard('output_scorecard22.jpg');
$sosco_key = $sc_array[0];
$scoring = $sc_array[1];
$temp_score = $sc_array[2];
$sc_array = null;

$sequence = $_GET["Sequence"];
if (! ($sequence)) {
        die("Unable to catch your keyword, please try it again.");
}


$display_per_line = 100;
$sequence_length = strlen($sequence);

$i = 0;
$u = 0;
$sequence_fragment = array();
while ($i < $sequence_length) {        
        if ($i + $display_per_line > $sequence_length) {
                $sequence_fragment[$u] = substr($sequence, $i);
                break;
        }
        $sequence_fragment[$u] = substr($sequence, $i, $display_per_line);
        $i = $i + $display_per_line;
        $u++;
}
$repeat = '....*....|';
$i = 0;
$v = 10;
foreach ($sequence_fragment as $fragment) {
        $first_line_output = '';
        $second_line_output = '';
        $tmp = $v + 100;
        while ($v < $tmp) {
                if ($v - 10 > $sequence_length) {
                        break;
                }
                $first_line_output = $first_line_output . str_repeat(' ', 10 - strlen($v)) . $v;
                $second_line_output = $second_line_output . $repeat;
                if ($v == $sequence_length) {
                        break;
                }
                $v = $v + 10;
        }
        
        echo '<span style="color:#4498d4;">' . $first_line_output . '</span>';
        echo '<br>';
        echo '<span style="color:#4498d4;">' . $second_line_output . '</span>';
        echo '<br>';
        echo $fragment;
        echo '<br>';
        displayer($fragment, $sosco_key, $scoring);
}
?>
</pre>
</div>
</div>
</body>
</html>