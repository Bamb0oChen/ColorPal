namespace AutoMap.Api.DTOs;

public class LocationDto
{
    public double Lat { get; set; }
    public double Lng { get; set; }
}

public class PlaceDto
{
    public string Id { get; set; } = string.Empty;
    public string Name { get; set; } = string.Empty;
    public string Address { get; set; } = string.Empty;
    public LocationDto Location { get; set; } = null!;
    public string Category { get; set; } = string.Empty;
    public double Rating { get; set; }
    public string Description { get; set; } = string.Empty;
    public string Image { get; set; } = string.Empty;
    public double Distance { get; set; }
    public string? Duration { get; set; }
}

public class RecommendRequestDto
{
    public string Query { get; set; } = string.Empty;
    public LocationDto? Location { get; set; }
}

public class RecommendResponseDto
{
    public List<PlaceDto> Places { get; set; } = new();
    public LocationDto CenterLocation { get; set; } = null!;
}

public class LocationResponseDto
{
    public double Lat { get; set; }
    public double Lng { get; set; }
    public string Address { get; set; } = string.Empty;
}
