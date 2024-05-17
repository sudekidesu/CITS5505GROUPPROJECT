export const getToken = async (forceUpdate) => {
  if (forceUpdate) {
    sessionStorage.clear('csrf-token');
  }
  const t = sessionStorage.getItem('csrf-token');
  if (t) {
    return t;
  }
  const res = await fetch('/csrf-token');
  const { csrfToken } = await res.json();
  sessionStorage.setItem('csrf-token', csrfToken);
  return csrfToken;
}

export const search = async ({ question, page = 1, per_page = 10 }) => {
  const res = await fetch(`/search?q=${question}&page=${page}&per_page=${per_page}`);
  return res.json();
}

export const publish = async (data) => {
  const body = new FormData();
  Object.entries(data).forEach((item) => {
    body.append(...item);
  })
  body.append('csrf_token', await getToken());

  const res = await fetch(
    '/qa/public',
    {
      method: 'post',
      body
    },
  );
  return res.json();
}

export const getBoard = async () => {
  const r = await fetch('/board');
  const { questions } = await r.json();
  return questions;
}

export const renderBoard = async () => {
  const qs = await getBoard();
  document.getElementById("board").innerHTML = qs.sort((a, b) => b.likes - a.likes).map(item => `
  <div class="pints-wrapper">
    <div class="left-user3898">
      <a href="#"><img src='/static/image/images.png' alt="Image"></a>
      <div class="imag-overlay39">
        <a><i class="fa fa-plus" aria-hidden="true"></i></a> 
      </div>
    </div>
    <span class="points-details938">
      <a href="#"><h5>${item.username}</h5></a>
      <p>${item.likes}</p>
    </span>
  </div>
  `).join('');
}