# FEC Aggregation

Scripts for processing raw FEC data (particularly ActBlue/WinRed filings) and aggregating it based on some points of interest. Initially working on donor overlaps.

For now, we're just going to work with already-processed filings from [ActBlue](https://projects.propublica.org/itemizer/committee/C00401224/2022)/[WinRed](https://projects.propublica.org/itemizer/committee/C00694323/2022) in CSV format, from ProPublica's [FEC Itemizer](https://projects.propublica.org/itemizer). In the future, depending on needs around completeness or expediency, or what we're looking at, we can look at processing raw `.fec` files.

The narrow goal right now is to look at overlap between Trump 2020 donors and 2022 congressional candidates, but I've tried to write these in a way that's somewhat general-purpose/applicable for future uses.

The bash script in `scripts/process_data.sh` can be used as a guide for what each script does and when to execute it. More or less, we're aggregating then processing several data files with committee, campaign, and contribution data to work towards a file with donor count totals/overlaps between each registered candidate present in WinRed filings (virtually all federal, GOP candidates).
