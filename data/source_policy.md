# Source Policy

## Primary sources used

### Official Stardew Valley website

https://www.stardewvalley.net/

ConcernedApe's official Stardew Valley website is the primary source for:

- Official announcements
- Game updates
- Patch notes
- Official changelogs
- Developer information

When official information is available, it should be preferred over secondary sources.

### Official Stardew Valley Wiki

https://stardewvalleywiki.com/

The Stardew Valley Wiki is hosted by ConcernedApe and maintained by Stardew Valley community contributors. It provides detailed gameplay information and is the primary reference for:

- Crops
- Fish
- Villagers
- Gifts
- Buildings
- Animals
- Items
- Locations
- Festivals
- Game mechanics
- Quests
- Skills
- Bundles
- Other gameplay data

The wiki is community-edited, so individual pages may change and should be treated as a detailed secondary reference rather than a developer-authored source. :contentReference[oaicite:0]{index=0}

## Why both sources?

Both sources are used because they serve different purposes:

- The official website provides authoritative developer announcements and update information.
- The official wiki provides detailed gameplay tables, mechanics, item data, and other structured information that is not practical to maintain on the official website.

For exact gameplay facts, the wiki should normally be used when detailed information is required.

For official announcements, patch notes, and developer statements, the official website takes priority.

## Wiki reliability note

The Stardew Valley Wiki is an open community-edited resource. Its disclaimer states that information may be modified by community members and that the content has not necessarily been reviewed by the game's developer. :contentReference[oaicite:1]{index=1}

Therefore, the RAG pipeline should preserve:

- Source URL
- Page title
- Retrieval date
- Game version
- Category
- Source type

Recommended metadata:

```json
{
  "source": "stardewvalleywiki.com",
  "page": "Crops",
  "version": "1.6.15",
  "category": "crops",
  "retrieved_at": "YYYY-MM-DD"
}
```
