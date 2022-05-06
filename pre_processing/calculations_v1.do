/*******************************************************************************
 * Filename: calculations_v1
 * Author: Cameron Yap
 * Team: Index Zero
 * Date Created: 2/16/2022
 
********************************************************************************
********************************************************************************
**/

/*set working directory to file location*/
cd "\\ppd3.sppd.usc.edu\users$\cyap\Index Zero Data Work"

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
  * Rent Prices Data
***/
import delimited "Raw Files\LA Rent Prices.csv", clear

//format variables
gen geoid2 = substr(geoid, 11, 10)
destring geoid2, replace
rename amount median_rent

//keep only latest year of data
drop if year != 2016

//keep, order, save
keep geoid geoid2 tractnumber median_rent neighborhood
order geoid geoid2 tractnumber median_rent neighborhood
save "Calculations\Stata Files\2016 LA County Median Rent Price by 2010 CT", replace
export delimited "Calculations\2016 LA County Median Rent Price by 2010 CT.csv", replace


/** #3
  * Oil Wells Data
***/
import delimited "Interim Data\LA_County_Oil_Wells_Spatial_Joined.csv", clear

//format census tract variables
rename geoid geoid2
tostring geoid2, replace
gen geoid = "1400000US0" + geoid2
destring geoid2, replace
drop if geoid2 == .

//generate well count variable & collapse into a total count
gen well_count = 1
collapse (sum) well_count, by(geoid geoid2)

//keep, order, save
keep geoid geoid2 well_count
order geoid geoid2 well_count
save "Calculations\Stata Files\LA County Oil Wells by 2010 CT", replace
export delimited "Calculations\LA County Oil Wells by 2010 CT.csv", replace


/** #4
  * CalEnviroScreen Data
***/
import excel "Raw Files\CalEnviroScreen 4.0.xlsx", firstrow clear

//format variables
rename CensusTract geoid2
replace geoid2 = 6037137000 if geoid2 == 6037930401
tostring geoid2, replace
gen geoid = "1400000US0" + geoid2
destring geoid2, replace
drop if CaliforniaCounty != "Los Angeles"
replace CES40Score = "" if CES40Score == "NA"
destring CES40Score, replace

//keep, order, save
order geoid geoid2
save "Calculations\Stata Files\CalEnviroScreen Data by 2010 CT", replace
export delimited "Calculations\CalEnviroScreen Data by 2010 CT.csv", replace


import excel "Raw Files\California Demographic Profile.xlsx", firstrow clear

//format variables
rename CensusTract geoid2
replace geoid2 = 6037137000 if geoid2 == 6037930401
tostring geoid2, replace
gen geoid = "1400000US0" + geoid2
destring geoid2, replace
drop if CaliforniaCounty != "Los Angeles"
replace CES40Score = "" if CES40Score == "NA"
destring CES40Score, replace

//keep, order, save
order geoid geoid2
save "Calculations\Stata Files\Demographic Data by 2010 CT", replace
export delimited "Calculations\Demographic Data by 2010 CT.csv", replace


/** #5
  * aggregate all to LA County Tracts for final output file
***/
use "Interim Data\Los Angeles County", replace

merge 1:1 geoid2 using "Calculations\Stata Files\CalEnviroScreen Data by 2010 CT"
drop _merge

merge 1:1 geoid2 using "Calculations\Stata Files\Demographic Data by 2010 CT"
tabulate _merge
drop _merge

merge 1:1 geoid2 using "Calculations\Stata Files\LA County Oil Wells by 2010 CT"
replace well_count = 0 if well_count == .
drop _merge

merge 1:1 geoid2 using "Calculations\Stata Files\2016 LA County Median Rent Price by 2010 CT"

drop if geoid2 == 6037990300

keep geoid geoid2 TotalPopulation Ozone PM25 DieselPM DrinkingWater Lead Pesticides ToxRelease Traffic CleanupSites GroundwaterThreats HazWaste ImpWaterBodies SolidWaste Asthma LowBirthWeight CardiovascularDisease	Education LinguisticIsolation Poverty Unemployment HousingBurden  Children10years Pop1064years Elderly64years Hispanic White AfricanAmerican NativeAmerican AsianAmerican OtherMultiple well_count median_rent


foreach var in TotalPopulation Ozone  DieselPM Pesticides  CleanupSites GroundwaterThreats HazWaste ImpWaterBodies SolidWaste median_rent {
	tostring `var', replace
	replace `var' = "NA" if `var' == "."
	replace `var' = "NA" if `var' == ""

}

save "Calculations\Stata Files\Aggregated Stats", replace
export delimited "Calculations\Aggregated Stats.csv", replace
