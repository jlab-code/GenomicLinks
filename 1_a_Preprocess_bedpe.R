rm(list=ls())
library(dplyr)
library(data.table)


# Set the working directory
setwd('/mnt/storage3/luca2/v6_prominent_APs/')


raw.bedpe <- fread('/mnt/storage3/luca2/v6_prominent_APs/prominent_APs.bedpe')
raw.bedpe <- data.frame(raw.bedpe)


# check data 
if (ncol(raw.bedpe) > 6) {
  raw.bedpe <- select(raw.bedpe, -(7:ncol(raw.bedpe)))
} else {
  raw.bedpe <- raw.bedpe
  message("Data has correct format")
}

df.bedpe <- data.frame(raw.bedpe)

# Adjust the difference between s1 and e1 to 2500
#midpoint <- round((df.bedpe[,2] + df.bedpe[,3])/2)
#df.bedpe[,2] <- midpoint - 1250
#df.bedpe[,3] <- midpoint + 1250

# Adjust the difference between s2 and e2 to 2500
#midpoint2 <- round((df.bedpe[,5] + df.bedpe[,6])/2)
#df.bedpe[,5] <- midpoint2 - 1250
#df.bedpe[,6] <- midpoint2 + 1250

nms <- c("chr1","s1", "e1","chr2","s2","e2")
df.bedpe<-setnames(df.bedpe, nms)



# Define the folder name with unique_user_id
FOLDER <- 'predictions'

# Check if the folder exists, and create it if it doesn't
if (!dir.exists(FOLDER)) {
  dir.create(FOLDER)
}

fwrite(df.bedpe,paste0(FOLDER,"/out.csv"),sep = "\t", scipen = 50 )
tmpA<-df.bedpe[,1:3]
tmpA<- tmpA %>% dplyr::distinct(chr1,s1,e1)
fwrite(tmpA,paste0(FOLDER,"/region_A.csv"),sep = "\t", scipen = 50 )

tmpB<-df.bedpe[,4:6]
tmpB<- tmpB %>% dplyr::distinct(chr2,s2,e2)
fwrite(tmpB,paste0(FOLDER,"/region_B.csv"),sep = "\t", scipen = 50 )
message("Pairs created!")

# create unique folders
uniqFolder<-unique(df.bedpe$chr1)
# create main chr and sun chr
dir.create(file.path(FOLDER,"/chr"), showWarnings = FALSE)
mainDir= paste0(FOLDER,"/chr")
for (subDir in uniqFolder){
  dir.create(file.path(mainDir,subDir), showWarnings = FALSE)
}
