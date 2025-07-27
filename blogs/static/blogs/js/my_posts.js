const host = "http://localhost:8000/api"; 
const token = localStorage.getItem("access");

// Load user's posts
async function loadMyPosts() {
  const res = await fetch(`${host}/posts/my_posts/`, {
    headers: {
      Authorization: `Bearer ${token}`
    }
  });
  const posts = await res.json();

  const container = document.getElementById("myPostsList");
  container.innerHTML = "";

  posts.forEach(post => {
    const div = document.createElement("div");
    div.className = "col-md-6";
    div.innerHTML = `
      <div class="card h-100 shadow-sm">
        <div class="card-body">
          <h5 class="card-title">${post.title}</h5>
          <p class="card-text">${post.content.slice(0, 120)}...</p>
          <div class="d-flex justify-content-end">
            <button class="btn btn-sm btn-outline-primary me-2" onclick="openEditModal(${post.id}, \`${post.title}\`, \`${post.content}\`)">Update</button>
            <button class="btn btn-sm btn-outline-danger" onclick="openDeleteModal(${post.id})">Delete</button>
          </div>
        </div>
      </div>
    `;
    container.appendChild(div);
  });
}

// Open update modal
function openEditModal(id, title, content) {
  document.getElementById("editPostId").value = id;
  document.getElementById("editPostTitle").value = title;
  document.getElementById("editPostContent").value = content;
  new bootstrap.Modal(document.getElementById("editPostModal")).show();
}

// Open delete modal
function openDeleteModal(id) {
  document.getElementById("confirmDeleteBtn").onclick = () => deletePost(id);
  new bootstrap.Modal(document.getElementById("deletePostModal")).show();
}

// Submit edit
document.getElementById("editPostForm").addEventListener("submit", async function (e) {
  e.preventDefault();
  const id = document.getElementById("editPostId").value;
  const title = document.getElementById("editPostTitle").value;
  const content = document.getElementById("editPostContent").value;

  const res = await fetch(`${host}/posts/${id}/`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ title, content }),
  });

  if (res.ok) {
    bootstrap.Modal.getInstance(document.getElementById("editPostModal")).hide();
    loadMyPosts();
  } else {
    alert("Update failed.");
  }
});

// Delete post
async function deletePost(id) {
  const res = await fetch(`${host}/posts/${id}/`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (res.ok) {
    bootstrap.Modal.getInstance(document.getElementById("deletePostModal")).hide();
    loadMyPosts();
  } else {
    alert("Delete failed.");
  }
}

loadMyPosts();