Industrial IOT Dashboard

Borrowed heavily from https://github.com/adilmoujahid/kaggle-talkingdata-visualization please attribute

#Dependencies

Postgres, R (dplyr, RPostgreSQL packages), and  ```Python``` 2.7.x and 3 ```Python``` libraries: ```Pandas```, ```Flask```, ```Shapely```.

The easiest way to install ```Pandas``` is to install it as part of the [Anaconda distribution](https://www.continuum.io/downloads).

You can install ```Flask``` and ```Shapely``` using ```pip```.

```
pip install flask shapely psycopg2 urlparse
```

#How to run the code

1. Install all Python, R, and Postgres dependencies
2. Make sure that postgres database is running 
3. Update postgres access strings in R and app.py
4. Run R code to seed the database
5. From the root folder, run ```python app.py```


NOTE: events data is from the dataset ( events.csv) from [Kaggle](https://www.kaggle.com/c/talkingdata-mobile-user-demographics/data). You need to create a Kaggle account and agree to the competition rules to download the data.


