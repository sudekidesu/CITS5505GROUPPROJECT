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
                    // 在这里处理成功响应
                    console.log(response); // 你可以将响应输出到控制台查看
                },
                error: function() {
                    alert('Search failed. Please try again.');
                }
            });
        } else {
            alert('Please enter a search term.');
        }
    });
});
