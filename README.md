# FINLEARN:

---

The financial analysis tool that continues to learn. Fin learn is a price prediction app that utilizes over 100 different sources and thousands of data points. Everything from the types of articles posted to weather, to general mental health.

I use social media apps to gauge the general mental health of society. The way I do that is gauge the kinds of posts that are posted each day. Then my algorithm uses a scale between 5 to -5. Once The social state is determined the algorithm checks big box retail stores to see how many reviews have been left and uses the review counts + their sentiment to check for correlation between volume of stocks and online shopping. The idea is that "buyers fever" floods over into the market and causes key stocks to go up.

Then from there there is a lot more intellectual property that I can't share publically but I can say there is over 100 technical indicators, 3000 links and AI as well as Deep Neural Networks at work determining stock movement.

Also, since most of the analysis is focused on minute data, my price predictor is making predictions an hour to 24 hours in advance and predicting just the next 3 days.

---

> TODO: Finish building the database connection so I can workon the data accumulation and get the data collection up and running.

> I am currently working on the Quote and Fundamental classes. I want to make each one of them have their own implementation of `execute_main`. The goal is to make each one self sufficient, only requiring the stocks list at the time of instantiation.

    > This way I can simply import both `Fundamental` and `Quote` to the main script, along with `_select_symbols()` and be able to instantiate them on the home page. And by doing so, I will have created the `stock_chunk` list. It will also have the ability to insert data into the database.

- There may be a better way though. Create an `interface`. one that takes in the stock list, chunks the data, creates a `markedata` database `engine`, and has the insert_into_database methods built into it. This will allow both Fundamental and Quote to inherit from this interface and use the methods which allows for them to be instantiated once.

- OR, I build an interface class that has two "subclasses" Quote and Fundamental so that the nothing gets instantiated more than necessary.
