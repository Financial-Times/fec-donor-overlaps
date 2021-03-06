# FEC Donor Overlaps

Scripts for processing raw FEC data (particularly ActBlue/WinRed filings) or itemized filings from ProPublica, aggregating them, and producing donor overlap figures. Used for the charts/data in [this story](https://www.ft.com/content/27cf21ac-dabc-45a5-813f-0223572b908f).

For now, we're going to work mainly with already-processed filings from [ActBlue](https://projects.propublica.org/itemizer/committee/C00401224/2022)/[WinRed](https://projects.propublica.org/itemizer/committee/C00694323/2022) in CSV format, from ProPublica's [FEC Itemizer](https://projects.propublica.org/itemizer). We can work with raw `.fec` files directly from the FEC site, as well, but need to process them with a tool like [FastFEC](https://github.com/washingtonpost/FastFEC) first.

The narrow goal right now is to look at overlap between Trump 2020/Biden 2020 donors and 2022 congressional candidates, but I've written these in a way that's general-purpose/applicable for future uses.

The bash script in [`scripts/process_data.sh`](https://github.com/Financial-Times/fec-donor-overlaps/blob/main/scripts/process_data.sh) can be used as a guide for what each script does and when to execute it. More or less, we're aggregating then processing several data files with committee, campaign, and contribution data to work towards a file with donor count totals/overlaps between each registered candidate present in WinRed/ActBlue filings (virtually all federal candidates).

## Licence
This software is published by the Financial Times under the MIT licence.

Please note the MIT licence only covers the software, and does not cover any FT content or branding incorporated into the software or made available using the software. FT content is copyright © The Financial Times Limited, and FT and ‘Financial Times’ are trademarks of The Financial Times Limited, all rights reserved. For more information about republishing FT content, please contact our republishing department.
