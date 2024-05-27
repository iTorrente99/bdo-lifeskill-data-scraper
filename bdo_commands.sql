SELECT
    guild,
    ROUND(AVG(gathering_total_level), 2) AS avg_gathering,
    ROUND(AVG(fishing_total_level), 2) AS avg_fishing,
    ROUND(AVG(hunting_total_level), 2) AS avg_hunting,
    ROUND(AVG(cooking_total_level), 2) AS avg_cooking,
    ROUND(AVG(alchemy_total_level), 2) AS avg_alchemy,
    ROUND(AVG(processing_total_level), 2) AS avg_processing,
    ROUND(AVG(training_total_level), 2) AS avg_training,
    ROUND(AVG(trading_total_level), 2) AS avg_trading,
    ROUND(AVG(farming_total_level), 2) AS avg_farming,
    ROUND(AVG(sailing_total_level), 2) AS avg_sailing,
    ROUND(AVG(barter_total_level), 2) AS avg_barter,
    ROUND(AVG(total_level), 2) AS avg_total_level,
    ROUND(AVG(life_fame), 2) AS avg_life_fame
FROM adventurer_data
WHERE date = '2024-05-26' AND total_level IS NOT NULL
GROUP BY guild
ORDER BY avg_total_level DESC;

SELECT
    date,
    ROUND(AVG(gathering_total_level), 2) AS avg_gathering,
    ROUND(AVG(fishing_total_level), 2) AS avg_fishing,
    ROUND(AVG(hunting_total_level), 2) AS avg_hunting,
    ROUND(AVG(cooking_total_level), 2) AS avg_cooking,
    ROUND(AVG(alchemy_total_level), 2) AS avg_alchemy,
    ROUND(AVG(processing_total_level), 2) AS avg_processing,
    ROUND(AVG(training_total_level), 2) AS avg_training,
    ROUND(AVG(trading_total_level), 2) AS avg_trading,
    ROUND(AVG(farming_total_level), 2) AS avg_farming,
    ROUND(AVG(sailing_total_level), 2) AS avg_sailing,
    ROUND(AVG(barter_total_level), 2) AS avg_barter,
    ROUND(AVG(total_level), 2) AS avg_total_level,
    ROUND(AVG(life_fame), 2) AS avg_life_fame
FROM adventurer_data
WHERE guild = 'Clarity' AND total_level IS NOT NULL
GROUP BY date
ORDER BY date DESC;





-- UPDATE adventurer_data
-- SET
--     total_level = CASE WHEN total_level = 0 THEN NULL ELSE total_level END,
--     life_fame = CASE WHEN life_fame = 0 THEN NULL ELSE life_fame END;

-- UPDATE adventurer_data
-- SET life_fame = life_fame + 1
-- WHERE date = '2024-05-26';



SELECT 
	ad1.date as start_d,
	ad2.date as end_d,
    ad1.family_name,
    ad1.guild,
    ad2.total_level,
    (ad2.gathering_total_level - ad1.gathering_total_level) AS gathering_diff,
    (ad2.fishing_total_level - ad1.fishing_total_level) AS fishing_diff,
    (ad2.hunting_total_level - ad1.hunting_total_level) AS hunting_diff,
    (ad2.cooking_total_level - ad1.cooking_total_level) AS cooking_diff,
    (ad2.alchemy_total_level - ad1.alchemy_total_level) AS alchemy_diff,
    (ad2.processing_total_level - ad1.processing_total_level) AS processing_diff,
    (ad2.training_total_level - ad1.training_total_level) AS training_diff,
    (ad2.trading_total_level - ad1.trading_total_level) AS trading_diff,
    (ad2.farming_total_level - ad1.farming_total_level) AS farming_diff,
    (ad2.sailing_total_level - ad1.sailing_total_level) AS sailing_diff,
    (ad2.barter_total_level - ad1.barter_total_level) AS barter_diff,
    (ad2.total_level - ad1.total_level) AS total_level_diff,
    (ad2.life_fame - ad1.life_fame) AS life_fame_diff
FROM 
    adventurer_data ad1
JOIN 
    adventurer_data ad2 ON ad1.family_name = ad2.family_name AND ad1.guild = ad2.guild
WHERE 
    ad1.date = '2024-05-25' AND ad2.date = '2024-05-26'
    AND (ad2.guild = 'Clarity' OR ad2.guild = 'Life')
    AND (ad2.total_level - ad1.total_level) > 0
ORDER BY 
    total_level_diff DESC;
	
	
SELECT 
	ad1.date as start_d,
	ad2.date as end_d,
    ad1.guild,
    ROUND(AVG(ad2.gathering_total_level - ad1.gathering_total_level), 2) AS gathering_diff,
    ROUND(AVG(ad2.fishing_total_level - ad1.fishing_total_level), 2) AS fishing_diff,
    ROUND(AVG(ad2.hunting_total_level - ad1.hunting_total_level), 2) AS hunting_diff,
    ROUND(AVG(ad2.cooking_total_level - ad1.cooking_total_level), 2) AS cooking_diff,
    ROUND(AVG(ad2.alchemy_total_level - ad1.alchemy_total_level), 2) AS alchemy_diff,
    ROUND(AVG(ad2.processing_total_level - ad1.processing_total_level), 2) AS processing_diff,
    ROUND(AVG(ad2.training_total_level - ad1.training_total_level), 2) AS training_diff,
    ROUND(AVG(ad2.trading_total_level - ad1.trading_total_level), 2) AS trading_diff,
    ROUND(AVG(ad2.farming_total_level - ad1.farming_total_level), 2) AS farming_diff,
    ROUND(AVG(ad2.sailing_total_level - ad1.sailing_total_level), 2) AS sailing_diff,
    ROUND(AVG(ad2.barter_total_level - ad1.barter_total_level), 2) AS barter_diff,
    ROUND(AVG(ad2.total_level - ad1.total_level), 2) AS total_level_diff,
    ROUND(AVG(ad2.life_fame - ad1.life_fame), 2) AS life_fame_diff,
    ROUND(AVG(ad2.total_level), 2) AS avg_total_level,
    ROUND(AVG(ad2.life_fame), 2) AS avg_life_fame
FROM 
    adventurer_data ad1
JOIN 
    adventurer_data ad2 ON ad1.family_name = ad2.family_name AND ad1.guild = ad2.guild
WHERE 
    ad1.date = '2024-05-25' AND ad2.date = '2024-05-26'
GROUP BY 
    ad1.guild
ORDER BY 
    avg_total_level DESC;





