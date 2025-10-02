(function () {
    // ------------------- Variables -------------------
    const feedContainer = document.getElementById('show-feed'); // main container
    const feed = document.getElementById('feed'); // inner feed holding posts
    const endTrigger = document.getElementById('end-trigger');

    const imgPopup = document.getElementById('img-modal');
    const modalImg = document.getElementById('modal-img');
    const closeImg = imgPopup.querySelector('.close-img');

    const descModal = document.getElementById('desc-modal');
    const fullDesc = document.getElementById('full-desc');
    const closeDesc = descModal.querySelector('.close-btn');

    // ------------------- Infinite Scroll -------------------
    const observer = new IntersectionObserver((entries) => {
        if (entries[0].isIntersecting) {
            // Clone current posts
            const clone = feed.innerHTML;
            feed.insertAdjacentHTML('beforeend', clone);
        }
    });

    observer.observe(endTrigger);

    // ------------------- Event Delegation -------------------
    feedContainer.addEventListener('click', (e) => {
        // ---------------- Image Modal ----------------
        if (e.target.classList.contains('post-img')) {
            imgPopup.style.display = "flex";
            modalImg.src = e.target.src;
        }

        // ---------------- Description Modal ----------------
        if (e.target.classList.contains('read-more-btn')) {
            const description = e.target.previousElementSibling.textContent;
            fullDesc.textContent = description;
            descModal.style.display = 'flex';
        }
    });

    // ------------------- Close Modals -------------------
    closeImg.addEventListener('click', () => {
        imgPopup.style.display = "none";
    });

    closeDesc.addEventListener('click', () => {
        descModal.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === imgPopup) imgPopup.style.display = 'none';
        if (e.target === descModal) descModal.style.display = 'none';
    });

    // ------------------- Polling New Posts -------------------
    let lastCheck = Date.now() / 1000; // seconds timestamp

    async function pollNewPosts() {
        try {
            const response = await fetch(`/poll_new_posts/?last_check=${lastCheck}`);
            const data = await response.json();

            if (data.new_post) {
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = data.html;

                const posts = tempDiv.querySelectorAll('.post-card');

                posts.forEach(post => {
                    const postId = post.dataset.id;
                    const existing = document.querySelector(`.post-card[data-id="${postId}"]`);

                    if (existing) {
                        // ✅ Replace the old post card completely
                        existing.replaceWith(post);
                    } else {
                        // ✅ Prepend new post at top
                        feed.insertAdjacentHTML('afterbegin', post.outerHTML);
                    }
                });

                lastCheck = data.last_check;
            }

            if (data.deleted_post) {
                data.deleted_ids.forEach(id => {
                    const el = document.querySelector(`.post-card[data-id="${id}"]`);
                    if (el) el.remove();
                });
                lastCheck = data.last_check;
            }

        } catch (err) {
            console.error("Polling error:", err);
        }

        setTimeout(pollNewPosts, 3000); // repeat polling every 3s
    }

    pollNewPosts();

    // --------------------------LIKES---------------------------

    document.addEventListener("click", async function (e) {
    if (e.target.closest(".like-btn")) {
        const btn = e.target.closest(".like-btn");
        const postId = btn.dataset.id;
        const heartIcon = btn.querySelector(".heart-icon");
        const likeCount = btn.querySelector(".like-count");

        try {
            const response = await fetch(`/toggle_like/${postId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            });
            const data = await response.json();

            if (data.post_id) {
                likeCount.textContent = data.like_count;

                if (data.liked) {
                    heartIcon.classList.add("liked");  // pink
                } else {
                    heartIcon.classList.remove("liked"); // blue
                }
            }
        } catch (err) {
            console.error("Like toggle failed:", err);
        }
    }
});

// ✅ CSRF helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



})();