---
layout: post
title: "Delete liked tweets"
date: 2016-07-03 18:00:00
comments: false
lang: english
---

# requirement

- twitter 5.16.0 (ruby gem)
- ruby 2.3.0

# code

```rb
# -*- coding: utf-8 -*-
require 'twitter'


consumer_key = 'hogehoge'
consumer_secret = 'hogehoge'
access_token = 'hoeghoge-hogehoge'
access_token_secret = 'hogehoge'

client = Twitter::REST::Client.new do |config|
  config.consumer_key = consumer_key
  config.consumer_secret = consumer_secret
  config.access_token = access_token
  config.access_token_secret = access_token_secret
end

# delete my liked tweets
while true
  client.favorites(:count => 200).each do |elem|
    client.unfavorite(elem.id)
  end
end

# options
# delete my tweets
while true
  client.user_timeline(:count => 200).each do |elem|
    client.destroy_status(elem.id)
  end
end
```
