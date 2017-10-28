#!/usr/bin/perl
#####
# This script try to make a pml file for pymol
# This pml file is try to color the residue according to the propensity scores
# markliou 20140903
#####
use 5.010 ;

%aminoacid_abbr = ('CYS', 'C', 'ASP', 'D', 'SER', 'S', 'GLN', 'Q', 'LYS', 'K',
				 'ILE', 'I', 'PRO', 'P', 'THR', 'T', 'PHE', 'F', 'ASN', 'N', 
				 'GLY', 'G', 'HIS', 'H', 'LEU', 'L', 'ARG', 'R', 'TRP', 'W', 
				 'ALA', 'A', 'VAL', 'V', 'GLU', 'E', 'TYR', 'Y', 'MET', 'M') ;
				 
user_interface() ;
open pmlfile,">$outfile" or die ;
select pmlfile;
if($smooth_color_bar == 1){
	set_color_smooth(parse_PDB($PDB ,$ppsfile,'N')) ;
}else{
	set_color($ppsfile) ;
}
parse_PDB($PDB ,$ppsfile);
close pmlfile ;


##### user interface
sub user_interface{
	print " Please input the PDB file: ";
	$PDB= <stdin>;
	chomp $PDB ;
	print " Please input the score file: ";
	$ppsfile= <stdin>;
	chomp $ppsfile ;
	print " Please input the score file type (0:propensity score, 1:dipeptide score, default:0):";
	$score_file_type= <stdin>;
	chomp $score_file_type ;
	$score_file_type == 0 ? 0:1 ;
	print " Please input the smooth parameter (default:1): ";
	$smooth_par = <stdin> ;
	chomp $smooth_par ;
	$smooth_par = ($smooth_par eq '')?1:$smooth_par;
	print " Please input the smooth color bar? (0:no 1:yes default:0): ";
	$smooth_color_bar = <stdin> ;
	chomp $smooth_color_bar ;
	$smooth_color_bar = ($smooth_color_bar eq '')?0:$smooth_color_bar;
	#say $smooth_par;
	print " Please input the output file: ";
	$outfile= <stdin>;
	chomp $outfile ;
}

##### parse the PDB file and output the pml script for color
sub parse_PDB{
	my $pdb ;
	my $line ;
	my ($chain,$p_chain) = (' ',' ') ;
	my ($resi,$p_resi)=(0,0) ;
	my $resn ;
	my $seq ;
	my @resi ;
	my @s_ps ;
	my $s_ps ;
	my $pstab = $_[1] ;
	my $write_result = $_[2] ;
	my $i ;
	
	$pdb = $_[0] ;
	open file,"<$pdb" or die " can't open $pdb !" ;
	while($line = <file>){
		chomp $line ;
		if($line=~/^ATOM/){
			#say $line; #debug
			$chain = substr($line,21,1) ;
			
			if ($p_chain eq ' '){
				$p_chain = $chain  ;
				next ;
			}
			########################
			if($p_chain ne $chain){
				if($score_file_type == 0){
					@s_ps = smooth_seq_score($seq,$smooth_par,$pstab) ;
				}else{
					@s_ps = smooth_dpc_score($seq,$smooth_par,$pstab);
				}
				#say for @s_ps;
				
				# output the pml
				for $i(0..$#s_ps){ 
					$s_ps = $s_ps[$i];
					$resi = $resi[$i];
					say "color ps_$s_ps , chain $p_chain & resi $resi ";
				}
				@resi = ();
				$seq = '';
				
				# say("$p_chain $chain");
			}
			$p_chain = $chain ;
			########################
			
			$resn  = substr($line,17,3) ;
			$resi  = int(substr($line,22,4)) ;
			#say $resi; #debug
			
			if($p_resi ne $resi){
				#say ($resi,$aminoacid_abbr{$resn}) ; # debug
				$seq .= $aminoacid_abbr{$resn} ;
				push @resi,$resi ;
			}
			$p_resi = $resi ;
			#say $seq ;
		}
	}
	close file ;
	
	# say $seq ;
	if($score_file_type == 0){
		@s_ps = smooth_seq_score($seq,$smooth_par,$pstab) ;
	}else{
		@s_ps = smooth_dpc_score($seq,$smooth_par,$pstab);
	}
	
	return(@s_ps) if ($write_result eq 'N'); 
	
	# output the pml
	for $i(0..$#s_ps){ 
		$s_ps = $s_ps[$i];
		$resi = $resi[$i];
		say "color ps_$s_ps , chain $chain & resi $resi";
	}
		
}

##### parse the peopensity score file
sub parse_pps{
	my $psfile ;
	my %pps ;
	my $line ;
	my @pps ;
	
	$psfile = $_[0] ;
	open psfile,"<$psfile" or die " can't open $psfile !" ;
	while($line = <psfile>){
		chomp $line ;
		#say for @{[split"\t",$line]};
		push(@pps,(@{[split"\t",$line]}));
	}
	close psfile ;
	%pps = @pps ;
	#say "$_ $pps{$_}" for keys(%pps) ; 
	
	return %pps ;
}

##### parse the dipeptide score
sub parse_dps{
	my $dpsfile ;
	my %dps ;
	my $line ;
	my @dps ;
	my @aa ;
	my $temp ;
	
	$dpsfile = $_[0] ;
	open dpsfile,"<$dpsfile" or die " can't open $dpsfile !" ;
	$line = <dpsfile> ;
	chomp $line ;
	@aa = map{$temp = $_ ; map{$temp.$_}@{[split"\t",$line]}}@{[split"\t",$line]} ;
	
	$temp = 0 ;
	while($line = <dpsfile>){
		chomp $line ;
		$dps{$aa[$temp++]} = $_ for (@{[split"\t",$line]});
	}
	close dpsfile ;
	#say "$_ $dps{$_}" for keys(%dps) ; 
	
	return %dps ;
}

