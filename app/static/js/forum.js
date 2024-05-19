document.addEventListener('DOMContentLoaded', function() {
    // Load questions from the server
    function loadQuestions() {
        fetch('/qa/public') // Adjust this URL based on your actual API endpoint for fetching questions
        .then(response => response.json())
        .then(questions => {
            const questionsContainer = document.getElementById('content1');
            questionsContainer.innerHTML = ''; // Clear existing content
            questions.forEach(question => {
                const div = document.createElement('div');
                div.className = 'question-type2033';
                div.innerHTML = `
                    <div class="row">
                        <div class="col-md-1">
                            <div class="left-user12923">
                                <img src="${question.authorAvatar || 'path/to/default/avatar.png'}" alt="User Avatar" class="question-image">
                            </div>
                        </div>
                        <div class="col-md-9">
                            <div class="right-description893">
                                <div id="que-hedder2983">
                                    <h3><a href="post-details.html?id=${question.id}" target="_blank">${question.title}</a></h3>
                                </div>
                                <div class="ques-details10018">
                                    <p>${question.details}</p>
                                </div>
                            </div>
                        </div>
                    </div>`;
                questionsContainer.appendChild(div);
            });
        })
        .catch(error => console.error('Error loading questions:', error));
    }

    // Event listener for posting a new question
    const submitButton = document.querySelector('.publis1291');
    submitButton.addEventListener('click', function() {
        const questionTitle = document.querySelector('input[name="fname"]').value;
        const category = document.querySelector('input[name="myBrowser"]').value;
        const details = document.getElementById('txtEditor').value;

        const newQuestion = {
            title: questionTitle,
            category: category,
            details: details
        };

        fetch('/qa/public', {  // Adjust this endpoint for posting a new question
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(newQuestion)
        })
        .then(response => {
            if (response.ok) return response.json();
            throw new Error('Failed to create question');
        })
        .then(() => window.location.href = '/')
        .catch(error => console.error('Error posting question:', error));
    });

    loadQuestions();
});
