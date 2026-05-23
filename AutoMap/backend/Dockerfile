FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY ["AutoMap.Api/AutoMap.Api.csproj", "AutoMap.Api/"]
RUN dotnet restore "AutoMap.Api/AutoMap.Api.csproj"

COPY . .
WORKDIR "/src/AutoMap.Api"
RUN dotnet build "AutoMap.Api.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "AutoMap.Api.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=publish /app/publish .
EXPOSE 5000
ENTRYPOINT ["dotnet", "AutoMap.Api.dll"]
