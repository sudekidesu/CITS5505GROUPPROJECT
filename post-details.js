document.addEventListener('DOMContentLoaded', function() {
    var questions = JSON.parse(localStorage.getItem('questions')) || [];
    var latestQuestion = questions[questions.length - 1]; // 获取最新的帖子
    if (latestQuestion) {
        document.getElementById('postTitle').textContent = latestQuestion.title; // 设置帖子标题
    }
});
