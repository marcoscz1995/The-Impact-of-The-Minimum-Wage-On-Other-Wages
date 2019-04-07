setwd("~/ECON 480/newFolder")
library(plm)
library(tidyr)
library(dplyr)
library(readr)
library(ggplot2)

data <- read_csv("dfTotal_no_nan.csv")
df_year<- read_csv("occ_data_year.csv")
df<- read_csv("occ_data.csv")






##### clean the data ########

#remove all rows with * or # in H_MEAN
data<-data[!(data$H_MEAN=="*" | data$H_MEAN=="#" ),]

#if the state min wage < fed min wage --> state min wage <- fed min wage
#the fed min wage is the lowest wage for all states
minWage<-pmax(data$`Minimum Wage`, data$`Federal Minimum Wage`)
data<-cbind(data,minWage)

#delete the some values from the global enviromnet
rm(minWage,dfTotal_no_nan)

#####finding the interesctions: the jobs that exist in all years and in all states#####

#####import and clean the intersection data

##all the occ_codes that exist in all years grouped by states

#a list of all the occ codes that exist in all years grouped by states
df_state_intersect<-as.data.frame(Reduce(intersect,df))
#rename the column
colnames(df_state_intersect)<-"occ_code"
#convert to characters
df_state_intersect$occ_code<-as.character(df_state_intersect$occ_code)

##all the occ_codes that exist in all states grouped by year

#a list of all the occ codes that exist in all states by year ie what jobs are common amongst all years
#these are the jobs that exist in all 16 years and among all 45 states
df_year_intersect<-as.data.frame(Reduce(intersect,df_year))
#rename the column
colnames(df_year_intersect)<-"occ_code_year"
#convert to characters
df_year_intersect$occ_code_year<-as.character(df_year_intersect$occ_code_year)

rm(df_year)

########need the interesection of df_state_intersect and df_year_intersect 
#this is all the jobs that exist in all years and in all states

#convert the two dataframes two vectors and find their interesection, and then convert to a dataframe
dfyear<-c(df_year_intersect$occ_code_year)
dfstate<-c(df_state_intersect$occ_code)
intersect_total<-as.data.frame(intersect(dfyear,dfstate))
#rename the column
colnames(intersect_total)<-"occ_code_total"
#convert to character
intersect_total$occ_code_total<-as.character(intersect_total$occ_code_total)

#intersect_total has 423 obs: ie 423 jobs that exist in every year and every state


rm(dfyear,dfstate)



#exculde all OCC_codes that are not in intersect_total

data1 <- data[data$OCC_CODE %in% intersect_total$occ_code_total,]
#at this point data1 has 261063 obs

#still an ubalanced panel since alabama in 2017 has 634 jobs, when it should have exactly 423 jobs
#the above operations are doing things but not removing what I require

data<-data1

#####Variable analysis######


#upload the modified data that was edited in python
data<-read_csv("minWageDataUpdated.csv")

attach(data)

#Type casting

#make the variables as vectors 
Y <- data$log_Hourly_Wages #hourly wage
MW<-data$log_minWage #min wage
E<-data$`Typical education needed for entry` #education


########the main course######

#set data as panel data
pdata<-plm.data(data,index = c("STATE", "Year"))

#fixed effect

data$id <-group_indices(data, STATE, OCC_TITLE) #re-index

####full model

#Fixed effects model, Year FE
mod1<-plm(Y~MW+data$Year, data = data, index = c("id", "Year"), model = "within", effect = "time")
summary(mod1)

#fixed effects with state and year fixed effects
mod2<-plm(Y~MW + data$id + data$Year, data = data, index = c("id", "Year"), model = "within", effect = "twoways")
summary(mod2)

#fixed effects with year fixed effects
mod3<-plm(Y~MW + data$Year +E + E:MW, data = data, index = c("id", "Year"), model = "within", effect = "time")
summary(mod3)

#fixed effects with year and state fixed effects full model
mod4<-plm(Y~MW + data$Year + data$id +E + E:MW, data = data, index = c("id", "Year"), model = "within", effect = "twoways")
summary(mod4)

#simple models
mod5<-plm(Y~MW, data = data, index = c("id", "Year"), model = "within", effect = "time") #model 1
mod6<-plm(Y~MW, data = data, index = c("id", "Year"), model = "within", effect = "twoways") #model 2
mod7<-plm(Y~MW + E +E:MW, data = data, index = c("id", "Year"), model = "within", effect = "time") #model 3
mod8<-plm(Y~MW + E + E:MW, data = data, index = c("id", "Year"), model = "within", effect = "twoways") #full model 4

##plot the min-wage distribution for a given year

minWageByState <-
count<-table(unique(data$minWage))

ggplot(data, aes(data$minWage))+geom_histogram()

coeftest(mod3.plm, vcov=vcovHC(mod3.plm,type="HC0",cluster="group"))

library(lmtest)
library(sandwich)
coeftest(mod3, vcov=vcovHC(mod3,type="HC0",cluster="group"))

coeftest(mod5, vcov=vcovHC(mod5,type="HC0",cluster="group"))
coeftest(mod6, vcov=vcovHC(mod6,type="HC0",cluster="group"))
coeftest(mod7, vcov=vcovHC(mod7,type="HC0",cluster="group"))
coeftest(mod8, vcov=vcovHC(mod8,type="HC0",cluster="group"))



