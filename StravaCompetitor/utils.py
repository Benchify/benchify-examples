import haversine
import datetime
import json
import os
from typing import Dict, List, Tuple, Optional, Union, Any

def calculate_distance(coords: List[Tuple[float, float]]) -> float:
    """
    Calculate total distance in kilometers given a list of GPS coordinates.
    
    Args:
        coords: List of (latitude, longitude) tuples
        
    Returns:
        Total distance in kilometers
    """
    total_distance = 0.0
    
    for i in range(len(coords) - 1):
        # Calculate distance between consecutive points using haversine formula
        distance = haversine.haversine(coords[i], coords[i+1], unit='km')
        total_distance += distance
        
    return total_distance

def calculate_elevation_gain(elevation_data: List[float]) -> float:
    """
    Calculate total elevation gain in meters from a list of elevation points.
    
    Args:
        elevation_data: List of elevation values in meters
        
    Returns:
        Total elevation gain in meters
    """
    gain = 0.0
    
    for i in range(len(elevation_data) - 1):
        # Only count positive elevation changes
        diff = elevation_data[i+1] - elevation_data[i]
        if diff > 0:
            gain += diff
            
    return gain

def calculate_pace(distance_km: float, duration_seconds: int) -> Tuple[int, int]:
    """
    Calculate pace in minutes per kilometer.
    
    Args:
        distance_km: Distance in kilometers
        duration_seconds: Duration in seconds
        
    Returns:
        Tuple of (minutes, seconds) per kilometer
    """
    if distance_km <= 0:
        return (0, 0)
    
    # Calculate seconds per kilometer
    seconds_per_km = duration_seconds / distance_km
    
    # Convert to minutes and seconds
    minutes = int(seconds_per_km // 60)
    seconds = int(seconds_per_km % 60)
    
    return (minutes, seconds)

def save_activity(user_id: str, activity_data: Dict[str, Any], 
                  base_dir: str = "data/activities") -> str:
    """
    Save activity data to disk and return the activity ID.
    
    Args:
        user_id: Unique identifier for the user
        activity_data: Dictionary containing activity information
        base_dir: Base directory for storing activity data
        
    Returns:
        Activity ID
    """
    # Generate a unique activity ID
    activity_id = f"{user_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Add activity ID and timestamp to the data
    activity_data["id"] = activity_id
    activity_data["timestamp"] = datetime.datetime.now().isoformat()
    
    # Create user directory if it doesn't exist
    user_dir = os.path.join(base_dir, user_id)
    os.makedirs(user_dir, exist_ok=True)
    
    # Save activity data as JSON
    file_path = os.path.join(user_dir, f"{activity_id}.json")
    with open(file_path, "w") as f:
        json.dump(activity_data, f, indent=2)
    
    return activity_id

def get_user_activities(user_id: str, limit: Optional[int] = None,
                        activity_type: Optional[str] = None,
                        base_dir: str = "data/activities") -> List[Dict[str, Any]]:
    """
    Retrieve a user's activities with optional filtering.
    
    Args:
        user_id: Unique identifier for the user
        limit: Maximum number of activities to return (newest first)
        activity_type: Filter by activity type (e.g., "run", "ride", "swim")
        base_dir: Base directory for storing activity data
        
    Returns:
        List of activity data dictionaries
    """
    user_dir = os.path.join(base_dir, user_id)
    
    # Return empty list if user directory doesn't exist
    if not os.path.exists(user_dir):
        return []
    
    activities = []
    
    # Get all JSON files in the user directory
    for filename in os.listdir(user_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(user_dir, filename)
            with open(file_path, "r") as f:
                activity = json.load(f)
                
                # Apply activity type filter if provided
                if activity_type is None or activity.get("type") == activity_type:
                    activities.append(activity)
    
    # Sort activities by timestamp (newest first)
    activities.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    
    # Apply limit if provided
    if limit is not None and limit > 0:
        activities = activities[:limit]
    
    return activities

def calculate_statistics(activities: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate summary statistics for a list of activities.
    
    Args:
        activities: List of activity dictionaries
        
    Returns:
        Dictionary with summary statistics
    """
    if not activities:
        return {
            "total_activities": 0,
            "total_distance": 0,
            "total_elevation_gain": 0,
            "total_duration": 0,
            "activity_types": {}
        }
    
    stats = {
        "total_activities": len(activities),
        "total_distance": 0,
        "total_elevation_gain": 0,
        "total_duration": 0,
        "activity_types": {}
    }
    
    for activity in activities:
        # Accumulate totals
        stats["total_distance"] += activity.get("distance", 0)
        stats["total_elevation_gain"] += activity.get("elevation_gain", 0)
        stats["total_duration"] += activity.get("duration", 0)
        
        # Count by activity type
        activity_type = activity.get("type", "unknown")
        if activity_type in stats["activity_types"]:
            stats["activity_types"][activity_type] += 1
        else:
            stats["activity_types"][activity_type] = 1
    
    return stats