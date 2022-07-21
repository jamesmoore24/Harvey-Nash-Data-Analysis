###OPEN THE DATASET ###

#Gio's Dataset
library(readxl)
library(openxlsx)
Company_Financial_Data <- read_excel("Desktop/Finance UROP/Company_Financial_Data.xlsx")
View(Nash_Financial_Data)

#Grab Data
sample_rev <- Company_Financial_Data$`Revenue - Total...36`
sample_date <- Company_Financial_Data$`Fiscal Data Year and Quarter`
sample_name <-Company_Financial_Data$`Company Name`
sample_total_asset <- Company_Financial_Data$`Assets - Total`
sample_net_inc <- Company_Financial_Data$`Income Before Extraordinary Items - Available for Common...17`

#Result vectors (want to fill these)
company_names <- c()
rev_growth_1_2020 <- c()
rev_growth_1_2021 <- c()
# rev_growth_3 <- c()
roa_2019 <- c()
roa_2020 <- c()
roa_2021 <- c()

###FUNCTIONS FOR CALCULATIONS###
rev_growth_1_func <- function(rev_vec, date_vec) {
  #Parameters:
    #rev_vec a column vector of 9-12 entries which represent the revenue totals/quarter
    #date_vec: a column vector of 9-12 entries depicting the year and quarter for each rev entry
  
  rev_growths <- c()
  for (ix_date in 1:length(date_vec)) {
    if (date_vec[ix_date] == "2019Q4" | 
        date_vec[ix_date] == "2020Q4" |
        date_vec[ix_date] == "2021Q4") {
      rev_growths <- c(rev_growths, rev_vec[ix_date])
    }
  }
  calc <- function(future_rev, past_rev) {
    return(((future_rev - past_rev)/past_rev)*100)
  }
  
  return(c(calc(rev_growths[2], rev_growths[1]), calc(rev_growths[3], rev_growths[2])))
}


roa_func <- function(asset_vec, income_vec, date_vec) {
  #Parameters:
    #asset_vec: vec with total amount of assets in a q
    #income_vec: vec with total income for that q
    #date_vec: vec with the dates for that quarter and year
  
  roas <- c()
  
  calc <- function(avg_asset, income_year) {
    #takes in numbers for the average asset and income over a year 
    return((income_year/avg_asset)*100)
  }
  
  avg_vec <- c()
  income_year <- c()
  
  for (i in 1:length(date_vec)) {
    if (date_vec[i] == "2019Q1" | 
        date_vec[i] == "2020Q1" |
        date_vec[i] == "2021Q1") {
      for (j in 0:3) {
        #need to find average total assets
        avg_vec <- c(avg_vec, asset_vec[i + j])
        income_year <- c(income_year, income_vec[i + j])
      }
      roas <- c(roas, calc(mean(avg_vec), sum(income_year)))
    }
  }
  return(roas)
}

### PARSER ###

#Holder Vecs
rev_vec <- c()
date_vec <- c()
asset_vec <- c()
net_inc_vec <- c()
results_rev <- c()
results_roa <- c()

for (i in 1:(length(sample_name)-1)) {
  rev_vec <- c(rev_vec, sample_rev[i])
  date_vec <- c(date_vec, sample_date[i])
  asset_vec <- c(asset_vec, sample_total_asset[i])
  net_inc_vec <- c(net_inc_vec, sample_net_inc[i])
  
  
  if (sample_name[i] != sample_name[i+1]) {
    #append values
    #add company to list
    company_names <- c(company_names, sample_name[i])
    
    #add revenue growths to chart
    results_rev <- rev_growth_1_func(rev_vec, date_vec)
    rev_growth_1_2020 <- c(rev_growth_1_2020, results_rev[1])
    rev_growth_1_2021 <- c(rev_growth_1_2021, results_rev[2])
    
    results_roa <- roa_func(asset_vec, net_inc_vec, date_vec)
    roa_2019 <- c(roa_2019, results_roa[1])
    roa_2020 <- c(roa_2020, results_roa[2])
    roa_2021 <- c(roa_2021, results_roa[3])
    
    #reset vectors
    rev_vec <- c()
    date_vec <- c()
    asset_vec <- c()
    net_inc_vec <- c()
  }
}
  

#write to excel file   
library(xlsx)  

ss <- data.frame("Company Name" = company_names,
                 "Revenue Growth 1 Year 2019-2020 (%)" = rev_growth_1_2020,
                 "Revenue Growth 1 Year 2020-2021 (%)" = rev_growth_1_2021,
                 "ROA 2019 (%)" = roa_2019,
                 "ROA 2020 (%)" = roa_2020,
                 "ROA 2021 (%)" = roa_2021)
  

write.xlsx(ss, 'Desktop/r.xlsx')


# CLEAN UP #################################################

# Clear environment
rm(list = ls())

# Clear packages
detach("package:datasets", unload = TRUE)  # For base

# Clear plots
dev.off()  # But only if there IS a plot

# Clear console
cat("\014")  # ctrl+L



