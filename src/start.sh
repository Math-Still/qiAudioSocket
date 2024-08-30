#!/bin/bash

if [ "$#" -ne 4 ]; then
    echo "用法: $0 <服务器IP> <用户名> <远程路径> <本地文件名>"
    exit 1
fi

SERVER_IP="$1"
USERNAME="$2"
REMOTE_PATH="$3"
FILE="$4"

scp "$FILE" "$USERNAME@$SERVER_IP:$REMOTE_PATH"

ssh "$USERNAME@$SERVER_IP" "python $REMOTE_PATH/$(basename "$FILE")"