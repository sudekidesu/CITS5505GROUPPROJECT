document.addEventListener('DOMContentLoaded', function() {
    var questions = JSON.parse(localStorage.getItem('questions')) || [];
    var latestQuestion = questions[questions.length - 1]; // 获取最新的帖子
    if (latestQuestion) {
        document.getElementById('postTitle').textContent = latestQuestion.title; // 设置帖子标题
        document.getElementById('postContent').textContent = latestQuestion.details; // 设置帖子内容
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var questions = JSON.parse(localStorage.getItem('questions')) || [];
    var latestQuestion = questions[questions.length - 1];
    if (latestQuestion) {
        document.getElementById('postTitle').textContent = latestQuestion.title;
        document.getElementById('postContent').textContent = latestQuestion.details;
    }

    var submitButton = document.querySelector('.pos393-submit');
    var commentInput = document.querySelector('.comment-input219882');
    var commentsList = document.getElementById('comments-list');

    submitButton.addEventListener('click', function() {
        var commentText = commentInput.value.trim();
        if (commentText) {
            var newComment = document.createElement('li');
            newComment.innerHTML = `
                <div class="comment-main-level">
                    <div class="comment-avatar">
                        <img src="${image}" alt="Image" class="question-image">
                    </div>
                    <div class="comment-box">
                        <div class="comment-head">
                            <h6 class="comment-name">Anonymous</h6>
                            <span><i class="fa fa-clock-o" aria-hidden="true"></i> just now</span>
                        </div>
                        <div class="comment-content">${commentText}</div>
                    </div>
                </div>`;
            commentsList.appendChild(newComment);
            commentInput.value = ''; // 清空输入框
        }
    });
});