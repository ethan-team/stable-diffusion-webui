#!/usr/bin/env bash

# Function to confirm the operation
confirm_operation() {
    echo "update autodl-tmp by rsync data from autodl-fs"
    read -rp "Are you sure you want to proceed? make sure you know what you are doing (y/n): " response
    case "$response" in
        [yY])
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Example usage
if confirm_operation; then
    echo "Operation confirmed. Proceeding..."
    # Perform your desired operation here

    echo "Rsync models from fs to tmp..."
    rsync -av --delete  /root/autodl-fs/sdw/models/ /root/autodl-tmp/models
    echo ""

    echo "Rsync repositories from fs to tmp..."
    rsync -av --delete /root/autodl-fs/sdw/repositories /root/autodl-tmp/repositories
    echo ""

else
    echo "Operation canceled."
fi

