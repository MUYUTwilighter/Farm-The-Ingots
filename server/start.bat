@echo off

set installer="fabric-server-mc.${minecraft_version}-loader.${loader_version}-launcher.${launcher_version}.jar"
set java_path=java

:: if not exist, download fabric installer

if not exist %installer% (
    curl -o %installer% "https://meta.fabricmc.net/v2/versions/loader/${minecraft_version}/${loader_version}/${launcher_version}/server/jar"
)

:: run fabric installer

%java_path% -jar %installer% -nogui