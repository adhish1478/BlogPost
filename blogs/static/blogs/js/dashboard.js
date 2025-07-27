const host= "https://blogpost-qyzf.onrender.com/api"

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


// Render Posts
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
            <h3>
                    <a href="/posts/${post.id}/" class="text-decoration-none text-dark">
                        ${post.title}
                    </a>
                </h3>
                <p>${post.content.split(" ").slice(0, 30).join(" ")}...</p>
                <p><strong>Author:</strong> ${post.author}</p>
                <p><strong>Created At:</strong> ${formattedDate}</p>
                <p><strong>♥️</strong> ${post.likes_count}</p>
                <a href="/posts/${post.id}/" class="btn btn-sm btn-outline-primary mt-2">Read More</a>
                `;
            postList.appendChild(div);

        });


}

// Search functionality
document.getElementById("searchInput").addEventListener("input", function () {
    const keyword = this.value.trim();
    if (keyword) {
        fetchPosts(keyword); // Call the function to fetch posts with the keyword
    }
});

// Post Create modal
document.getElementById("createPostForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const title = document.getElementById("postTitle").value.trim();
    const content = document.getElementById("postContent").value.trim();

    if (!title || !content) {
        alert("Title and content are required.");
        return;
    }

    try {
        const response = await fetch(`${host}/posts/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${localStorage.getItem("access")}`,
            },
            body: JSON.stringify({ title, content }),
        });

        if (response.ok) {
            const post = await response.json();
            // Close modal and reload posts
            const modal = bootstrap.Modal.getInstance(document.getElementById("createPostModal"));
            modal.hide();
            fetchPosts(); // reload post list
        } else {
            const err = await response.json();
            alert(err.detail || "Failed to create post.");
        }
    } catch (error) {
        console.error("Post creation error:", error);
        alert("Something went wrong while creating post.");
    }
});

// Initial fetch of posts
fetchPosts();
