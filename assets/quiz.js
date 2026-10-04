// Reusable quiz component. Markup:
// <div class="quiz" data-answer="2" data-right="Why it's right" data-wrong="Hint if wrong">
//   <h3>Question</h3><div class="opts"><button>..</button>...</div></div>
// One try per question (retrieval practice); a running score shows in any .score element.
(function () {
  const quizzes = [...document.querySelectorAll('.quiz')];
  let done = 0, right = 0;
  const scoreEls = document.querySelectorAll('.score');
  const paint = () => scoreEls.forEach(el => { el.textContent = done ? `${right} / ${quizzes.length} right first time` : `0 / ${quizzes.length} answered`; });
  quizzes.forEach(q => {
    const buttons = [...q.querySelectorAll('.opts button')];
    const answer = Number(q.dataset.answer);
    const why = document.createElement('p');
    why.className = 'why'; why.setAttribute('aria-live', 'polite');
    q.appendChild(why);
    buttons.forEach((b, i) => {
      b.type = 'button';
      b.addEventListener('click', () => {
        const ok = i === answer;
        buttons.forEach(x => x.disabled = true);
        buttons[answer].classList.add('right');
        if (!ok) b.classList.add('wrong');
        why.className = 'why ' + (ok ? 'ok' : 'no');
        why.textContent = (ok ? 'Right. ' : 'Not quite. ') + (q.dataset.right || '');
        done++; if (ok) right++; paint();
      });
    });
  });
  paint();
})();
