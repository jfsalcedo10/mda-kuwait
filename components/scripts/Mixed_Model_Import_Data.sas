%let path=~/MDA;
libname data base "&path/data";	

*****************************;
*  data without covariates  *;
*****************************;

proc import out=data.sst
    datafile="&path/data/df_ssnmf_pivot.csv"
    dbms=csv
    replace;
    getnames=YES;
run;

proc sort data=data.sst;
	by topic id sentence;
run;

proc freq data=data.sst nlevels;
	tables sentiment / noprint;
run;

/* delete missing values */;
data data.sst;
 set data.sst;
 if cmiss(of _all_) then delete;
run;

/* check whether rows with missing values have been deleted */;
proc freq data=data.sst nlevels;
	tables sentiment / noprint;
run;

data data.sst;
 set data.sst;
 constant = 1;
run;


********************************;
*  data with approval ratings  *;
********************************;

proc import out=data.approval
    datafile="&path/data/df_ssnmf_approval_ratings.txt"
    dbms=csv
    replace;
    getnames=YES;
run;


*******************************;
*  data with economy ratings  *;
*******************************;

proc import out=data.economy
    datafile="&path/data/df_ssnmf_economy_ratings.txt"
    dbms=csv
    replace;
    getnames=YES;
run;


****************************************;
*  data with personal finance ratings  *;
****************************************;

proc import out=data.pfin
    datafile="&path/data/df_ssnmf_pfin_ratings.txt"
    dbms=csv
    replace;
    getnames=YES;
run;


*********************************;
*  data with jobmarket ratings  *;
*********************************;

proc import out=data.jobs
    datafile="&path/data/df_ssnmf_jobs_ratings.txt"
    dbms=csv
    replace;
    getnames=YES;
run;


*********************************;
*  export predicted sentiments  *;
*********************************;

*PROC EXPORT DATA=data.pred
*            OUTFILE="&path/data/predicted_sentiment.txt"
*            DBMS=CSV REPLACE;
*     PUTNAMES=YES;
*RUN;

*PROC EXPORT DATA=re_estimates
*            OUTFILE="&path/data/empiral_bayes_estimates.txt"
*            DBMS=CSV REPLACE;
*     PUTNAMES=YES;
*RUN;