##### smooth the residue score
sub smooth_seq_score{
	my @seq = split'',$_[0];
	my $score ;
	my $smooth_par = $_[1] ;
	my @t_score ;
	my $t_score ;
	my %pps = parse_pps($_[2]);
	my ($i,$j,$start,$end,$resno) ;
	
	for $i (0..$#seq){
		$start = ($i-$smooth_par)<=0    ?0    :($i-$smooth_par) ;
		$end   = ($i+$smooth_par)>=$#seq?$#seq:($i+$smooth_par) ;
		$resno = $end-$start+1 ;
		$t_score = 0 ;
		for $j ($start..$end){
			$t_score += ($pps{$seq[$j]}/$resno) ;
		}
		push @t_score,int($t_score);
	}
	
	#say for @t_score;
	return @t_score;
}

##### smooth the dpc score
sub smooth_dpc_score{
	my @seq = split'',$_[0];
	my $score ;
	my $smooth_par = $_[1] ;
	my @t_score ;
	my $t_score ;
	my %dps = parse_dps($_[2]);
	my ($i,$j,$start,$end,$resno) ;
	
	for $i (0..$#seq){
		$start = ($i-$smooth_par)<=0    ?0    :($i-$smooth_par) ;
		$end   = ($i+$smooth_par)>=$#seq?$#seq:($i+$smooth_par) ;
		$resno = $end-$start+1 ;
		$t_score = 0 ;
		if($smooth_par==0){
			$t_score = ($dps{$seq[$start].$seq[$start+1]}/($resno-1)) ;
		}else{
			for $j ($start..($end-1)){
				$t_score += ($dps{$seq[$j].$seq[$j+1]}/($resno-1)) ;
			}
		}
		push @t_score,int($t_score);
	}
	
	#say for @t_score;
	return @t_score;
}

##### set color
sub set_color{
	my $temp ;
	my $ppsfile = $_[0] ;
	my $line ;
	my ($max,$min,$cscore,$mid,$space) ;
	my $color_name ;
	
	open ppsfile,"<$ppsfile" or die " there is no $ppsfile" ;
	if($score_file_type == 0){
		$line=<ppsfile>;
		chomp $line ;
		$max = $min = ${[split"\t",$line]}[1] ;
		while($line =<ppsfile>){
			chomp $line ;
			$cscore = ${[split"\t",$line]}[1] ; 
			$max = ($max<$cscore)?$cscore:$max ;
			$min = ($min>$cscore)?$cscore:$min ;
		}
	}else{
		$line=<ppsfile>;
		$line=<ppsfile>;
		chomp $line ;
		$max = $min = ${[split"\t",$line]}[0] ;
		seek(ppsfile,0,0) ;
		$line =<ppsfile> ;
		while($line =<ppsfile>){
			chomp $line ;
			for $cscore (@{[split"\t",$line]}){ 
				$max = ($max<$cscore)?$cscore:$max ;
				$min = ($min>$cscore)?$cscore:$min ;
			}
		}
	}
	
	close ppsfile ;
	
	$space = int(($max-$min)/2) ;
	$mid = int($min+(($max-$min)/2)) ;
	say "$max $min $mid" ;
	
	for(($min)..($max)){
		#$color_name = int($_+$min) ;
		print "set_color " ;
		print "ps_";
		print "$_ = [" ;
		if($_>$mid){
			$temp = (1 - ((int($_-$mid))*(1/$space)));
			print '1' ;
			print ',' ;
			print $temp;
			print ',' ;
			print $temp ;
		}elsif($_<$mid){
			$temp = (int($_-$min))*(1/$space);
			print $temp ;
			print ',' ;
			print $temp;
			print ',' ;
			print '1' ;
		}else{
			print '1,1,1';
		}
		say   "]";
	}
}
# sub set_color{
	# my $temp ;
	# for(0..1000){
		# print "set_color " ;
		# print "ps_";
		# print "$_ = [" ;
		# if($_>500){
			# $temp = (1 - (($_-500)*0.002));
			# print '1' ;
			# print ',' ;
			# print $temp;
			# print ',' ;
			# print $temp ;
		# }elsif($_<500){
			# $temp = ($_)*0.002;
			# print $temp ;
			# print ',' ;
			# print $temp;
			# print ',' ;
			# print '1' ;
		# }else{
			# print '1,1,1';
		# }
		# say   "]";
	# }
# }


##### set color according to the smooth score
sub set_color_smooth{
	my $temp ;
	#my $ppsfile = $_[0] ;
	my $line ;
	my ($max,$min,$cscore,$mid,$space) ;
	my $color_name ;
	my @smooth_score = @_ ;
	
	($min,$max) = @{[sort{$a<=>$b}@smooth_score]}[0,-1] ;
	$space = int(($max-$min)/2) ;
	$mid = int($min+(($max-$min)/2)) ;
	say "$max $min $mid" ;
	
	for(($min)..($max)){
		#$color_name = int($_+$min) ;
		print "set_color " ;
		print "ps_";
		print "$_ = [" ;
		if($_>$mid){
			$temp = (1 - ((int($_-$mid))*(1/$space)));
			print '1' ;
			print ',' ;
			print $temp;
			print ',' ;
			print $temp ;
		}elsif($_<$mid){
			$temp = (int($_-$min))*(1/$space);
			print $temp ;
			print ',' ;
			print $temp;
			print ',' ;
			print '1' ;
		}else{
			print '1,1,1';
		}
		say   "]";
	}
}