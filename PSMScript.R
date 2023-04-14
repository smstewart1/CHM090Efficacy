library(tidyverse)
library(MatchIt)
library(dplyr)
library(ggplot2)
library(gridExtra)
library(ggpubr)
#stuff that needs to be changed
psmfile <- "151PSM.csv"
treatmentfile <- "151with090.csv"
controlfile <- "151sans090.csv"
mydata <- read.csv(psmfile)
mydata %>% #calculates the raw GPAs of students in and out of the control group
  group_by(treatment) %>% 
  summarize(N = n(), mean_math = mean(Grade), std_err = sd(Grade)/sqrt(N))
with(mydata, t.test(Grade ~ treatment)) #gets the raw t-test results
covariates <- c('Term', 'DelMet', 'Gender', 'Ethnicity', 'EMI') #lists the covariates
#build up propensity scores using a logit model
propscore <- glm(treatment ~ Term + DelMet + Gender + Ethnicity + EMI, family = binomial(), data = mydata)
summary(propscore) #saves the PSs 
studentscores <- data.frame(PMS = predict(propscore, type = "response"), treatment = propscore$model$treatment) #calculate PSs for all students
#finding the region of common support
labs <- paste("090 Status:", c("Attended", "Did not Attend 090"))
studentscores %>%
  mutate(treatment = ifelse(treatment == 1, labs[1], labs[2])) %>%
  ggplot(aes(x = PMS)) +  geom_histogram(color = "white") +  facet_wrap(~treatment) + xlab("Propensity Score") + theme_bw()
#executing a matching algorithm
studentdata <- mydata %>% select(Grade, treatment, one_of(covariates)) %>% na.omit() #clears out any NA data
mod_match <- matchit(treatment ~ Term + DelMet + Gender + Ethnicity + EMI, method = "nearest", data = studentdata) #executes a matching algorithm
#visual inspection of the matches
#plot(mod_match)
summary(mod_match)
data_matched <- match.data(mod_match) #dataframe of matched data
#function for estimating data balance
fn_bal <- function(dta, variable) {
  dta$variable <- dta[, variable]
  dta$treatment <- as.factor(dta$treatment)
  support <- c(min(dta$variable), max(dta$variable))
  ggplot(dta, aes(x = distance, y = variable, color = treatment)) +
    geom_point(alpha = 0.2, size = 1.3) +
    geom_smooth(method = "loess", se = F) +
    xlab("Propensity score") + ylab(variable) + theme_bw() + ylim(support)
}
#visualization of the matched data
grid.arrange(
  fn_bal(data_matched, "Term"),
  fn_bal(data_matched, "DelMet") + theme(legend.position = "none"),
  fn_bal(data_matched, "Gender"),
  fn_bal(data_matched, "Ethnicity") + theme(legend.position = "none"),
  fn_bal(data_matched, "EMI"),
  nrow = 3, widths = c(1, 0.8)
)
#difference-in-means 
data_matched %>% group_by(treatment) %>% select(one_of(covariates)) %>% summarise_all(funs(mean))

#calculates differences between the matched and unmatched groups
with(data_matched, t.test(Grade ~ treatment)) #straight t test
#print the distribution
ggboxplot(data_matched, x = "treatment", y = "Grade", ylab = "Grade", xlab = "Groups", add = "jitter")
#lm_treat1 <- lm(Grade ~ treatment, data = data_matched) #t-test without covariates
#summary(lm_treat1)
#lm_treat2 <- lm(Grade ~ treatment + Term + Ethnicity + DelMet + EMI + Gender, data = data_matched) #t-test with covariates 
#summary(lm_treat2)

