# ActBlue data

The files we're keeping in here are too large to push to remote. We can eventually use GitHub's large file storage, or figure something else out, but for the time-being, all of the files that we're looking at can be found in the ActBlue filings for the 2020 and 2022 cycles on ProPublica's FEC Itemizer, in the "Receipts" (Schedule A) column (or directly from the committee's page on the FEC site if we don't want to wait for the itemizer to run and then processed with the FastFEC tool):

- [ActBlue's 2020 Filings](https://projects.propublica.org/itemizer/committee/C00401224/2020)
- [ActBlue's 2022 Filings](https://projects.propublica.org/itemizer/committee/C00401224/2022)

Here are links to a couple of example files that are included in this set, to confirm you're finding matching files:

- [ActBlue's 2020 July Monthly Receipts](https://pp-projects-static.s3.amazonaws.com/itemizer/sa1427110.csv.zip?_ga=2.215416215.1874942751.1644604537-578717599.1642611375) (`sa_actblue_july_2020_monthly.csv`)
- [ActBlue's 2021 Year-End filing](https://pp-projects-static.s3.amazonaws.com/itemizer/sa1566626.csv.zip?_ga=2.210744597.1874942751.1644604537-578717599.1642611375) (`sa_actblue_jan_2022_yearend.csv`)

For looking at Biden overlap, we're including all ActBlue filings from 2020 and 2022, which will crucially include the year-end filing for 2021, once it is available.

I've added a sample data with 2000 rows from the mid-year filing that we can work with to sort out campaign-committee mappings and other processing without wrangling multiple GBs of data.
