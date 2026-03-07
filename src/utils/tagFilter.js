// src/utils/tagFilter.js
// Used on blog and portfolio pages for client-side filtering
export function filterByTag(items, selectedTag) {
  if (!selectedTag || selectedTag === 'all') return items;
  return items.filter(item => item.tags.includes(selectedTag));
}
