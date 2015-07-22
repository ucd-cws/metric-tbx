
tempdf <- dataset[c(26:30, 1:25, 31)]


names(tempdf)<-c("SOURCE", "CLASS", "YEAR", "JULIAN_START", "JULIAN_END","CODE", "CVPM_2", "CVPM_3", "CVPM_4", "CVPM_5", "CVPM_6", "CVPM_7", "CVPM_8", "CVPM_9", "CVPM_10", "CVPM_11", "CVPM_12", "CVPM_13", "CVPM_16", "CVPM_17", "CVPM_18", "CVPM_20", "CVPM_14A", "CVPM_14B", "CVPM_15A", "CVPM_15B", "CVPM_19A", "CVPM_19B", "CVPM_21A", "CVPM_21B")

dataset<-tempdf

rm(tempdf)

# rename cols in final dataset
write.csv(dataset, "tabulated_results.csv")