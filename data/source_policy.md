# Source Policy

## Primary sources used

### Official Stardew Valley website
https://www.stardewvalley.net/

ConcernedApe's official website publishes official announcements and update changelogs.

### Official Stardew Valley Wiki
https://stardewvalleywiki.com/

The Stardew Valley Wiki is hosted and maintained by ConcernedApe and is community-edited. It is the primary detailed reference used for gameplay facts in this corpus.

## Why both sources?
- The official website is authoritative for developer announcements and official update information.
- The official wiki contains detailed gameplay tables and mechanics.

## Wiki reliability note
The wiki's own disclaimer says it is an open community-edited resource and that pages may change. Therefore, a RAG pipeline should preserve:
- source URL
- retrieval date
- game version
- page title

## Licensing note
The wiki states that its content is licensed under CC BY-NC-SA 3.0, subject to the stated exceptions and conditions. See:
https://stardewvalleywiki.com/Stardew_Valley_Wiki:Copyrights

## Recommended RAG metadata
```json
{
  "source": "stardewvalleywiki.com",
  "page": "Crops",
  "version": "1.6.15",
  "category": "crops"
}
```
