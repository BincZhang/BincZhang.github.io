(() => {
  const search = document.querySelector('#search');
  if (!search) return;
  const rows = [...document.querySelectorAll('[data-search]')];
  const count = document.querySelector('#result-count');
  const empty = document.querySelector('#empty');
  const filter = () => {
    const q = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    rows.forEach(row => {
      row.hidden = !row.dataset.search.toLocaleLowerCase().includes(q);
      if (!row.hidden) visible++;
    });
    count.textContent = `${visible} 篇文章`;
    empty.hidden = visible !== 0;
  };
  search.addEventListener('input', filter);
  filter();
})();
