# Drone-Vertical-Wind-Profiling

## ⚠️ THIS PROJECT IS IN PROGRESS. ⚠️

Log data has all been collected, random forest model running at reasonable accuracy (barring extreme gusts and turbulence, which can be accounted for by normalizing for training data's average 10m turbulence and collecting data in more extreme weather).

A project to reverse-engineer consumer drone telemetry (DJI Fly Mavic Mini) to create "Vertical Wind Profiles" based on different low-level altitudes (regression). Additionally, testing out whether the pitch/roll data from the drone's gyroscope (in addition to wind data from OpenWeatherMap) can accurately predict what altitude the drone is hovering at (classification).
