# index-to-detail (concept)

**Shared job.** Takes the visitor from an index (a grid, a range, a list of work) into one item's detail without losing their place, and back again to exactly where they were.

| Variant | Use it when | Do not use it when | Register | Rung | Cost band | Status |
|---|---|---|---|---|---|---|
| [`echo-trail`](echo-trail/PART.md) | The item itself is the hero: a product, a piece of work, a photograph. The echoes make the journey visible and a little theatrical. | The index is text-only, or opening detail is routine and frequent (a long list people scan quickly). | Expressive | 2 | Low | Admitted |
| [`push`](push/PART.md) | Choosing one thing out of many is the moment: the rest of the index is shoved off screen to make room. | The index is long and scrolled, or the visitor opens items repeatedly in quick succession. | Bold | 2 | Low | Admitted (run 006) |
| [`flip`](flip/PART.md) | The same job in a calm register: the picture glides into place and home again, no echoes. Use when opening detail is frequent or the brand is restrained. | The item is the hero and the journey should be felt. | Restrained | 2 | Low | Admitted (original) |

All variants must keep focus management: focus moves into the detail on open and back to the item on close, and Escape closes.

All variants share one markup contract and option set, so a build can switch between them with one line.
