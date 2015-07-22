# get all files 
setwd(getwd()) # set path to folder if different than location of THIS file
file_list <- list.files(pattern="\\.txt$")

# read results
# clean up results .txt file (add source, julian day, year)
read_results <- function(input_file){
  inputname <- substr(input_file, 1, nchar(input_file)-4)
  split <- strsplit(inputname, "_") # split name on underscores
  
  year <- as.numeric(split[[1]][2]) # get year
  firstday <- as.numeric(split[[1]][3]) # get first julian day
  lastday <- as.numeric(split[[1]][4]) # get last julian day
  
  tempdf <- read.csv(input_file, header=TRUE)
  tempdf[,1] <- inputname
  names(tempdf)<-c("SOURCE", "CODE", "CVPM_2", "CVPM_3", "CVPM_4", "CVPM_5", "CVPM_6", "CVPM_7", "CVPM_8", "CVPM_9", "CVPM_10", "CVPM_11", "CVPM_12", "CVPM_13", "CVPM_16", "CVPM_17", "CVPM_18", "CVPM_20", "CVPM_14A", "CVPM_14B", "CVPM_15A", "CVPM_15B", "CVPM_19A", "CVPM_19B", "CVPM_21A", "CVPM_21B")
  tempdf[["CLASS"]] <- c("Water", "Agriculture", "Fallow")
  tempdf[["YEAR"]] <- year
  tempdf[["JULIAN_START"]] <- firstday
  tempdf[["JULIAN_END"]] <- lastday
  final <- tempdf[,c(1:2, 27:30, 3:26)] # reorder cols
}



for (file in file_list){
  
  # if the merged dataset doesn't exist, create it
  if (!exists("dataset")){
    dataset <- read_results(file)
  }
  
  # if the merged dataset does exist, append to it
  else if (exists("dataset")){
    temp_dataset <-read_results(file)
    dataset<-rbind(dataset, temp_dataset)
    rm(temp_dataset)
  }
  
}

write.csv(dataset, "tabulated_results.csv")