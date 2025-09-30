(function() {
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
    async function poll(lastCheck) {
        try {
            let res = await fetch(`/poll_new_posts?last_check=${lastCheck}`);
            let data = await res.json();

            if (data.new_post) {
                // Check if already in feed
                const existing = feed.querySelector(`.post-card[data-id="${data.post_id}"]`);
                if (!existing) {
                    feed.insertAdjacentHTML("afterbegin", data.html);
                }
                lastCheck = data.last_check;
            }

            setTimeout(() => poll(lastCheck), 1000);
        } catch (err) {
            console.error("Polling error:", err);
            setTimeout(() => poll(lastCheck), 5000);
        }
    }

    poll(0);

})();
