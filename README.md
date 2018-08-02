# Analyze cinema industry with MongoDB and Python
Small code that explains how to merge 3 datasets into one with MongoDb Compass and save it as a separate table in a database. Datasets are taken from Unesco, World Bank and  Numbeo. Files are available at the repository.<br>

The idea is to analyze the film industry a little bit, compare the state of cinema industry across countries all over the world and analyze the correlation between variables. Hypotheses are:<br /><br />



- Hypothesis 1
1. H1: there is a relationship between population grows and ticket sold
2. H0: there is no relationship between population grows and ticket sold.<br /><br />



- Hypothesis 2
1. H1: there is a positive relationship between GDP and number of cinemas per country
2. H0: there is no relationship between GDP and number of cinemas per country <br /><br />



- Hypothesis 3
1. H1: People who live in developed country buy more tickets in cinema
2. H0: People who live in developed country do not buy more tickets in cinema <br /><br />

## MongoDB

**Start a MongoDB shell**

[Reference on StackOverflow](https://stackoverflow.com/questions/42739166/could-not-connect-to-mongodb-on-the-provided-host-and-port?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa)

1. Create folder "C:\data\db"
2. access "mongod" in bin folder of MongoDB to set up the MongoDB on a machine and establish connection
3. access "mongo" in bin folder of MongoDB to start shell

**Create a database**

`use project`

>switched to db project

**Add collections (tables) to a database**

```
db.createCollection("unesco")
db.createCollection("numbeo")
db.createCollection("worldbank")
```

>{ "ok" : 1 }

`show collections`

>unesco  
>numbeo  
>worldbank  

**Fill collections with data. Data is stored in csv (through command line)**

```
mongoimport --db georgian --collection unesco --type csv --headerline --file “D:/mongodb/DatasetsFilm/unesco.csv"  
mongoimport --db georgian --collection numbeo --type csv --headerline --file “D:/mongodb/DatasetsFilm/tickets.csv"  
mongoimport --db georgian --collection worldbank --type csv --headerline --file “D:/mongodb/DatasetsFilm/worldbank.csv"  
```

**First merge (unesco with worldbank)**

Mutual field is "country"

```db.createCollection("merged_one")
db.worldbank.aggregate([{$lookup: {from: "unesco",localField: "country",foreignField: "country",as: "cinemas"}},{$out : "merged_one"}])
```

**Second merge (first merge with worldbank)**

Mutual field is "country"

```db.createCollection("merged_two")
db.merged_one.aggregate([{$lookup: {from: "numbeo",localField: "country",foreignField: "country",as: "ticket_price"}},{$out : "merged_two"}])
```

**Export collection as json**

```
mongoexport --db georgian --collection merged_two --out “C:/Users/alexa/Desktop/GC/GC2/Data collection and curation/mongodb/merged_t.json"
```

## Python code and data analysis

**Create dataframe by extracing data from json**

```
import pandas as pd
import json
countries=[]
admissions=[]
ticket_prices=[]
gdp_s=[]
gdp_per_capita=[]
population=[]
cinemas=[]
for line in open("C:/Users/alexa/Desktop/GC/GC2/Data collection and curation/mongodb/merged_t.json", 'r'):
    #lines.append(line)
    js = json.loads(line)
    countries.append(js['country'])
    gdp_s.append(js['gdp'])
    gdp_per_capita.append(js['gdp_capita'])
    population.append(js['population'])
    admissions.append(js['cinemas'][0]['admiss'])
    cinemas.append(js['cinemas'][0]['cinemas'])
    ticket_prices.append(js['ticket_price'][0]['ticket_price'])
    
dict={}

dict["countries"] = countries
dict["admissions"] = admissions
dict["ticket_prices"] = ticket_prices
dict["gdp_s"] = gdp_s
dict["gdp_per_capita"] = gdp_per_capita
dict["population"] = population
dict["cinemas"] = cinemas

df = pd.DataFrame(data=dict)
```

![Alt text](https://github.com/oleksandrkim/Analyze-cinema-industry-with-MongoDB-and-Python/blob/master/Screenshot_1.png "Optional title")

## Question 1

###### Hypothesis: There is a relationship between population grows and ticket sold

**Create new column (number of tickets sold) required for hypothesis testing**

`df['tickets_sold '] = df.apply(lambda row: row['admissions'] / row['ticket_prices'], axis=1)`

**Remove outliers - 68-95-99 rule is applied on "admission" column**  
Countries to remove - Brazil, China, Mexico, Republic of Korea, Russia, US

```
df = df[(df['countries'] != 'Brazil') & (df['countries'] != 'China') & 
        (df['countries'] != 'Mexico') & (df['countries'] != 'Republic of Korea') &
        (df['countries'] != 'Russian Federation') & (df['countries'] != 'United States of America')]
```

**Calculate correlation and p-value**

```df['tickets_sold'].corr(df['population'])```

>0.73

```
from scipy.stats import ttest_ind
ttest_ind(df['tickets_sold'], df['population'])
```

>Ttest_indResult(statistic=-5.396667468504574, pvalue=3.0475777179812855e-07)

In summary, p-value is < 0.05, cinsequently there is a relationship between number of tickets sold and population;  

Conclusion: 
Film companies, when entering a market of a company, do not need to take the consideration the population because the number of tickets sold per person is the almost the same across countries of the world. 
 

## Question 2

###### Hypothesis: There is a positive relationship between GDP and number of cinemas per country

```df['cinemas'].corr(df['gdp_s'])```

>0.76

```ttest_ind(df['cinemas'], df['gdp_s'])```

>Ttest_indResult(statistic=-4.313915342388997, pvalue=3.117987914035751e-05)

In summary, p-value is < 0.05, cinsequently there is a relationship between number of cinemas and GDP;  

## Question 3

###### Hypothesis: People who live in developed country buy more tickets in cinema

**Create a column with ration "tickets sold" to population**

```df['tickets_population_ratio'] = df.apply(lambda row: row['tickets_sold'] / row['population'], axis=1)```  

Top-10 countries with the highest tickets sold to population ration:  

```
df.sort_values('tickets_population_ratio', ascending=False)['countries'].head(10)
```

>43    Malaysia   
>30    Cuba       
>61    Singapore  
>3     Belarus    
>48    New Zealand  
>29    Iceland    
>12    Colombia   
>13    Costa Rica  
>6     Australia  
>21    Estonia 
 
In summary, top 10 countries are not those that are considered as first-world countries by Nationsonline   
http://www.nationsonline.org/oneworld/first_world.htm

## Summary  
Hypotheses 1 and 2 were not rejected, while the 3rd one was rejected
