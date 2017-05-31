#read in data from 
library(dplyr)
data(state)
locs = jsonlite::read_json("./input/locs.json")
out_loc = list()
for(i in 1:NROW(locs)){
  out_loc[[i]] = data.frame(latitude= locs[[i]]$lt, longitude = locs[[i]]$ln, 
                        address= locs[[i]]$a, city = locs[[i]]$c, state = locs[[i]]$s, zip = locs[[i]]$z)
  
}
out_loc = do.call("rbind", out_loc) %>% filter(state %in% state.abb)
locs = out_loc %>% filter(state %in% state.abb) %>% mutate(loc_id = paste0("a",base::sample(1:1e6,NROW(.))))
region = data.frame(st =  state.abb, region=state.region, div= state.division)
locs2 = locs %>% left_join(region, by= c("state" = "st"))
locs3 = data.frame(locs2, stringsAsFactors = F)

iot = read.csv("/Users/robertcrozier/Downloads/kaggle-talkingdata-visualization-master/input/events.csv", stringsAsFactors = FALSE)
iot2 = iot[sample(1:NROW(iot),100000),]
ind = base::sample(1:NROW(locs3), NROW(iot2), replace=TRUE)
iot2$longitude = locs3$longitude[ind]
iot2$latitude = locs3$latitude[ind]
iot2$location = locs3$div[ind]

brands = c(paste0("model", LETTERS[1:12]), "Other")
iot2$phone_brand_en = base::sample(brands, NROW(iot2), replace= TRUE)
iot2$gender = base::sample(c('Running As Expected','Failure: Water Leak', 'Failure: Vibrations'), NROW(iot2), replace= TRUE, prob = c(100,10,5))
ages = c( '22-','23-26','27-28','29-32','33-38','39+')
iot2$age_segment = base::sample(ages, NROW(iot2), replace= TRUE)

iot3 = iot2 %>% select(timestamp, longitude, latitude, phone_brand_en, gender, age_segment, location)
#write.csv(iot3,"./input/events.csv",row.names=F,quote=F)

library(RPostgreSQL)
drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname = "postgres",
                 host = "localhost", port = 5432,
                 user = "robertcrozier", password = 'password')

dbWriteTable(con, "iot", 
             value = iot3, append = TRUE, row.names = FALSE)
 
# query the data from postgreSQL 
df_postgres <- dbGetQuery(con, "SELECT * from iot")