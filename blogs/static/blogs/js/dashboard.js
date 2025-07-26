const host= "http://localhost:8000/api"

async function fetchPosts(searchTerm = '') {
    try{
        const query= searchTerm ? `?search=${encodeURIComponent(searchTerm)}` : '';
        const response= await fetch(`${host}/posts/${query}`);
        if (!response.ok) {
            throw new Error('Failed to fetch Post from Server');
        }

        const data= await response.json();
        renderPosts(data);
    } catch (error) {
        console.error('Error fetching posts:', error);
        alert('Failed to fetch posts. Please try again later.');
    }
}

async function renderPosts(posts) {
        const postList= document.getElementById('postList')
        postList.innerHTML= ''; // Clear existing posts

        const postArray = posts.results || posts; // Handle both single and multiple posts

        if(!postArray.length) {
            postList.innerHTML= '<p> No Post to display</p>';
            return;
        }

        postArray.forEach(post => {
            const div= document.createElement('div');
            div.className= 'post-item';
            // Format the date to 'dd Month yyyy'
            const formattedDate = new Date(post.created_at).toLocaleDateString('en-GB', {
                day: 'numeric',
                month: 'long',
                year: 'numeric'
            });
            div.innerHTML= `
                <h3>${post.title}<h3>
                <p>${post.content}</p>
                <p><strong>Author:</strong> ${post.author}</p>
                <p><strong>Created At:</strong> ${formattedDate}</p>
                <p><strong>🤍:</strong> ${post.likes_count}</p>
                `;
            postList.appendChild(div);

        });


}

document.getElementById("searchForm").addEventListener("submit", function (e) {
    e.preventDefault();
    const keyword = document.getElementById("searchInput").value.trim();
    if (keyword) {
        fetchPosts(keyword); // Call the function to fetch posts with the keyword
    }
});

// Initial fetch of posts
fetchPosts();
