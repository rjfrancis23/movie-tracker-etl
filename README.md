# _"Dazzling images...on a huge silver screen."_
# Trending Movies Tracker 🎬 🪩
🚧 🔨 **UNDER CONSTRUCTION** 🔨 🚧

## Project Overview
As an enthusiastic movie-watcher, I was curious to know (especially as we head into awards season🏆) what movies are most popular based on the number of people who are watching at any given time. To answer this simple question I built out a basic data pipeline that pulls down watch data each hour (via [Trakt API](https://trakt.docs.apiary.io/#)), loads it to the Google Cloud Platform, and updates a dashboard with the top 20 most-watched movies that hour. A system design diagram and more details on the components of the pipeline can be found below. [View the live dashboard here](https://lookerstudio.google.com/reporting/3bb990d1-2280-4f51-915b-ed23d286d416).

![image](https://github.com/rjfrancis23/movie-tracker-etl/assets/110854287/dcd21f94-bf09-4a42-a60a-41b3d3eb7f4e)
_Static view of dashboard. View live version [here](https://lookerstudio.google.com/reporting/3bb990d1-2280-4f51-915b-ed23d286d416)._

### System Design 
Below is a diagram of the basic pipeline design. 
![image](https://github.com/rjfrancis23/movie-tracker-etl/assets/110854287/6a41337f-1216-4e54-bba4-c07c0782a3c6)

### To-dos and Goals 
