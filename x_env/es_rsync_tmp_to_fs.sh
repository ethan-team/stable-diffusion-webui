#!/usr/bin/env bash

# Function to confirm the operation
confirm_operation() {
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

    echo "Rsync models..."
    rsync -av --delete /root/autodl-tmp/models/ /root/autodl-fs/sdw/models
    echo ""

    echo "Rsync repositories..."
    rsync -av --delete /root/autodl-tmp/repositories/ /root/autodl-fs/sdw/repositories
    echo ""

else
    echo "Operation canceled."
fi

gu