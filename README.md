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

