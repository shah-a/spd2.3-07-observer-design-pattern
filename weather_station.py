"""
Final Implementation of WeatherData.  Complete all the TODOs
"""


class Subject:
    # Both of the following two methods take an
    # observer as an argument; that is, the observer
    # to be registered ore removed.
    def registerObserver(observer):
        pass

    def removeObserver(observer):
        pass

    # This method is called to notify all observers
    # when the Subject's state (measuremetns) has changed.
    def notifyObservers():
        pass

# The observer class is implemented by all observers,
# so they all have to implemented the update() method. Here
# we're following Mary and Sue's lead and
# passing the measurements to the observers.


class Observer:
    def update(self, temp, humidity, pressure):
        pass

# WeatherData now implements the subject interface.


class WeatherData(Subject):
    def __init__(self):
        self.observers = []
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0

    def registerObserver(self, observer):
        # When an observer registers, we just
        # add it to the end of the list.
        self.observers.append(observer)

    def removeObserver(self, observer):
        # When an observer wants to un-register,
        # we just take it off the list.
        self.observers.remove(observer)

    def notifyObservers(self):
        # We notify the observers when we get updated measurements
        # from the Weather Station.
        for ob in self.observers:
            ob.update(self.temperature, self.humidity, self.pressure)

    def measurementsChanged(self):
        self.notifyObservers()

    def setMeasurements(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure

        self.measurementsChanged()

    # other WeatherData methods here.


class CurrentConditionsDisplay(Observer):
    def __init__(self, weatherData):
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0

        self.weatherData = weatherData  # save the ref in an attribute.
        weatherData.registerObserver(self)  # register the observer
        # so it gets data updates.

    def update(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.display()

    def display(self):
        print("Current conditions:", self.temperature,
              "F degrees and", self.humidity, "[%] humidity",
              "and pressure", self.pressure)
        print()


class ForecastDisplay(Observer):
    def __init__(self, weatherData):
        self.temperature = 0
        self.humidity = 0
        self.pressure = 0

        self.weatherData = weatherData  # save the ref in an attribute.
        weatherData.registerObserver(self)  # register the observer
        # so it gets data updates.

    def update(self, temperature, humidity, pressure):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.display()

    def calc_forecast(self):
        forecast_temperature = self.temperature + \
            0.11 * self.humidity + 0.2 * self.pressure
        forecast_humidity = self.humidity - 0.9 * self.humidity
        forecast_pressure = self.pressure + 0.1 * \
            self.temperature - 0.21 * self.pressure
        return (round(forecast_temperature, 2), round(forecast_humidity, 2), round(forecast_pressure, 2))

    def display(self):
        forecast_temperature, forecast_humidity, forecast_pressure = self.calc_forecast()
        print("Forecast conditions:", forecast_temperature,
              "F degrees and", forecast_humidity, "[%] humidity",
              "and pressure", forecast_pressure)
        print()


class StatisticsDisplay(Observer):
    def __init__(self, weatherData):
        self.temperature_values = []
        self.humidity_values = []
        self.pressure_values = []

        # save the ref in an attribute and register the observer so it gets data updates.
        self.weatherData = weatherData
        weatherData.registerObserver(self)

    def update(self, temperature, humidity, pressure):
        self.temperature_values.append(temperature)
        self.humidity_values.append(humidity)
        self.pressure_values.append(pressure)
        self.display()

    def calc_min_max_avg(self, values):
        return (min(values), max(values), sum(values) / len(values))

    def get_min_max_avg(self):
        temp_min_max_avg = self.calc_min_max_avg(self.temperature_values)
        humidity_min_max_avg = self.calc_min_max_avg(self.humidity_values)
        pressure_min_max_avg = self.calc_min_max_avg(self.pressure_values)
        return (temp_min_max_avg, humidity_min_max_avg, pressure_min_max_avg)

    def display(self):
        stats = self.get_min_max_avg()
        print("Weather Statistics:")
        print("Temperature:", end=" ")
        print("\tMin:", round(stats[0][0], 2), end=" ")
        print("\tMax:", round(stats[0][1], 2), end=" ")
        print("\tAvg:", round(stats[0][2], 2))
        print("Humidity:", end=" ")
        print("\tMin:", round(stats[1][0], 2), end=" ")
        print("\tMax:", round(stats[1][1], 2), end=" ")
        print("\tAvg:", round(stats[1][2], 2))
        print("Pressure:", end=" ")
        print("\tMin:", round(stats[2][0], 2), end=" ")
        print("\tMax:", round(stats[2][1], 2), end=" ")
        print("\tAvg:", round(stats[2][2], 2))
        print()


class WeatherStation:
    def main(self):
        weather_data = WeatherData()

        current_display = CurrentConditionsDisplay(weather_data)
        statistics_display = StatisticsDisplay(weather_data)
        forecast_display = ForecastDisplay(weather_data)

        weather_data.setMeasurements(80, 65, 30.4)
        weather_data.setMeasurements(82, 70, 29.2)
        weather_data.setMeasurements(78, 90, 29.2)

        # un-register the observer
        weather_data.removeObserver(current_display)
        weather_data.removeObserver(statistics_display)
        weather_data.setMeasurements(120, 100, 1000)


if __name__ == "__main__":
    w = WeatherStation()
    w.main()
