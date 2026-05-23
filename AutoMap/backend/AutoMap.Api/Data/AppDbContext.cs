using Microsoft.EntityFrameworkCore;
using AutoMap.Api.Models;

namespace AutoMap.Api.Data;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {
    }

    public DbSet<Place> Places { get; set; } = null!;
    public DbSet<UserFavorite> UserFavorites { get; set; } = null!;

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);

        modelBuilder.Entity<Place>().HasData(
            new Place
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
                CreatedAt = DateTime.UtcNow
            },
            new Place
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
                CreatedAt = DateTime.UtcNow
            }
        );
    }
}
