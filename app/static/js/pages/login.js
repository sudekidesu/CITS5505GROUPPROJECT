import { getToken } from './tools.js'


document.getElementById('submit').onclick = async () => {
  const body = new FormData();
  ['username', 'password'].forEach(key => {
    body.append(key, document.getElementById(key).value);
  });
  body.append('csrf_token', await getToken());

  await fetch('/login', { method: 'POST', body })

  // window.location.href = '/';
}
