# Logs Analysis
Logs analysis is a basic python code connected to database acts as a reporting tool that will use 
information from the database to discover what kind of articles the site's readers like. 
  -- this is project is part of the [full stack web developer nano degree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004) by *Udacity* --

## Prerequisities
- [python 3.6](https://www.python.org)
- [postgreSQL database](https://www.postgresql.org)
- [psycopg2](http://initd.org/psycopg/)

## Installation
- download the data [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
- run  `psql -d news -f newsdata.sql`.
- run the logs_analysis.py file.
- open localhost:8000 in your browser

## output
![output](https://github.com/KarimTawfik17/Logs-Analysis/blob/master/output.PNG)

### Database views definitions
we created one view called popular_articles for making queries simpler 
```sql
create view popular_articles as
            select articles.title, count(*) as views
            from articles, log
            where log.path like concat('%', articles.slug )
            group by articles.title
            order by views desc ;
```

### Authors
- Karim Tawfik