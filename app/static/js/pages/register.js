import { getToken } from './tools.js'


document.getElementById('submit').onclick = async () => {
  const body = new FormData();
  ['username', 'email', 'password', 'password_confirm'].forEach(key => {
    body.append(key, document.getElementById(key).value);
  });
  body.append('csrf_token', await getToken(true));

  await fetch('/register', { method: 'POST', body })

   window.location.href = '/login';
}