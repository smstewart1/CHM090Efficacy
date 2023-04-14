library(tidyverse)
library(MatchIt)
library(dplyr)
library(ggplot2)
classT <- "CHM-151"
labels <-"151 Control Group"
labelstwo <- "090 Cohort in 151"
mydataT <- read.csv("151with090.csv")
mydataC <- read.csv("151sans090.csv")
ATs <- nrow(mydataT[mydataT$Grade == "A" & mydataT$Course.Name == classT, ])
BTs <- nrow(mydataT[mydataT$Grade == "B" & mydataT$Course.Name == classT, ])
CTs <- nrow(mydataT[mydataT$Grade == "C" & mydataT$Course.Name == classT, ])
DTs <- nrow(mydataT[mydataT$Grade == "D" & mydataT$Course.Name == classT, ])
FTs <- nrow(mydataT[mydataT$Grade == "F" & mydataT$Course.Name == classT, ])
WTs <- nrow(mydataT[mydataT$Grade == "W" & mydataT$Course.Name == classT| 
                      mydataT$Grade == "WF" & mydataT$Course.Name == classT | 
                      mydataT$Grade == "WP" & mydataT$Course.Name == classT |
                      mydataT$Grade == "WE" & mydataT$Course.Name == classT, ])
totTs <- (ATs + BTs + CTs + DTs + FTs) / 100
ACs <- nrow(mydataC[mydataC$Grade == "A", ])
BCs <- nrow(mydataC[mydataC$Grade == "B", ])
CCs <- nrow(mydataC[mydataC$Grade == "C", ])
DCs <- nrow(mydataC[mydataC$Grade == "D", ])
FCs <- nrow(mydataC[mydataC$Grade == "F", ])
WCs <- nrow(mydataC[mydataC$Grade == "W" | mydataC$Grade == "WF" | 
                      mydataC$Grade == "WP" |mydataC$Grade == "WE" , ])
totCs <- (ACs + BCs + CCs + DCs + FCs) / 100
gradedistr <- data.frame(Treatment = rep(c("090 Cohort", "Control Group"), each = 5),
              Grade = rep(c("A", "B", "C", "D", "F"), 2), 
              Percent = c(ATs/totTs, BTs/totTs, CTs/totTs, DTs/totTs, FTs/totTs, ACs/totCs, BCs/totCs, CCs/totCs, DCs/totCs, FCs/totCs))
              #Percent = c(ATs, BTs, CTs, DTs, FTs, ACs, BCs, CCs, DCs, FCs))
jpeg("FullSBS.jpg") #saves side by side comparison of groups as jpeg
ggplot(gradedistr, aes(Grade, Percent, fill = Treatment)) + geom_bar(stat = "identity", position = position_dodge()) + labs(x = "Final Grade in Course", y = "Percentage of Students") + theme_minimal() + scale_fill_brewer(palette = "Greens") + ylim(0, 100)
#ggboxplot(gradedistr, x = "treatment", y = "Percent", ylab = "Grade", xlab = "Groups", add = "jitter")
dev.off() #closes file
As <- nrow(mydataT[mydataT$Grade == "A" & mydataT$Course.Name == "CHM-090", ])
Bs <- nrow(mydataT[mydataT$Grade == "B" & mydataT$Course.Name == "CHM-090", ])
Cs <- nrow(mydataT[mydataT$Grade == "C" & mydataT$Course.Name == "CHM-090", ])
Ds <- nrow(mydataT[mydataT$Grade == "D" & mydataT$Course.Name == "CHM-090", ])
Fs <- nrow(mydataT[mydataT$Grade == "F" & mydataT$Course.Name == "CHM-090", ])
Ws <- nrow(mydataT[mydataT$Grade == "W" & mydataT$Course.Name == "CHM-090"| 
                      mydataT$Grade == "WF" & mydataT$Course.Name == "CHM-090" | 
                      mydataT$Grade == "WP" & mydataT$Course.Name == "CHM-090" |
                      mydataT$Grade == "WE" & mydataT$Course.Name == "CHM-090", ])
tots <- (As + Bs + Cs + Ds + Fs) / 100
Distr090 <- data.frame(Treatment = rep(c(labelstwo, "090 Cohort in 090"), each = 5),
                         Grade = rep(c("A", "B", "C", "D", "F"), 2), 
                         Percent = c(ATs/totTs, BTs/totTs, CTs/totTs, DTs/totTs, FTs/totTs, As/tots, Bs/tots, Cs/tots, Ds/tots, Fs/tots))
jpeg("090vs090.jpg")
ggplot(Distr090, aes(Grade, Percent, fill = Treatment)) + geom_bar(stat = "identity", position = position_dodge()) + labs(x = "Final Grade in Course", y = "Percentage of Students") + theme_minimal() + scale_fill_brewer(palette = "Greens") + ylim(0, 100)
dev.off()
#rentention rates and student success
rent <- data.frame(Treatment = c("090 Cohort", labels),
                   Group = c("090 Cohort", labels),
                   Percent = c(100 - WTs / (totTs + WTs / 100), 100 - WCs / (totCs + WCs / 100)))
