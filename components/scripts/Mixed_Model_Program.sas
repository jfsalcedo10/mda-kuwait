%let path=~/MDA;
libname data base "&path/data";	


/* without covariates */
proc mixed data=data.sst covtest PLOTS(MAXPOINTS=NONE);
	class id topic;
	model sentiment = constant / solution outp=pred;
	random intercept / subject=topic solution;
	random intercept / subject=id(topic) solution;
	ods exclude solutionr;
	ods output solutionr=re_estimates;
run;
/* 
	for testing whether the variances are zero: take boundary problem into account, 
	in this case the correction is to half the p-values 
*/

/* get the fitted values per speech */
data data.pred;
	set pred;
run;


/* approval rating */
proc mixed data=data.approval PLOTS(MAXPOINTS=NONE);
	class id topic;
	model sentiment = Approve / solution;
	random intercept / subject=topic;
	random intercept / subject=id(topic);
run;

proc mixed data=data.approval PLOTS(MAXPOINTS=NONE);
	class id topic;
	model sentiment = Disapprove / solution;
	random intercept / subject=topic;
	random intercept / subject=id(topic);
run;

proc mixed data=data.approval PLOTS(MAXPOINTS=NONE);
	class id topic;
	model sentiment = ratio / solution;
	random intercept / subject=topic;
	random intercept / subject=id(topic);
run;


/* economy rating */
proc mixed data=data.economy PLOTS(MAXPOINTS=NONE);
	class id topic;
	model sentiment = better / solution;
	random intercept / subject=topic;
	random intercept / subject=id(topic);
run;

proc mixed data=data.economy PLOTS(MAXPOINTS=NONE);
	class id topic;
	model sentiment = worse / solution;
	random intercept / subject=topic;
	random intercept / subject=id(topic);
run;

proc mixed data=data.economy PLOTS(MAXPOINTS=NONE);
	class id topic;
	model sentiment = ratio / solution;
	random intercept / subject=topic;
	random intercept / subject=id(topic);
run;


/* personal finance rating */
proc mixed data=data.pfin PLOTS(MAXPOINTS=NONE);
	class id topic;
	model sentiment = better / solution;
	random intercept / subject=topic;
	random intercept / subject=id(topic);
run;

proc mixed data=data.pfin PLOTS(MAXPOINTS=NONE);
	class id topic;
	model sentiment = worse / solution;
	random intercept / subject=topic;
	random intercept / subject=id(topic);
run;

proc mixed data=data.pfin PLOTS(MAXPOINTS=NONE);
	class id topic;
	model sentiment = ratio / solution outp=pred_pfin;
	random intercept / subject=topic solution;
	random intercept / subject=id(topic) solution;
	ods exclude solutionr;
	ods output solutionr=re_estimates_pfin;
run;

/* get the fitted values per speech */
data data.pred_pfin;
	set pred_pfin;
run;


/* jobmarket rating */
proc mixed data=data.jobs PLOTS(MAXPOINTS=NONE);
	class id topic;
	model sentiment = better / solution;
	random intercept / subject=topic;
	random intercept / subject=id(topic);
run;

proc mixed data=data.jobs PLOTS(MAXPOINTS=NONE);
	class id topic;
	model sentiment = worse / solution;
	random intercept / subject=topic;
	random intercept / subject=id(topic);
run;

proc mixed data=data.jobs PLOTS(MAXPOINTS=NONE);
	class id topic;
	model sentiment = ratio / solution outp=pred_jobs;
	random intercept / subject=topic solution;
	random intercept / subject=id(topic) solution;
	ods exclude solutionr;
	ods output solutionr=re_estimates_jobs;
run;

/* get the fitted values per speech */
data data.pred_jobs;
	set pred_jobs;
run;


