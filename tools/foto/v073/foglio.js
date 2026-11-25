// Foglio di controllo delle candidate: window.FOGLIO(from, to) mostra le voci in quell'intervallo
window.FOGLIO = (from, to) => {
  const ids = Object.keys(FOTO.cand);
  const th = u => u.replace('/commons/', '/commons/thumb/') + '/120px-' + u.split('/').pop() + (/\.png$/i.test(u) ? '' : '');
  let h = '<style>body{margin:0;background:#fff;font:11px system-ui}.r{display:flex;gap:4px;padding:3px 6px;border-bottom:1px solid #ccc;align-items:flex-start}.l{width:150px;flex:none;font-weight:600}.c{width:118px;flex:none}.c img{width:118px;height:84px;object-fit:cover;display:block;background:#eee}.c span{display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;color:#333}.c.r0 span{color:#b00}</style>';
  ids.slice(from, to).forEach((id, k) => {
    const c = FOTO.cand[id];
    h += `<div class="r"><div class="l">${from + k}. ${id.replace(/^(event|site|culture|state|invention|tradition|movement|religion|empire)-/, '')}</div>` +
      c.map((x, i) => `<div class="c r${x.rel}"><img src="${th(x.url)}"><span>${i} · ${x.v >= 1000 ? Math.round(x.v / 1000) + 'k' : x.v}</span><span>${x.f.slice(0, 26)}</span></div>`).join('') + '</div>';
  });
  document.body.innerHTML = h; window.scrollTo(0, 0);
  return ids.length;
};
