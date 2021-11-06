#!/bin/sh

TagTestFile=$1
CosEdit=$2
paths=$3
VAD=$4

awk ' function dist(a,b) {if(a in V && b in V) { dV = V[a] - V[b]; dA = A[a] - A[b]; dD = D[a] - D[b]; return sqrt(dV*dV + dA*dA + dD*dD)} 
       		    				 	    	     	       else {return "NA"}}
$1 == "#" {header = header " " $NF}; 
$1 == "sim" {print header " word1 word2 gold VAD.dist ant.morph ant.edges edges"
       while(getline < VAD > 0) {V[$1]=$2; A[$1]=$3; D[$1]=$4}
       while(getline < paths > 0) if($5 == "None") {pathValues[$1,$2]= "NA NA"} else {pathValues[$1,$2]= $5 " " $6}
       while(getline < TagTestFile > 0) {antmorph[$1,$2]=$3; gold[$1,$2]=$4}}
    {word1 = $(NF-1); word2 = $NF}
word1 SUBSEP word2 in gold {print($1, word1, word2, gold[word1, word2], dist(word1, word2), antmorph[word1,word2], pathValues[word1,word2])}' paths=$paths TagTestFile=$TagTestFile VAD=$VAD $CosEdit |
    tr '|' ' '


