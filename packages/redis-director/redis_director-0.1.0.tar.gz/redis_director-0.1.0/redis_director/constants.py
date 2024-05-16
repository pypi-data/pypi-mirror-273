INCREMENT_LUA_SCRIPT = """
local key = KEYS[1]
local member = ARGV[1]
local increment = tonumber(ARGV[2])
local minimum = tonumber(ARGV[3])

local currentScore = redis.call('zscore', key, member)

if not currentScore then
    currentScore = 0
else
    currentScore = tonumber(currentScore)
end

local newScore = currentScore + increment

if newScore < minimum then
    newScore = minimum
end

redis.call('zadd', key, newScore, member)

return newScore
"""
