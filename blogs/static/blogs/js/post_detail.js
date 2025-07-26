const postId = document.body.dataset.postId;
const host = "http://localhost:8000/api";

// Function to load post details
async function loadPostDetails() {
  const res = await fetch(`${host}/posts/${postId}/`);
  const data = await res.json();

  document.getElementById("postTitle").textContent = data.title;
  document.getElementById("postContent").textContent = data.content;
  document.getElementById("postAuthor").textContent = data.author;
  document.getElementById("postLikes").textContent = data.likes_count;
  document.getElementById("postDate").textContent = new Date(data.created_at).toLocaleString();
}

// toggleLike function to like/unlike the post
async function toggleLike() {
  const res = await fetch(`${host}/posts/${postId}/toggle_like/`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("access")}`,
    },
  });
  if (res.status === 401) {
    alert("Please log in to like this post.");
    window.location.href = "/login/";
    return;
  }
  const data = await res.json();
  document.getElementById("postLikes").textContent = data["likes count"];
}

// Function to load comments
async function loadComments() {
  const res = await fetch(`${host}/posts/${postId}/comments/`);
  const comments = await res.json();

  const commentList = document.getElementById("commentsList");
  const currentUserName= localStorage.getItem('username')
  commentList.innerHTML = "";

  if (!comments.length) {
    commentList.innerHTML = "<p>No comments yet.</p>";
    return;
  }

  comments.forEach((c) => {
    const div = document.createElement("div");
    div.className = "comment";
    div.innerHTML = `
      <p><strong>${c.author}:</strong> ${c.text}</p>
      ${c.author === currentUserName ? `
        <button class="btn btn-sm btn-outline-secondary me-2 edit-comment" data-id="${c.id}">Edit</button>
        <button class="btn btn-sm btn-outline-danger delete-comment" data-id="${c.id}">Delete</button>
      ` : ""}
    `;
    commentList.appendChild(div);
  });
  // Bind edit/delete
  document.querySelectorAll(".delete-comment").forEach(btn => {
    btn.addEventListener("click", handleDeleteComment);
  });

  document.querySelectorAll(".edit-comment").forEach(btn => {
    btn.addEventListener("click", handleEditComment);
  });
}

// Function to handle comment deletion and editing
async function handleDeleteComment(e) {
  const commentId = e.target.dataset.id;
  const res = await fetch(`${host}/posts/${postId}/comments/${commentId}/`, {
    method: "DELETE",
    headers: {
      "Authorization": `Bearer ${localStorage.getItem("access")}`
    }
  });

  if (res.ok) {
    loadComments();
  } else {
    alert("Failed to delete comment.");
  }
}

async function handleEditComment(e) {
  const commentId = e.target.dataset.id;
  const newText = prompt("Edit your comment:");
  if (!newText) return;

  const res = await fetch(`${host}/posts/${postId}/comments/${commentId}/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${localStorage.getItem("access")}`
    },
    body: JSON.stringify({ text: newText })
  });

  if (res.ok) {
    loadComments();
  } else {
    alert("Failed to update comment.");
  }
}

// Function to submit a new comment
async function submitComment(e) {
  e.preventDefault();
  const text = document.getElementById("commentText").value;

  const res = await fetch(`${host}/posts/${postId}/comments/`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${localStorage.getItem("access")}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });
  if (res.status === 401) {
    alert("Please log in to comment.");
    window.location.href = "/login/";
    return;
  }
  if (res.ok) {
    document.getElementById("commentText").value = "";
    await loadComments(); // Refresh comments
  } else {
    alert("Failed to comment.");
  }
}

// View Likes
document.getElementById("showLikesBtn").addEventListener("click", async function () {
    const res = await fetch(`${host}/posts/${postId}/likes/`);
    const users = await res.json();

    const container = document.getElementById("likesList");
    container.innerHTML = "";

    if (!users.length) {
        container.textContent = "No likes yet.";
        return;
    }

    users.forEach(user => {
        const p = document.createElement("p");
        p.textContent = user.username;
        container.appendChild(p);
    });

    new bootstrap.Modal(document.getElementById("likesModal")).show();
});

// Check if the user has liked the post- uses state to change color of the like button
const likeBtn = document.getElementById("likeBtn");

async function checkIfUserLiked() {
    const res = await fetch(`${host}/posts/${postId}/likes/`);
    const users = await res.json();
    const currentUserId = localStorage.getItem("user_id");

    const hasLiked = users.some(user => user.id == currentUserId);

    updateLikeBtnStyle(hasLiked);
}

function updateLikeBtnStyle(liked) {
    if (liked) {
        likeBtn.classList.add("btn-liked");
        likeBtn.classList.remove("btn-unliked");
        likeBtn.textContent = "♥";
    } else {
        likeBtn.classList.remove("btn-liked");
        likeBtn.classList.add("btn-unliked");
        likeBtn.textContent = "🤍";
    }
}

likeBtn.addEventListener("click", async () => {
    const res = await fetch(`${host}/posts/${postId}/toggle_like/`, {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${localStorage.getItem("access")}`
        }
    });

    if (res.ok) {
        const data = await res.json();
        document.getElementById("postLikes").textContent = data["likes count"];
        checkIfUserLiked(); // recheck state and update color
    } else {
        alert("Failed to like/unlike the post.");
    }
});

document.getElementById("likeBtn").addEventListener("click", toggleLike);
document
  .getElementById("commentForm")
  .addEventListener("submit", submitComment);
loadPostDetails();
loadComments();
checkIfUserLiked();
