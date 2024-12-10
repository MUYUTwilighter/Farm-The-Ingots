@echo off

if "%1" == "build" (
    if "%2" == "client" (
        python ./pradle/build_client.py
    ) else if "%2" == "server" (
        python ./pradle/build_server.py
    ) else (
        python ./pradle/build_client.py
        python ./pradle/build_server.py
    )
) else if "%1" == "runServer" (
    python ./pradle/run_server.py
) else if "%1" == "init" (
    shift
    python ./pradle/init.py %*
) else if not "%1" == "" (
    echo Unknown command "%1"
) else (
    echo Pradle 0.0.1 Alpha
    echo Author: MUYU_Twilighter
)