using AutoMap.Api.Data;
using AutoMap.Api.DTOs;
using Microsoft.EntityFrameworkCore;

namespace AutoMap.Api.Services;

public class MapService : IMapService
{
    private readonly AppDbContext _dbContext;
    private readonly ILogger<MapService> _logger;

    private static readonly List<object> SamplePlaces = new()
    {
        new
        {
            Id = "1",
            Name = "外滩",
            Address = "上海市黄浦区中山东一路",
            Latitude = 31.2397,
            Longitude = 121.4998,
            Category = "scenic",
            Rating = 4.8,
            Description = "百年历史万国建筑博览群，夜景超美，魔都地标必打卡",
            Image = "https://images.unsplash.com/photo-1474181487882-5abf3f0ba6a2?w=400",
        },
        new
        {
            Id = "2",
            Name = "南京路步行街",
            Address = "上海市黄浦区南京东路",
            Latitude = 31.2354,
            Longitude = 121.4739,
            Category = "shopping",
            Rating = 4.5,
            Description = "中华商业第一街，老式铛铛车穿梭，购物美食一站式",
            Image = "https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400",
        },
        new
        {
            Id = "3",
            Name = "豫园",
            Address = "上海市黄浦区福佑路168号",
            Latitude = 31.2220,
            Longitude = 121.4880,
            Category = "scenic",
            Rating = 4.6,
            Description = "明代古典园林，九曲桥、小笼包，老上海味道",
            Image = "https://images.unsplash.com/photo-1537531383496-f4749b8032cf?w=400",
        },
        new
        {
            Id = "4",
            Name = "东方明珠",
            Address = "上海市浦东新区世纪大道1号",
            Latitude = 31.2397,
            Longitude = 121.4998,
            Category = "scenic",
            Rating = 4.7,
            Description = "上海地标塔，360度俯瞰浦江两岸，悬空走廊超刺激",
            Image = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=400",
        },
        new
        {
            Id = "5",
            Name = "老城隍庙小吃广场",
            Address = "上海市黄浦区旧校场路99号",
            Latitude = 31.2240,
            Longitude = 121.4860,
            Category = "food",
            Rating = 4.4,
            Description = "南翔小笼、生煎包、蟹粉豆腐，上海小吃一网打尽",
            Image = "https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?w=400",
        },
    };

    public MapService(AppDbContext dbContext, ILogger<MapService> logger)
    {
        _dbContext = dbContext;
        _logger = logger;
    }

    public async Task<RecommendResponseDto> GetRecommendationsAsync(string query, LocationDto? location)
    {
        var center = location ?? new LocationDto { Lat = 31.2304, Lng = 121.4737 };
        var random = new Random();

        var places = SamplePlaces.Select((p, i) =>
        {
            dynamic place = p;
            var variation = (random.NextDouble() - 0.5) * 0.02;
            return new PlaceDto
            {
                Id = place.Id,
                Name = place.Name,
                Address = place.Address,
                Location = new LocationDto
                {
                    Lat = center.Lat + variation * (i + 1),
                    Lng = center.Lng + variation * (i + 1)
                },
                Category = place.Category,
                Rating = place.Rating,
                Description = place.Description,
                Image = place.Image,
                Distance = random.Next(500, 3000),
                Duration = $"{random.Next(10, 40)}分钟"
            };
        }).ToList();

        return await Task.FromResult(new RecommendResponseDto
        {
            Places = places,
            CenterLocation = center
        });
    }

    public async Task<List<PlaceDto>> GetPlacesAsync()
    {
        var places = await _dbContext.Places.ToListAsync();
        return places.Select(p => new PlaceDto
        {
            Id = p.Id,
            Name = p.Name,
            Address = p.Address,
            Location = new LocationDto { Lat = p.Latitude, Lng = p.Longitude },
            Category = p.Category,
            Rating = p.Rating,
            Description = p.Description,
            Image = p.Image,
            Distance = 0
        }).ToList();
    }
}
