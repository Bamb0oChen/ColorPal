using Microsoft.AspNetCore.Mvc;
using AutoMap.Api.Services;
using AutoMap.Api.DTOs;

namespace AutoMap.Api.Controllers;

[ApiController]
[Route("api/[controller]")]
public class MapController : ControllerBase
{
    private readonly IMapService _mapService;
    private readonly ILogger<MapController> _logger;

    public MapController(IMapService mapService, ILogger<MapController> logger)
    {
        _mapService = mapService;
        _logger = logger;
    }

    [HttpPost("recommend")]
    public async Task<ActionResult<RecommendResponseDto>> GetRecommendations(
        [FromBody] RecommendRequestDto request)
    {
        try
        {
            var result = await _mapService.GetRecommendationsAsync(request.Query, request.Location);
            return Ok(result);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "获取推荐失败");
            return StatusCode(500, new { message = "获取推荐失败" });
        }
    }

    [HttpGet("location")]
    public async Task<ActionResult<LocationResponseDto>> GetLocation()
    {
        try
        {
            return Ok(new LocationResponseDto
            {
                Lat = 31.2304,
                Lng = 121.4737,
                Address = "上海市黄浦区"
            });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "获取位置失败");
            return StatusCode(500, new { message = "获取位置失败" });
        }
    }

    [HttpGet("places")]
    public async Task<ActionResult<List<PlaceDto>>> GetPlaces()
    {
        try
        {
            var places = await _mapService.GetPlacesAsync();
            return Ok(places);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "获取地点列表失败");
            return StatusCode(500, new { message = "获取地点列表失败" });
        }
    }
}
