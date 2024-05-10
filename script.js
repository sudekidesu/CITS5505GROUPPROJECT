
function searchPosts() {
    var input, filter, posts, postContainer, textValue;
    input = document.getElementById("searchInput");
    filter = input.value.toUpperCase(); 
    posts = document.getElementsByClassName("question-type2033"); 
    for (var i = 0; i < posts.length; i++) {
        postContainer = posts[i].getElementsByTagName("p")[0]; 
        if (postContainer) {
            textValue = postContainer.textContent || postContainer.innerText;
            if (textValue.toUpperCase().indexOf(filter) > -1) {
                posts[i].style.display = ""; 
            } else {
                posts[i].style.display = "none"; 
            }
        }
    }
}

