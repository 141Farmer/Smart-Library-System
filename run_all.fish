#!/usr/bin/fish

function run_service
    set service $argv[1]
    set cmd $argv[2]

    switch (uname)
        case Linux
            if command -v konsole >/dev/null
                # KDE Plasma (konsole)
                konsole --new-tab --workdir "./$service" -e fish -c "$cmd; exec fish" &
            else if command -v gnome-terminal >/dev/null
                # GNOME Terminal
                gnome-terminal --tab --title="$service" --working-directory="./$service" -- bash -c "$cmd; exec fish" &
            else if command -v xterm >/dev/null
                # Fallback: xterm
                xterm -title "$service" -e "cd ./$service && $cmd" &
            end
        case Darwin
            # macOS Terminal
            osascript -e "tell application \"Terminal\" to do script \"cd ./$service && $cmd\"" &
        case '*'
            echo "Unsupported OS: "(uname)
            exit 1
    end
end

# Run all services
run_service "user-service" "fish run.fish"
run_service "book-service" "fish run.fish"
run_service "loan-service" "fish run.fish"

echo "All services started in separate terminals/windows!"