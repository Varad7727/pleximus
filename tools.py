import requests

def calculator(expression: str) -> str:
    """Evaluates a basic mathematical expression.
    
    Args:
        expression: The math expression to evaluate, e.g., '25 * 18'.
    """
    try:
        # Safe evaluation of basic mathematical expressions
        allowed_chars = set("0123456789+-*/(). %")
        if not all(char in allowed_chars for char in expression):
            return "Invalid characters in mathematical expression."
        result = eval(expression)
        return str(result)
    except Exception:
        return "Invalid mathematical expression."

def weather(latitude: float, longitude: float) -> str:
    """Gets the current weather for a given latitude and longitude.
    
    Args:
        latitude: Latitude of the location (e.g., 19.0760 for Mumbai).
        longitude: Longitude of the location (e.g., 72.8777 for Mumbai).
    """
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={latitude}&longitude={longitude}&current_weather=true"
        )
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return "Failed to fetch weather data from API."
        
        data = response.json()
        current = data.get("current_weather", {})
        temp = current.get("temperature")
        wind = current.get("windspeed")
        return f"Temperature: {temp}°C, Wind Speed: {wind} km/h"
    except Exception as e:
        return f"Error retrieving weather: {str(e)}"

def text_utility(text: str, operation: str) -> str:
    """Performs string manipulations on text.
    
    Args:
        text: The input string.
        operation: The operation ('word_count', 'character_count', 'reverse', 'uppercase', 'lowercase').
    """
    if operation == "word_count":
        return f"Word count: {len(text.split())}"
    elif operation == "character_count":
        return f"Character count: {len(text)}"
    elif operation == "reverse":
        return f"Reversed text: {text[::-1]}"
    elif operation == "uppercase":
        return f"Uppercase: {text.upper()}"
    elif operation == "lowercase":
        return f"Lowercase: {text.lower()}"
    return "Invalid text operation. Use word_count, character_count, reverse, uppercase, or lowercase."

def wikipedia_summary(title: str) -> str:
    """Fetches a brief Wikipedia summary for a given topic or title.
    
    Args:
        title: The Wikipedia topic title (e.g., 'Python_(programming_language)').
    """
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}"
        headers = {"User-Agent": "PleximusAIHackathon/1.0 (student_project)"}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 404:
            return f"Wikipedia article '{title}' not found."
        elif response.status_code != 200:
            return "Failed to reach Wikipedia API."
            
        data = response.json()
        return data.get("extract", "No summary available.")
    except Exception as e:
        return f"Error fetching Wikipedia summary: {str(e)}"

def currency_converter(amount: float, from_currency: str, to_currency: str) -> str:
    """Converts money from one currency to another using live Frankfurter rates.
    
    Args:
        amount: The numeric amount to convert.
        from_currency: 3-letter source currency code (e.g., 'USD', 'EUR').
        to_currency: 3-letter target currency code (e.g., 'INR', 'GBP').
    """
    try:
        url = f"https://api.frankfurter.dev/v1/latest?amount={amount}&from={from_currency.upper()}&to={to_currency.upper()}"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return "Currency conversion failed. Check currency codes."
            
        data = response.json()
        converted_value = data.get("rates", {}).get(to_currency.upper())
        if converted_value is not None:
            return f"{amount} {from_currency.upper()} = {converted_value} {to_currency.upper()}"
        return "Could not retrieve exchange rate."
    except Exception as e:
        return f"Error converting currency: {str(e)}"