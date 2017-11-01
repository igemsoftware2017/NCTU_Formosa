<?php
error_reporting(0);
@session_start();
$counterFile = "counter.txt";
$counter = intval(file_get_contents($counterFile));
if($_SESSION['counted']!=1){
$fp = @fopen($counterFile, "w");
if($fp){
flock($fp, 2);
@fwrite($fp, ++$counter);
flock($fp, 3);
fclose($fp);
$_SESSION['counted']=1;
}
}
?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" >
<html lang="en">
<head>
<meta charset="UTF-8">
<META NAME="keywords" CONTENT="parabse, Parabase" />
<title>Parabase</title>
<link rel="stylesheet" type="text/css" href="css/header.css" media="screen" />
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
            <div id="top">
            <div id="homeDescr" class="clearfix" style="max-height: 400px;">
            <h1 class="lf">Parabase: a simple and applicable peptide prediction system with validation of artificial intelligence</h1>	
            <div  id="para_desc"><span><span>Parabase</span> is a software established by NCTU_Formosa iGEM team which aims for 
            (1)predicting potential antifungal peptides, (2)searching validated antifungal peptides, and (3)finding the relationship 
            between fungal pathogen, their host species and target peptides. To use the peptide prediction system, please click the
             "Predcit System" buttom. To use our search system, please click the "Search System" buttom. More information will be 
             given in the web page of the systems, respectively. Further user guide can be found in "Help". If there is any question, 
             welcome to contact us.
            </span>
            </div>
            
<div id="chooseprog" class="section clearfix">
            <h2>Parabase Tools</h2>
            <div id="control_tools">
            <a href="predict.html" class="left spFirst" id="homepara"><img class="control_tools" src="images/predict-system.png"/></a>
            <div id="transl" class="left">
            </div>
            <a href="search.html" class="left" id="homepara"><img class="control_tools" src="images/search-system.png"/></a>
            </div>
</div>
<div class="col-md-3" style="
    position: relative;
    max-width: 25%;
    left: 75%;
    top: -450px;
">
							<h2 class="title">Current curation</h1>
														<h4>Release: Oct. 1, 2017 </h4>
							<hr style="background: none;  border-bottom-style:dashed; border-bottom-color: #ECECEC">
														<h4>Number of peptides: 1334 </h4>
							<hr style="background: none;  border-bottom-style:dashed; border-bottom-color: #ECECEC">
														<h4>Number of pathogens: 383 </h4>
							<hr style="background: none;  border-bottom-style:dashed; border-bottom-color: #ECECEC">
														<h4>Number of host species: 161 </h4>
							<hr style="background: none;  border-bottom-style:dashed; border-bottom-color: #ECECEC">
														<h4>Number of articles: 584 </h4>
							<hr style="background: none;  border-bottom-style:dashed; border-bottom-color: #ECECEC">
														
</div>
<div id="our_info"">
    <p style="color:#656565;"><h6>NCTU_Formosa, National Chiao Tung University, Hsinchu, Taiwan</h6></p>
</div>
</body>
</html>
