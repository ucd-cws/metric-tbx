# get all files 
#setwd(getwd()) # set path to folder if different than location of THIS file
setwd(file.path('C:/Users/Andy/Desktop/results')) # set path to folder if different than location of THIS file
file_list <- list.files(pattern="\\.dbf$")

# require foreign
require(foreign)
require(plyr)

# read results
# clean up results .txt file (add source, julian day, year)
read_results <- function(input_file){
  inputname <- substr(input_file, 1, nchar(input_file)-4)
  split <- strsplit(inputname, "_") # split name on underscores
  
  year <- as.numeric(split[[1]][2]) # get year
  firstday <- as.numeric(split[[1]][3]) # get first julian day
  lastday <- as.numeric(split[[1]][4]) # get last julian day
  
  tempdf <- read.dbf(input_file)
  tempdf[["SOURCE"]] <- inputname
  tempdf[["CLASS"]] <- c("Water", "Agriculture", "Fallow")
  tempdf[["YEAR"]] <- year
  tempdf[["JULIAN_START"]] <- firstday
  tempdf[["JULIAN_END"]] <- lastday
  final <- tempdf # reorder cols
}



for (file in file_list){
  
  # if the merged dataset doesn't exist, create it
  if (!exists("dataset")){
    dataset <- read_results(file)
  }
  
  # if the merged dataset does exist, append to it
  else if (exists("dataset")){
    temp_dataset <-read_results(file)
    dataset<-rbind.fill(dataset, temp_dataset)
    rm(temp_dataset)
  }
  
}


