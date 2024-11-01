@echo off

if "%1" == "build" (
    if "%2" == "client" (
        python pradle/build_client.py
    ) else if "%2" == "server" (
        echo build server not available
    ) else (
        python pradle/build_client.py
    )
) else if "%1" == "runServer" (
    python pradle/run_server.py
)