import httpx
from fastmcp import FastMCP


ifsc_server = FastMCP("IFSCSERVER")

@ifsc_server.tool
async def fetch_ifsc_details(ifsc_code: str) -> dict:
    """
    Fetch IFSC code details from Razorpay public API.

    Args:
        ifsc_code (str): Example - 'HDFC0000001'

    Returns:
        dict: IFSC code details or error message.
    """
    url = f"https://ifsc.razorpay.com/{ifsc_code}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Invalid IFSC code or request failed. Status code: {response.status_code}"}


@ifsc_server.tool
async def get_weather(location: str) -> dict:
    """
    Get current temperature for a given location using Open-Meteo API.

    Args:
        location (str): Example - "Delhi, India"

    Returns:
        dict: Dictionary with temperature info or error message.
    """
    # Use Open-Meteo's geocoding to get latitude and longitude
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={location}"
    
    async with httpx.AsyncClient() as client:
        geo_response = await client.get(geo_url)
        if geo_response.status_code != 200:
            return {"error": "Location geocoding failed."}
        
        geo_data = geo_response.json()
        if not geo_data.get("results"):
            return {"error": "Location not found."}
        
        lat = geo_data["results"][0]["latitude"]
        lon = geo_data["results"][0]["longitude"]
        
        # Now fetch weather using coordinates
        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
        )
        weather_response = await client.get(weather_url)
        if weather_response.status_code != 200:
            return {"error": "Weather data fetch failed."}
        
        weather_data = weather_response.json()
        temperature = weather_data.get("current_weather", {}).get("temperature")

        if temperature is not None:
            return {
                "location": location,
                "temperature_celsius": temperature
            }
        else:
            return {"error": "Temperature data not available."}



if __name__ == "__main__":
    ifsc_server.run("streamable-http", host = "0.0.0.0", port = 8000)