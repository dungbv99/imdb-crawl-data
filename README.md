#Crawl imdb data using Scrapy Spider

Replace this directory in file ./imdb/spiders/ImdbSpiders.py (line 42)

```
'DELTAFETCH_DIR': '/home/dung/PycharmProjects/imdb/delta_fetch'
```

with your directory, ```{your_project_dir}``` is your directory where this project placed (eg. ```/home/dung/PycharmProjects/imdb```):

```
'DELTAFETCH_DIR': '{yours_project_dir}/delta_fetch
```

### Install packages

```
pip install scrapy scrapy-deltafetch
```

#### If install ```scrapy-deltafetch``` error, run 

```
sudo apt install libdb-dev
pip3 install bsddb3
```

### Run crawler

```
cd {yours_project_dir}
python3 main.py
```