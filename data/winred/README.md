The files we're keeping in here are too large to push to remote. We can eventually use GitHub's large file storage, or figure something else out, but for the time-being, the two files we're looking at are:

- [WinRed's 2020 October Quarterly Receipts](https://pp-projects-static.s3.amazonaws.com/itemizer/sa1490496.csv.zip?_ga=2.60827049.402447242.1643133319-578717599.1642611375) (sa_winred_oct_2020_quarterly.csv)
- [WinRed's 2021 Mid-Year filing](https://pp-projects-static.s3.amazonaws.com/itemizer/sa1532732.csv.zip?_ga=2.101090436.402447242.1643133319-578717599.1642611375) (sa_winred_july_2021_midyear.csv)

Even just for this initial stage looking at Trump overlap, we're eventually going to need to include all WinRed filings from 2020 and 2022, but keeping it simple for now with some test data.

I've added a sample data with 2000 rows from the mid-year filing that we can work with to sort out campaign-committee mappings and other processing without wrangling multiple GBs of data.
