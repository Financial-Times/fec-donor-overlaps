# WinRed data

The files we're keeping in here are too large to push to remote. We can eventually use GitHub's large file storage, or figure something else out, but for the time-being, all of the files that we're looking at can be found in the WinRed filings for the 2020 and 2022 cycles on ProPublica's FEC Itemizer, in the "Receipts" (Schedule A) column:

- [WinRed's 2020 Filings](https://projects.propublica.org/itemizer/committee/C00694323/2020)
- [WinRed's 2022 Filings](https://projects.propublica.org/itemizer/committee/C00694323/2022)

Here are links to a couple of example files that are included in this set, to confirm you're finding matching files:

- [WinRed's 2020 October Quarterly Receipts](https://pp-projects-static.s3.amazonaws.com/itemizer/sa1490496.csv.zip?_ga=2.60827049.402447242.1643133319-578717599.1642611375) (`sa_winred_oct_2020_quarterly.csv`)
- [WinRed's 2021 Mid-Year filing](https://pp-projects-static.s3.amazonaws.com/itemizer/sa1532732.csv.zip?_ga=2.101090436.402447242.1643133319-578717599.1642611375) (`sa_winred_july_2021_midyear.csv`)

For looking at Trump overlap, we're including all WinRed filings from 2020 and 2022, which will crucially include the year-end filing for 2021, once it is available next week.

I've added a sample data with 2000 rows from the mid-year filing that we can work with to sort out campaign-committee mappings and other processing without wrangling multiple GBs of data.
