
from tzwhere import tzwhere
from datetime import datetime
from pytz import timezone

night_color = (0, 0, 64)      # Dark blue for night
dawn_color = (255, 153, 51)   # Orange for dawn
day_color = (135, 206, 235)   # Light blue for day
dusk_color = (255, 102, 102)  # Red-orange for dusk

# Define time ranges for night, dawn, day, and dusk (in hours)
night_time = (0, 6)  # 00:00 - 06:00
dawn_time = (6, 9)   # 06:00 - 08:00
day_time = (9, 17)   # 08:00 - 18:00
dusk_time = (17, 19) # 18:00 - 20:00
night_time2 = (19, 20) # 20:00 - 00:00

def get_local_military_time(lat, lon):
    # Initialize tzwhere
    tz = tzwhere.tzwhere()

    # Get the timezone string for the given coordinates
    timezone_str = tz.tzNameAt(lat, lon)

    if timezone_str is None:
        return "Unable to determine timezone for the given coordinates"

    # Get the timezone object
    tz = timezone(timezone_str)

    # Get current UTC time
    utc_time = datetime.utcnow()

    # Convert UTC time to local time
    local_time = utc_time.replace(tzinfo=timezone('UTC')).astimezone(tz)

    # Format time in military (24-hour) format
    # military_time = local_time.strftime("%H:%M")
    military_time = local_time.hour

    return military_time

# print(get_local_military_time(41.8818, -87.6232))

def lerp_color(color1, color2, t):
    """Linearly interpolate between two colors."""
    return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))

def get_color_for_time(hour):
    """Get the color based on the current hour of the day."""
    if night_time[0] <= hour < night_time[1]:
        # Night to Dawn transition
        t = (hour - night_time[0]) / (night_time[1] - night_time[0])
        return lerp_color(night_color, dawn_color, t)
    elif dawn_time[0] <= hour < dawn_time[1]:
        # Dawn to Day transition
        t = (hour - dawn_time[0]) / (dawn_time[1] - dawn_time[0])
        return lerp_color(dawn_color, day_color, t)
    elif day_time[0] <= hour < day_time[1]:
        # Day color
        return day_color
    elif dusk_time[0] <= hour < dusk_time[1]:
        # Day to Dusk transition
        t = (hour - dusk_time[0]) / (dusk_time[1] - dusk_time[0])
        return lerp_color(day_color, dusk_color, t)
    elif night_time2[0] <= hour < night_time2[1]:
        # Dusk to Night transition
        # print("hit")
        t = (hour - dusk_time[1]) / (night_time2[1] - dusk_time[0])
        return lerp_color(dusk_color, night_color, t)
    else:
        # Night color
        return night_color