document.addEventListener('DOMContentLoaded', function() {
    function getParameterByName(name, url = window.location.href) {
        name = name.replace(/[\[\]]/g, '\\$&');
        var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
            results = regex.exec(url);
        if (!results) return null;
        if (!results[2]) return '';
        return decodeURIComponent(results[2].replace(/\+/g, ' '));
    }

    var postId = getParameterByName('id');  // 获取 URL 中的 id 参数
    var questions = JSON.parse(localStorage.getItem('questions')) || [];
    var question = questions.find(question => question.id && question.id.toString() === postId);  // 确保 id 存在并根据 id 找到相应的帖子

    if (question) {
        document.getElementById('postTitle').textContent = question.title;  // 设置帖子标题
        document.getElementById('postContent').textContent = question.details;  // 设置帖子内容
    } else {
        document.getElementById('postTitle').textContent = 'Post not found';
        document.getElementById('postContent').textContent = 'The requested post does not exist.';
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
                    <div class="left-user12923 left-user12923-repeat">
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
                    <div class="left-user12923 left-user12923-repeat">
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
