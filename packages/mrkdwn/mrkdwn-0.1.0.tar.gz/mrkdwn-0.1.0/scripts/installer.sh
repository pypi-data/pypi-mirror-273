#!/bin/bash

ALIAS="alias markdown='python -m markdown_tool.main'"
BASHRC="$HOME/.bashrc"
ZSHRC="$HOME/.zshrc"

# Determine the shell config file
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$ZSHRC"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$BASHRC"
else
    echo "Unsupported shell. Please add the alias manually."
    exit 1
fi

# Add the alias if it doesn't exist
if ! grep -q "$ALIAS" "$SHELL_CONFIG"; then
    echo "$ALIAS" >> "$SHELL_CONFIG"
    echo "Alias added to $SHELL_CONFIG. Please restart your terminal or source the file."
else
    echo "Alias already exists in $SHELL_CONFIG."
fi
