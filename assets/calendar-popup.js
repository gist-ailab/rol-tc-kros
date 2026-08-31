/* 일시 칩의 "일정 추가" 팝업 토글
   - 홈(index.html)과 회차 상세 페이지가 같은 스크립트를 공유합니다.
   - 팝업이 없는 페이지에서도 오류 없이 조용히 끝납니다. */
(function () {
  var wraps = document.querySelectorAll('.cal-add');
  if (!wraps.length) return;

  function closeAll(except) {
    wraps.forEach(function (wrap) {
      if (wrap === except) return;
      var btn = wrap.querySelector('.cal-add-btn');
      var menu = wrap.querySelector('.cal-add-menu');
      if (btn) btn.setAttribute('aria-expanded', 'false');
      if (menu) menu.hidden = true;
    });
  }

  wraps.forEach(function (wrap) {
    var btn = wrap.querySelector('.cal-add-btn');
    var menu = wrap.querySelector('.cal-add-menu');
    if (!btn || !menu) return;

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      e.stopPropagation();
      var isOpen = btn.getAttribute('aria-expanded') === 'true';
      closeAll(wrap);
      btn.setAttribute('aria-expanded', isOpen ? 'false' : 'true');
      menu.hidden = isOpen;
    });

    // 메뉴 내부 클릭은 바깥 클릭 닫힘으로 전파되지 않게 막습니다.
    menu.addEventListener('click', function (e) { e.stopPropagation(); });
  });

  document.addEventListener('click', function () { closeAll(null); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' || e.key === 'Esc') closeAll(null);
  });
})();
