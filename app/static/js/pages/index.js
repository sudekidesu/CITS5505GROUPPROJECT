import { search, renderBoard } from "./tools.js";

let __page__ = 1;
let __max_pages__ = 1;



const renderN = (pages = 0) => {
	if (pages < 2) {
		document.getElementById("navigation").innerHTML = "";
		return;
	}
	const li = new Array(pages)
		.fill(1)
		.map((_, index) => `<li><a value="${index + 1}">${index + 1}</a></li>`);
	document.getElementById("navigation").innerHTML = `
    <li>
      <a aria-label="Previous" value="pre">
        <span aria-hidden="true" value="pre">&laquo;</span>
      </a>
    </li>
    ${li.join("")}
    <li>
      <a aria-label="Next" value="next">
        <span aria-hidden="true" value="pre">&raquo;</span>
      </a>
    </li>`;
};

const mountX = (qs) => {
  const t = qs.map((question) => {
		return `
      <div class="row" value=>
        <div class="col-md-1">
          <div class="left-user12923 left-user12923-repeat">
            <a href="#"><img src="/static/image/images.png" alt="image"> </a> 
          </div>
        </div>
        <div class="right-description893">
          <div>
            <h3><a href="/qa/detail/${question.id}" target="_blank">${question.title}</a></h3>
          </div>
          <div class="ques-details10018">
              <p>${question.content}</p>
          </div>
        </div>
      </div>
    `;
	});
	document.getElementById("_content_").innerHTML = `<div>${t.join("")}</div>`;
}
const renderAnswered = async ({ __page__ = 1, per_page=10} = {}) => {
	 
	let resp= await fetch(`/recentanswered?page=${__page__}&per_page=${per_page}`);
	const { questions, pages, current_page } =await resp.json();
	console.log(resp,'pageresps');
	console.log(pages,'pages');
	console.log(current_page,'current_page');
	renderN(pages);
	navigationClick(2);
	__page__ = current_page;
	__max_pages__ = pages;
	mountX(questions);
};
const render = async ({ page = __page__ } = {}) => {
	const text = document.getElementById("searchInput").value ?? "";
	const { questions, pages, current_page } = await search({
		question: text,
		page,
	});
	renderN(pages);
	navigationClick(1);
	__page__ = current_page;
	__max_pages__ = pages;
    mountX(questions);
};
const navigationClick=(type)=>{
	document.getElementById("navigation").onclick = (value) => {
		let page = value.target.getAttribute("value");
		if (page === "pre") {
			page = __page__ === 1 ? __max_pages__ : __page__ - 1;
		} else if (page === "next") {
			page = __page__ === __max_pages__ ? 1 : __page__ + 1;
		}
		console.log(page);
		// document.querySelector('#tab1')
		if(type==1){
			render({ page });
		}
		if(type==2){
			renderAnswered ({ __page__:page });
		}

	};

}
window.onload = () => {
  renderBoard();
  render();
};

document.getElementById("searchButton").addEventListener("click", async () => {
	render();
});






document.getElementById('tab1').onclick = render

// document.getElementById('tab3').onclick = async()=> {
// 	const res = await fetch('/recentanswered');
// 	const {questions} = await res.json();
// 	console.info(questions);
// 	mountX(questions);
// }
document.getElementById('tab3').onclick = renderAnswered




