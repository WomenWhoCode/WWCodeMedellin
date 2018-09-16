import pandas as pd
#Import file
data = pd.read_csv("movie_metadata.csv", dtype={"title_year": str})
#Remove rows without release year data (title_year column)
data = data.dropna(subset=["title_year"])
#Replace duration missing elements with duration mean
data.duration = data.duration.fillna(data.duration.mean())
#Convert duration from float to integer
data.duration = pd.Series(data["duration"], dtype="int32")
#Filling empty rating elements with "Not Know"
data.content_rating = data.content_rating.fillna("Not Known")
#Rename columns with more intuitive names
data = data.rename(columns = {"title_year":"release_date", "movie_facebook_likes":"facebook_likes"})
#Uppercase and remove trailing spaces from titles
data.movie_title = data["movie_title"].str.upper()
data.movie_title = data["movie_title"].str.strip()
#Export data to .csv utf-8 encoding
data.to_csv("cleanfile.csv", encoding="utf-8")
