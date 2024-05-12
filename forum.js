document.addEventListener('DOMContentLoaded', function() {
    const submitButton = document.querySelector('.publis1291');
    if (submitButton) {
        submitButton.addEventListener('click', function() {
            const questionTitle = document.querySelector('input[name="fname"]').value;
            const category = document.querySelector('input[name="myBrowser"]').value;
            const details = document.getElementById('txtEditor').value;

            const newQuestion = {
                title: questionTitle,
                category: category,
                details: details
            };

            let questions = JSON.parse(localStorage.getItem('questions')) || [];
            questions.push(newQuestion);
            localStorage.setItem('questions', JSON.stringify(questions));

            window.location.href = 'index.html'; // Ensure this points to your homepage
        });
    }

    function loadQuestions() {
        const questionsContainer = document.getElementById('content1');
        if (questionsContainer) {
            const questions = JSON.parse(localStorage.getItem('questions')) || [];
            questions.forEach(function(question, index) {  // 添加index用于可能的标识符
                const div = document.createElement('div');
                div.className = 'question-type2033';
                div.innerHTML = `
                    <div class="row">
                        <div class="col-md-1">
                            <div class="left-user12923 left-user12923-repeat">
                                <img src="path/to/default/avatar.png" alt="User Avatar" class="question-image">
                            </div>
                        </div>
                        <div class="col-md-9">
                            <div class="right-description893">
                                <div id="que-hedder2983">
                                    <h3><a href="post-details.html?id=${index}" target="_blank">${question.title}</a></h3>
                                </div>
                                <div class="ques-details10018">
                                    <p>${question.details}</p>
                                </div>
                            </div>
                        </div>
                    </div>`;
                questionsContainer.prepend(div);
            });
        }
    }

    loadQuestions();
});
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');

    searchInput.addEventListener('input', function() {
        const searchText = searchInput.value.toLowerCase();
        const questions = JSON.parse(localStorage.getItem('questions')) || [];

        // 清除旧的搜索结果
        searchResults.innerHTML = '';

        // 过滤包含搜索文本的帖子并显示结果
        questions.forEach(function(question, index) {
            if (question.title.toLowerCase().includes(searchText)) {
                const resultItem = document.createElement('div');
                resultItem.className = 'search-result-item';
                resultItem.innerHTML = `
                    <h4><a href="post-details.html?id=${index}">${question.title}</a></h4>
                    <p>${question.details}</p>`;
                searchResults.appendChild(resultItem);
            }
        });

        // 如果没有结果，显示提示
        if (searchResults.children.length === 0 && searchText) {
            searchResults.innerHTML = '<p>No posts found.</p>';
        }

        // 如果搜索框为空，清除搜索结果
        if (!searchText) {
            searchResults.innerHTML = '';
        }
    });
});
