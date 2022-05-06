/*******************************************************************************
 * Filename: Zip_Tract_calculations.do
 * Author: Cameron Yap
 * Team: Index Zero
 * Date Created: 4/12/2022
 
********************************************************************************
********************************************************************************
**/

/*set working directory to file location*/
cd "/Users/cyap0710/Documents/School/USC/4. Spring 2022/DSCI 560/Index Zero Data Work"

/** #0
  * Turn on logs
***/
capture log close
local datetime : di %td_CY-N-D  date("$S_DATE", "DMY") " $S_TIME"
local datetime =  subinstr("`datetime'", " ", "_", .)
local datetime =  subinstr("`datetime'", ":", "_", .)
local datetime =  subinstr("`datetime'", "-", "_", .)
log using "Logs/log_`c(username)'_`datetime'"

/** #1
  * Program setup
***/
clear all
set more off
version 14
set linesize 80
drop _all


/** #2
  * 
***/
use "/Users/cyap0710/Documents/School/USC/4. Spring 2022/DSCI 560/Index Zero Data Work/Raw Files/Zipcode to Census Tract Crosswalk.dta", clear
keep ZIP TRACT RES_RATIO
rename TRACT geoid2
destring ZIP, replace
destring geoid2, replace
merge m:1 geoid2 using "/Users/cyap0710/Documents/School/USC/4. Spring 2022/DSCI 560/Index Zero Data Work/Interim Data/Los Angeles County.dta", keep(match)
keep ZIP geoid2
rename geoid2 geoid
bys ZIP (geoid): gen index=sum(geoid!=geoid[_n-1])
//reshape wide geoid, i(ZIP) j(index)

save "/Users/cyap0710/Documents/School/USC/4. Spring 2022/DSCI 560/Index Zero Data Work/Calculations/ZIP Tract Reference.dta", replace
export delimited "/Users/cyap0710/Documents/School/USC/4. Spring 2022/DSCI 560/Index Zero Data Work/Calculations/ZIP Tract Reference.csv", replace
