document.addEventListener('DOMContentLoaded', function() {
    // Function to fetch a post based on the ID from the URL
    function loadPost() {
        const postId = getParameterByName('id');
        fetch(`/qa/detail/${postId}`) // Make sure this matches your route for fetching a specific post
        .then(response => response.json())
        .then(question => {
            if (question) {
                document.getElementById('postTitle').textContent = question.title;
                document.getElementById('postContent').textContent = question.details;
            } else {
                document.getElementById('postTitle').textContent = 'Post not found';
                document.getElementById('postContent').textContent = 'The requested post does not exist.';
            }
        })
        .catch(error => console.error('Error loading the post:', error));
    }

    // Add comments
    const submitButton = document.querySelector('.pos393-submit');
    submitButton.addEventListener('click', function() {
        const commentText = document.querySelector('.comment-input219882').value.trim();
        const postId = getParameterByName('id');
        if (commentText && postId) {
            fetch(`/comment/public`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('input[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ content: commentText, question_id: postId })
            })
            .then(response => response.json())
            .then(comment => {
                var newComment = document.createElement('li');
                newComment.innerHTML = `
                    <div class="comment-main-level">
                        <div class="comment-avatar"><img src="${comment.avatarUrl || 'path/to/avatar.png'}" alt=""></div>
                        <div class="comment-box">
                            <div class="comment-head">
                                <h6 class="comment-name">${comment.authorName || 'Anonymous'}</h6>
                                <span>${new Date(comment.timestamp).toLocaleTimeString()}</span>
                            </div>
                            <div class="comment-content">${comment.text}</div>
                        </div>
                    </div>`;
                document.getElementById('comments-list').appendChild(newComment);
                document.querySelector('.comment-input219882').value = '';
            })
            .catch(error => console.error('Error posting comment:', error));
        }
    });

    loadPost();
});

// Helper function to extract parameters from the URL
function getParameterByName(name, url = window.location.href) {
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}
