from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


def load_weather_current(data, engine):
    try:
        with engine.begin() as connection:
            connection.execute(text("""INSERT INTO weather_current 
                                    (fetched_at, temperature, humidity, wind_speed, precipitation, weather_code) 
                                    VALUES 
                                    (:fetched_at, :temperature, :humidity, :wind_speed, :precipitation, :weather_code)"""),
                                    data)
    except SQLAlchemyError as error:
        print(f"Database error loading weather current: {error}")


def load_weather_forecast(data, engine):
    try:
        with engine.begin() as connection:
            connection.execute(text("""INSERT INTO weather_forecast 
                                    (fetched_at, forecast_date, temp_max, temp_min, sunrise_time, sunset_time, precipitation_sum, uv_index_max, weather_code) 
                                    VALUES 
                                    (:fetched_at, :forecast_date, :temp_max, :temp_min, :sunrise_time, :sunset_time, :precipitation_sum, :uv_index_max, :weather_code)"""),
                                    data)
    except SQLAlchemyError as error:
        print(f"Database error loading weather forecast: {error}")


def load_news_data(data, engine):
    try:
        with engine.begin() as connection:
            connection.execute(text("""INSERT INTO news_data 
                                    (fetched_at, source_name, author, title, article_description, article_url, published_at, category) 
                                    VALUES 
                                    (:fetched_at, :source_name, :author, :title, :article_description, :article_url, :published_at, :category)
                                    ON CONFLICT
                                    (article_url)
                                    DO NOTHING"""),
                               data)
    except SQLAlchemyError as error:
        print(f"Database error loading news data: {error}")


def load_stocks_data(data, engine):
    try:
        with engine.begin() as connection:
            connection.execute(text("""INSERT INTO stocks_data 
                                    (fetched_at, ticker, trade_date, open_price, high_price, low_price, close_price, volume) 
                                    VALUES 
                                    (:fetched_at, :ticker, :trade_date, :open_price, :high_price, :low_price, :close_price, :volume)
                                    ON CONFLICT 
                                    (ticker, trade_date) 
                                    DO NOTHING"""),
                               data)
    except SQLAlchemyError as error:
        print(f"Database error loading stocks data: {error}")


if __name__ == "__main__":
    import time
    from etl.utils.db_connection import get_engine
    from etl.extractors.weather_extractor import fetch_weather_data
    from etl.extractors.news_extractor import fetch_news_data
    from etl.extractors.stocks_extractor import fetch_stocks_data, TICKERS
    from etl.transformers.weather_transformer import transform_weather_current, transform_weather_forecast
    from etl.transformers.news_transformer import transform_news
    from etl.transformers.stocks_transformer import transform_stocks

    engine = get_engine()

    raw = fetch_weather_data()
    load_weather_current(transform_weather_current(raw), engine)
    load_weather_forecast(transform_weather_forecast(raw), engine)
    print("Weather data loaded successfully")

    for category in ["technology", "business", "science", "health"]:
        raw_news = fetch_news_data(category)
        load_news_data(transform_news(raw_news, category), engine)
        print(f"{category} news loaded successfully")

    for ticker in TICKERS:
        raw_stocks = fetch_stocks_data(ticker)
        load_stocks_data(transform_stocks(raw_stocks), engine)
        print(f"{ticker} loaded successfully")
        time.sleep(2)