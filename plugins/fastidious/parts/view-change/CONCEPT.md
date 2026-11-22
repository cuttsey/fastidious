# view-change (concept)

**Shared job.** Turns a change of view (a chapter, a page, a detail) into a moment, and hides the swap completely while it happens.

Both variants have the same API, so a build can switch between them in one line:

```js
await part.play(() => { /* swap the view underneath; may be async */ });
```

| Variant | Use it when | Do not use it when | Register | Rung | Cost band |
|---|---|---|---|---|---|
| [`type-curtain`](type-curtain/PART.md) | The brand is type-led and has its own vocabulary worth showing at full size. | The words would be filler, or the change happens often. | Expressive, loud | 2 | Low |
| [`pixel-cover`](pixel-cover/PART.md) | The brand is graphic, digital or playful, and the change should feel quick and mechanical. | The brand is quiet and material (use a fade, or `index-to-detail/flip` for items). | Graphic, brisk | 2 | Low |

Use at most one view-change part per site, and only for a few big moments.
