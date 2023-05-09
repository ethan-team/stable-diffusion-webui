#!/usr/bin/env bash

rsync -av --delete /root/autodl-tmp/models/ /root/autodl-fs/sdw

rsync -av --delete /root/autodl-tmp/repositories/ /root/autodl-fs/sdw