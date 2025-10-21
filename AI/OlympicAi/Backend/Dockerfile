FROM mcr.microsoft.com/dotnet/aspnet:9.0 AS base
WORKDIR /app
EXPOSE 5246

FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /src
COPY ["AI-spotter.csproj", "./"]

RUN dotnet restore "AI-spotter.csproj"
COPY . .

# Redundant for publish
RUN dotnet build "AI-spotter.csproj" -c Release -o /app/build 

FROM build AS publish
RUN dotnet publish "AI-spotter.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app

RUN mkdir -p /app/Videos
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "AI-spotter.dll"]

