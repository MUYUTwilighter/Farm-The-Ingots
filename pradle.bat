@echo off

if "%1" == "buildClient" (
    python pradle/build_client.py
) else if "%1" == "runServer" (
    python pradle/run_server.py
)