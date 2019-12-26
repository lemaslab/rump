# boxplot for matched files

data = read.csv("../results/allgroups_GLib_merged.csv")

for (i in 1:nrow(data)){
  foo <- data.frame(color=c("fat_anova","skim_anova","whole_anova"),
                   mean.temp=c(data[i,]$mean_fat_anova,data[i,]$mean_skim_anova,data[i,]$mean_whole_anova),
                   sd=c(data[i,]$sd_fat_anova,data[i,]$sd_skim_anova,data[i,]$sd_whole_anova))
  jpeg(paste("../figs/", data[i,]$row_ID, gsub("/", "_OR_", data[i,]$Name), data[i,]$M.Z, data[i,]$Retention, ".jpeg", sep = ""), res = 80, quality = 80)
  plot(1:3,foo$mean.temp,pch=19,xlab="",ylab="",xaxt="n",xlim=c(0.5,3.5),
      ylim=c(min(foo$mean.temp-foo$sd),max((foo$mean.temp+foo$sd))))
  lines(rbind(1:3,1:3,NA),rbind(foo$mean.temp-foo$sd,foo$mean.temp+foo$sd,NA))
  axis(side=1,at=1:3,labels=c("fat_anova", "skim_anova", "whole_anova"))
  Corner_text <- function(text, location="bottomright"){
     legend(location,legend=text, bty ="n", pch=NA) 
  }
  Corner_text(text=paste("p_value_f_anova: ", data[i,]$p_value_f_anova, "\n", "metabolite name: ", data[i,]$Name, sep=""))
  dev.off()
}