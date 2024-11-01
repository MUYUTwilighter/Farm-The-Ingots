@echo off

set installer="fabric-server-mc.1.20.1-loader.0.16.7-launcher.1.0.1.jar"
set java_path=java

:: if not exist, download fabric installer

if not exist %installer% (
    curl -o %installer% "https://meta.fabricmc.net/v2/versions/loader/1.20.1/0.16.7/1.0.1/server/jar"
)

:: run fabric installer

%java_path% -jar %installer% -nogui