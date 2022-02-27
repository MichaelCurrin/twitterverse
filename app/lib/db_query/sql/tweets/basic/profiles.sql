/*
 Select all values in Profile table.
 */
SELECT
  guid,
  '@' || screen_name AS screen_name,
  name,
  followers_count,
  location,
  image_url
FROM
  Profile;
