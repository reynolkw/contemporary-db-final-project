Kuyper Reynolds
IT 2055C
Brian Krahenbuhl
29 July 2024

# Final Project

## Database Platform
The database platform utilized in this application is MongoDB.

## Database Purpose
This database application answers the question: What's it like on top of Crosley Tower? Utilizing publicly available weather data via a JSON endpoint, it will poll and store weather data for the specific coordinates of Crosley Tower so that users can always know what the weather is like there.

The application will also feature a weather forecast using modern, commonly accepted techniques of weather forecasting... /s

## Database Model
```mermaid
erDiagram
    CROSLYWEATHER {
        WEATHER
        FORECAST
    }

    WEATHER {
        string _id
        object coord
        array weather
        string base
        object main
        number visibility
        object wind
        object clouds
        number dt
        object sys
        number timezone
        number id
        string name
        number cod
    }

    FORECAST {
        string _id
        string clouds
        string humidity
        number next_hour_temp_farenheit
        string temperature
        string visibility
        string wind
    }

    WEATHER_COORD {
        number lon
        number lat
    }

    WEATHER_WEATHER {
        number id
        string main
        string description
        string icon
    }

    WEATHER_MAIN {
        number temp
        number feels_like
        number temp_min
        number temp_max
        number pressure
        number humidity
        number sea_level
        number grnd_level
    }

    WEATHER_WIND {
        number speed
        number deg
    }

    WEATHER_CLOUDS {
        number all
    }

    WEATHER_SYS {
        number type
        number id
        string country
        number sunrise
        number sunset
    }

    CROSLYWEATHER ||--o{ WEATHER: "contains"
    CROSLYWEATHER ||--o{ FORECAST: "contains"
    WEATHER ||--o{ WEATHER_COORD: "has"
    WEATHER ||--o{ WEATHER_WEATHER: "has"
    WEATHER ||--o{ WEATHER_MAIN: "has"
    WEATHER ||--o{ WEATHER_WIND: "has"
    WEATHER ||--o{ WEATHER_CLOUDS: "has"
    WEATHER ||--o{ WEATHER_SYS: "has"
```

## Reflection
I've completed many small projects in Python like this, so the biggest challenge was determining the purpose of the database application and sourcing data to demonstrate my ability to create, update, and delete documents in MongoDB. However, I found OpenWeather's free API, which allows 1,000 free daily calls. Combining this with the low-cost "gpt-3.5-turbo" chat completions endpoint that OpenAI offers allowed me to complete database operations with real-world data. Having dynamic data like this helps keep the project exciting and fun!

This project's most significant learning outcome is the absolute ease of use that MongoDB with Python drivers offers for quick development. I had database CRUD operations up and running within ten minutes of starting the project. This simplicity allowed me to focus on the logic and data processing to handle the application functionality instead of spending a ton of time writing entity models or database IO functionality.

In the future, I would be more specific about the data I store in the database to allow for longer retention of historical weather data. For this project, I leveraged MongoDB's ability to store any object in a document easily. However, to scale the application up, documents could be more efficient, allowing for less storage usage.
