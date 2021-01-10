# Musinsa
Crawling all the best items & insert all the details in MongoDB

1. Crawl best items in 'https://search.musinsa.com/ranking/best'
2. Create dictionary for each information in item
3. Exclude key and value for item that has no certain information
4. Using pymongo, insert dictionary data one by one to avoid BulkWritingError. 
5. Also use function copy() to make different _ObjectId for each item
