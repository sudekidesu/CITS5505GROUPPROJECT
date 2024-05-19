import { publish, renderBoard } from './tools.js';

const submit = document.getElementById('submit');

submit.addEventListener('click', async () => {

  publish({
    title: document.getElementById('title').value,
    content: document.getElementById('content').value,
    category: document.getElementById('category').value,
  });
    window.location.href = "/";

})

window.onload = renderBoard;