#!/bin/bash

echo "Starting powermetrics..."

LIGHT_CLASS="programsWillem.Fibonacci"
HEAVY_CLASS="programsWillem.HeavyFibonacci"

if [ "$1" == "light" ]; then
    JAVA_CLASS=$LIGHT_CLASS
    POWER_FILE="power_light.txt"
elif [ "$1" == "heavy" ]; then
    JAVA_CLASS=$HEAVY_CLASS
    POWER_FILE="power_heavy.txt"
else
    echo "Usage: $0 [light|heavy]"
    exit 1
fi

# Start powermetrics
sudo powermetrics --samplers cpu_power,gpu_power --show-process-energy -i 1000 -n 30 > "$POWER_FILE" &
PM_PID=$!

sleep 2

echo "$(date '+%Y-%m-%d %H:%M:%S') - Starting Java program: $JAVA_CLASS"
START_TIME=$(date +%s)

java -cp out "$JAVA_CLASS"
JAVA_EXIT_CODE=$?

END_TIME=$(date +%s)
echo "$(date '+%Y-%m-%d %H:%M:%S') - Java program finished with exit code $JAVA_EXIT_CODE"

wait $PM_PID

echo "Powermetrics finished. Power data saved to $POWER_FILE"
echo "Java ran for $((END_TIME - START_TIME)) seconds."
