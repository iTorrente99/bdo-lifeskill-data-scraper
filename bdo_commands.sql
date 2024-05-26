--SELECT * FROM adventurer_data WHERE guild IN ('Clarity', 'Life') ORDER BY cooking_total_level DESC;

SELECT 
    guild,
    ROUND(AVG(gathering_total_level), 2) AS avg_gathering_level,
    ROUND(AVG(fishing_total_level), 2) AS avg_fishing_level,
    ROUND(AVG(hunting_total_level), 2) AS avg_hunting_level,
    ROUND(AVG(cooking_total_level), 2) AS avg_cooking_level,
    ROUND(AVG(alchemy_total_level), 2) AS avg_alchemy_level,
    ROUND(AVG(processing_total_level), 2) AS avg_processing_level,
    ROUND(AVG(training_total_level), 2) AS avg_training_level,
    ROUND(AVG(trading_total_level), 2) AS avg_trading_level,
    ROUND(AVG(farming_total_level), 2) AS avg_farming_level,
    ROUND(AVG(sailing_total_level), 2) AS avg_sailing_level,
    ROUND(AVG(barter_total_level), 2) AS avg_barter_level
FROM adventurer_data
GROUP BY guild;


