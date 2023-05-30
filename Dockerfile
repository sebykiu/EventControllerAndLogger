FROM mcr.microsoft.com/dotnet/runtime:7.0 AS base
WORKDIR /app

FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build
WORKDIR /src
COPY ["EventControllerAndLogger/EventControllerAndLogger.csproj", "EventControllerAndLogger/"]
RUN dotnet restore "EventControllerAndLogger/EventControllerAndLogger.csproj"
COPY . .
WORKDIR "/src/EventControllerAndLogger"
RUN dotnet build "EventControllerAndLogger.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "EventControllerAndLogger.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "EventControllerAndLogger.dll"]
