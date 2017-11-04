import psycopg2
from flask import Flask
app = Flask(__name__)

list_item = "<li> %s ________ %s %s.</li>"

html_text = '''
<!DOCTYPE html>
<html>
   <head>
      <title>Logs Analysis</title>
      <style>
         h1 { text-align: center; color: red; }
         li { color: blue; }
         p,ul { width: 400px; }
         p,ul { margin-left: 50px; }
      </style>
   </head>
   <body>
      <h1>Logs Analysis</h1>
      <p>1. What are the most popular three articles of all time? </p>
      <ul>
         %s
      </ul>
      <p>2. Who are the most popular article authors of all time? </p>
      <ul>
         %s
      </ul>
      <p>3. On which days did more than 1%% of requests lead to errors?</p>
      <ul>
         %s
      </ul>
   </body>
</html>
'''


def make_view():
  """creates the view popular articles if it doesn't exist"""
  connection = psycopg2.connect('dbname=news')
  c = connection.cursor()
  try:
    c.execute('''
        create view popular_articles as 
        select articles.title, count(*) as views
        from articles, log
        where log.path like concat('%', articles.slug )
        group by articles.title
        order by views desc ;
        ''')
    connection.commit()
  except:
    print("view is alread created !!")
  connection.close()


def get_popular_articles():
  """returns the most popular three articles of all time"""
  connection = psycopg2.connect('dbname=news')
  c = connection.cursor()
  c.execute('''
        select * from popular_articles limit 3;
        ''')

  results = c.fetchall()
  connection.close()
  # returns list of 3 tuples each tuple is pair of string and int
  results = [(results[i][0], int(results[i][1]))
             for i in range(len(results))]
  return "".join(list_item % (i, j, "views") for i, j in results)


def get_popular_authors():
  """returns the most popular articles authors of all time"""
  connection = psycopg2.connect('dbname=news')
  c = connection.cursor()
  c.execute('''
        select authors.name, sum(popular_articles.views) as total
        from articles, popular_articles, authors
        where popular_articles.title = articles.title
        and authors.id = articles.author
        group by authors.name order by total desc;
        ''')
  results = c.fetchall()
  connection.close()
  results = [(results[i][0], int(results[i][1]))
             for i in range(len(results))]
  return "".join(list_item % (i, j, "views") for i, j in results)


def get_more_than_one_percent_error_day():
  """returns days that with more than 1% of requests lead to errors"""
  connection = psycopg2.connect('dbname=news')
  c = connection.cursor()
  c.execute('''
        select a.day, (a.errors*100.0/b.requests*1.0)
        from
        (select date_trunc('day', time)
        as day , count(*) as errors from log where status != '200 OK'
        group by day) as a,
        (select date_trunc('day', time)
        as day , count(*) as requests from log group by day) as b
        where a.day = b.day and (a.errors*100.0/b.requests*1.0) >=1.0;
        ''')
  results = c.fetchall()
  connection.close()
  results = [(str(results[i][0]).split()[0], float(results[i][1]))
             for i in range(len(results))]
  return "".join(list_item % (i, round(j,2), "errors") for i, j in results)


@app.route('/', methods=['GET'])
def main():
  '''Main page of the application'''

  html = html_text % (get_popular_articles(), get_popular_authors(),
                      get_more_than_one_percent_error_day())
  return html


if __name__ == '__main__':
  make_view()
  app.run(host='0.0.0.0', port=8000)
