import { getToken, renderBoard } from './tools.js'

window.onload = renderBoard;

document.getElementById('postReplyButton').onclick = async () => {
  const text = document.getElementById('postReplyText').value;
  if (!text) {
    return;
  }
  const id = window.location.pathname.replace(/\/qa\/detail\//, '');
  const body = new FormData();
  body.append('content', text);
  body.append('csrf_token', await getToken());
  await fetch(`/qa/detail/${id}`, { method: 'POST', body })
  window.location.reload();
}

document.getElementById('likeButton').onclick = async () => {
  const body = new FormData();
  body.append('question_id', window.location.pathname.replace(/\/qa\/detail\//, ''));
  body.append('csrf_token', await getToken());
  await fetch('/qa/like', { method: 'POST', body });

  window.location.reload();
}