jpeg("Retention.jpg") #saves image as JPG
ggplot(rent, aes(Group, Percent, fill = Treatment)) + geom_bar(stat = "identity", position = position_dodge()) + labs(x = "Cohort", y = "Percentage of Students") + theme_minimal() + scale_fill_brewer(palette = "Greens") + ylim(0, 100)
dev.off() #closes file
success <- data.frame(Treatment = c("090 Cohort", labels),
                   Group = c("090 Cohort", labels),
                   Percent = c((ATs + BTs + CTs) / (totTs), (ACs + BCs + CCs) / (totCs)))
jpeg("Success.jpg") #saves image as JPG
ggplot(success, aes(Group, Percent, fill = Treatment)) + geom_bar(stat = "identity", position = position_dodge()) + labs(x = "Cohort", y = "Percentage of Students") + theme_minimal() + scale_fill_brewer(palette = "Greens") + ylim(0, 100)
dev.off() #closes file
rent <- data.frame(Treatment = c(labelstwo, "090 Cohort in 090"),
                   Group = c("090 Cohort", labelstwo),
                   Percent = c(100 - WTs / (totTs + WTs / 100), 100 - Ws / (tots + Ws / 100)))
jpeg("Retention090.jpg") #saves image as JPG
ggplot(rent, aes(Group, Percent, fill = Treatment)) + geom_bar(stat = "identity", position = position_dodge()) + labs(x = "Cohort", y = "Percentage of Students") + theme_minimal() + scale_fill_brewer(palette = "Greens") + ylim(0, 100)
dev.off() #closes file
#does the analysis for the matched groups
mydataT <- read.csv("MatchedTreatment.csv")
mydataC <- read.csv("MatchedControl.csv")
ATs <- nrow(mydataT[mydataT$Grade == "A", ])
BTs <- nrow(mydataT[mydataT$Grade == "B", ])
CTs <- nrow(mydataT[mydataT$Grade == "C", ])
DTs <- nrow(mydataT[mydataT$Grade == "D", ])
FTs <- nrow(mydataT[mydataT$Grade == "F", ])
WTs <- nrow(mydataT[mydataT$Grade == "W/WF/WP/WE", ])
totTs <- (ATs + BTs + CTs + DTs + FTs) / 100
ACs <- nrow(mydataC[mydataC$Grade == "A", ])
BCs <- nrow(mydataC[mydataC$Grade == "B", ])
CCs <- nrow(mydataC[mydataC$Grade == "C", ])
DCs <- nrow(mydataC[mydataC$Grade == "D", ])
FCs <- nrow(mydataC[mydataC$Grade == "F", ])
WCs <- nrow(mydataC[mydataC$Grade == "W/WF/WP/WE", ])
totCs <- (ACs + BCs + CCs + DCs + FCs) / 100
matchedgradedistr <- data.frame(Treatment = rep(c("090 Cohort", "Matched Control Group"), each = 5),
                         Grade = rep(c("A", "B", "C", "D", "F"), 2),
                         Percent = c(ATs/totTs, BTs/totTs, CTs/totTs, DTs/totTs, FTs/totTs, ACs/totCs, BCs/totCs, CCs/totCs, DCs/totCs, FCs/totCs))
jpeg("MatchedFullSBSPSM.jpg") #saves side by side comparison of groups as jpeg
ggplot(matchedgradedistr, aes(Grade, Percent, fill = Treatment)) + geom_bar(stat = "identity", position = position_dodge()) + labs(x = "Final Grade in Course", y = "Percentage of Students") + theme_minimal() + scale_fill_brewer(palette = "Greens") + ylim(0, 100)
dev.off() #closes file
matchsuccess <- data.frame(Treatment = c("090 Cohort", "Matched Cohort"),
                      Group = c("090 Cohort", "168 Control Group"),
                      Percent = c((ATs + BTs + CTs) / (totTs), (ACs + BCs + CCs) / (totCs)))
jpeg("MatchedSuccess.jpg") #saves image as JPG
ggplot(matchsuccess, aes(Group, Percent, fill = Treatment)) + geom_bar(stat = "identity", position = position_dodge()) + labs(x = "Cohort", y = "Percentage of Students") + theme_minimal() + scale_fill_brewer(palette = "Greens") + ylim(0, 100)
dev.off() #closes file
matchedrent <- data.frame(Treatment = c("090 Cohort", "Matched Cohort"),
                   Group = c("090 Cohort", labels),
                   Percent = c(100 - WTs / (totTs + WTs / 100), 100 - WTs / (totTs + WTs / 100)))
jpeg("MatchedRetention090.jpg") #saves image as JPG
ggplot(matchedrent, aes(Group, Percent, fill = Treatment)) + geom_bar(stat = "identity", position = position_dodge()) + labs(x = "Cohort", y = "Percentage of Students") + theme_minimal() + scale_fill_brewer(palette = "Greens") + ylim(0, 100)
dev.off() #closes file

