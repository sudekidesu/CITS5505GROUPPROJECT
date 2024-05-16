// document.addEventListener('DOMContentLoaded', function() {
//     const submitButton = document.querySelector('.publis1291');
//     if (submitButton) {
//         submitButton.addEventListener('click', function() {
//             const questionTitle = document.querySelector('input[name="fname"]').value;
//             const category = document.querySelector('input[name="myBrowser"]').value;
//             const details = document.getElementById('txtEditor').value;
//
//             const newQuestion = {
//                 id: Date.now(), // 使用当前时间作为帖子的唯一标识符
//                 title: questionTitle,
//                 category: category,
//                 details: details
//             };
//
//             let questions = JSON.parse(localStorage.getItem('questions')) || [];
//             questions.unshift(newQuestion); // 将新帖子添加到数组的开始，以便新帖子显示在前面
//             localStorage.setItem('questions', JSON.stringify(questions));
//
//             window.location.href = '/'; // 跳转回主页
//         });
//     }
//
//     function loadQuestions() {
//         const questionsContainer = document.getElementById('content1');
//         if (questionsContainer) {
//             questionsContainer.innerHTML = ''; // 清空现有内容
//             const questions = JSON.parse(localStorage.getItem('questions')) || [];
//             questions.forEach(function(question) {
//                 const div = document.createElement('div');
//                 div.className = 'question-type2033';
//                 div.innerHTML = `
//                     <div class="row">
//                         <div class="col-md-1">
//                             <div class="left-user12923 left-user12923-repeat">
//                                 <img src="${image}" alt="Image" class="question-image">
//                             </div>
//                         </div>
//                         <div class="col-md-9">
//                             <div class="right-description893">
//                                 <div id="que-hedder2983">
//                                     <h3><a href="/post?id=${question.id}" target="_blank">${question.title}</a></h3>
//                                 </div>
//                                 <div class="ques-details10018">
//                                     <p>${question.details}</p>
//                                 </div>
//                             </div>
//                         </div>
//                     </div>`;
//                 questionsContainer.appendChild(div);
//             });
//         }
//     }
//
//     loadQuestions();
// });
// document.addEventListener('DOMContentLoaded', function() {
//     const searchInput = document.getElementById('searchInput');
//     const searchResults = document.getElementById('searchResults');
//
//     // 为输入框添加输入事件监听器
//     searchInput.addEventListener('input', function() {
//         const searchText = searchInput.value.toLowerCase();
//         const questions = JSON.parse(localStorage.getItem('questions')) || [];
//         searchResults.innerHTML = '';  // 清空当前的搜索结果
//
//         // 过滤并显示匹配的搜索结果
//         questions.forEach(function(question) {
//             if (question.title.toLowerCase().includes(searchText)) {
//                 const div = document.createElement('div');
//                 div.className = 'search-result-item';
//                 div.innerHTML = `
//                     <h4><a href="/post?id=${question.id}">${question.title}</a></h4>
//                     <p>${question.details}</p>`;
//                 searchResults.appendChild(div);
//             }
//         });
//
//         // 如果没有匹配的结果，并且搜索框不为空，显示"没有找到帖子"
//         if (!searchResults.children.length && searchText) {
//             searchResults.innerHTML = '<p>No posts found.</p>';
//         }
//     });
// });
//
//

$(document).ready(function() {
    $('#searchButton').click(function(e) {
        e.preventDefault();
        const query = $('#searchInput').val();
        if (query) {
            $.ajax({
                url: '/search',
                type: 'GET',
                data: {
                    q: query
                },
                success: function(response) {
                    displaySearchResults(response);
                },
                error: function() {
                    alert('Search failed. Please try again.');
                }
            });
        } else {
            alert('Please enter a search term.');
        }
    });

    function displaySearchResults(response) {
        const searchResultsContainer = document.getElementById('searchResults');
        searchResultsContainer.innerHTML = ''; // 清空之前的搜索结果

        if (response.questions.length === 0) {
            searchResultsContainer.innerHTML = '<p>No results found.</p>';
            return;
        }

        response.questions.forEach(question => {
            const questionHtml = `
                <div class="question">
                    <h3>${question.title}</h3>
                    <p>${question.content}</p>
                    <p>Author: ${question.author}</p>
                    <p>Category: ${question.category}</p>
                    <p>Likes: ${question.likes}</p>
                    <p>Posted on: ${question.create_time}</p>
                </div>
                <hr>
            `;
            searchResultsContainer.innerHTML += questionHtml;
        });
    }
});
