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

            window.location.href = '/'; // Ensure this points to your homepage
        });
    }

    function loadQuestions() {
        const questionsContainer = document.getElementById('content1');
        if (questionsContainer) {
            const questions = JSON.parse(localStorage.getItem('questions')) || [];
            questions.forEach(function(question) {
                const div = document.createElement('div');
                div.className = 'question-type2033';
                div.innerHTML = `
                    <div class="row">
                        <div class="col-md-1">
                            <div class="left-user12923 left-user12923-repeat">
                                <img src="${image}" alt="Image" class="question-image">
                            </div>
                        </div>
                        <div class="col-md-9">
                            <div class="right-description893">
                                <div id="que-hedder2983">
                                    <h3><a href="/post" target="_blank">${question.title}<a></h3>
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
