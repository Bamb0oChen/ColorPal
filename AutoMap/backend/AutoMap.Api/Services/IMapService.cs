using AutoMap.Api.DTOs;

namespace AutoMap.Api.Services;

public interface IMapService
{
    Task<RecommendResponseDto> GetRecommendationsAsync(string query, LocationDto? location);
    Task<List<PlaceDto>> GetPlacesAsync();
}
