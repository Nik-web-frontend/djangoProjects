document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById('profileModal');
    const btn = document.getElementById('manageProfileBtn');
    const close = document.querySelector('.profile-close')

    if (btn) {

        btn.onclick = function () {
            modal.style.display = 'flex'; // show popup
        }

        close.onclick = function () {
            modal.style.display = 'none'; // hide popup
        }

        // Close popup if user clicks outside modal
        window.onclick = function (event) {
            if (event.target == modal) {
                modal.style.display = 'none';
            }
        }
    }

    const delProfile = document.querySelector('#del-profile');
    const delPopup = document.querySelector('.del-popup');
    const cancelBtn = document.querySelector('.profile-cancel');

    delProfile.onclick = function () {
        delPopup.style.display = 'flex'; // show popup
    }

    cancelBtn.onclick = function () {
        delPopup.style.display = 'none'; // hide popup
    }
    const uploadBtn = document.getElementById("uploadBtn")
    if (uploadBtn) {

        uploadBtn.onclick = function () {
            document.getElementById("uploadPopup").style.display = "flex";
        }
    }

    // --------------------------------------------------------------- 
    // POST EDIT BUTTON 

        const popup = document.getElementById("editPopup");
        const closePopup = document.getElementById("closePopup");
        const editForm = document.getElementById("editForm");
        const editTitle = document.getElementById("editTitle");
        const editDescription = document.getElementById("editDescription");

        document.querySelectorAll(".edit-btn").forEach(btn => {
            btn.addEventListener("click", function () {
                const postId = this.getAttribute("data-post-id");
                const title = this.getAttribute("data-title");
                const description = this.getAttribute("data-description");

                editTitle.value = title;
                editDescription.value = description;

                // update form action dynamically
                editForm.action = `/post/${postId}/edit/`;

                popup.style.display = "flex";
            });
        });

        closePopup.addEventListener("click", function () {
            popup.style.display = "none";
        });


    // ---------------------------------------------------- 
    //  POST DELETE BUTTON 

    // sab delete buttons select karo
    document.querySelectorAll('.del-post-popup-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.preventDefault();

            const postId = btn.getAttribute('data-post-id'); // button se post.id lo

            const popupContainer = document.querySelector('.del-post-container');
            const delForm = popupContainer.querySelector('.delpost-form');

            // form action update karo sahi post ke liye
            delForm.action = `/delete_post/${postId}/`;

            // popup show karo
            popupContainer.style.display = 'flex';
        });
    });

    // Cancel button click pe popup close karo
    document.querySelector('.del-post-cancel').addEventListener('click', () => {
        document.querySelector('.del-post-container').style.display = 'none';
    });

    // -------------------------------------------------------------------------- 
    // Description Read more or less 
    const modall = document.getElementById('desc-modal');
    const fullDesc = document.getElementById('full-desc');
    const closeBtn = modall.querySelector('.close-btn');
    const modalTitle = document.getElementById('modal-title');

    document.querySelectorAll('.read-more-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const card = btn.closest(".card"); // parent card
            const title = card.querySelector(".post-title").textContent;
            const description = card.querySelector(".description").textContent;

            modalTitle.textContent = title;
            fullDesc.textContent = description;
            modall.style.display = 'flex';
        });
    });

    closeBtn.addEventListener('click', () => {
        modall.style.display = 'none';
    });

    window.addEventListener('click', (e) => {
        if (e.target === modall) modall.style.display = 'none';
    });

    // POST IMG OPEN 



    const imgpopup = document.getElementById('img-modal');
    const modalImg = document.getElementById('modal-img');
    const closeimg = imgpopup.querySelector('.close-img');

    // For all post images
    document.querySelectorAll('.post-img').forEach(img => {
        img.addEventListener('click', () => {
            imgpopup.style.display = "flex";
            modalImg.src = img.src;
        });
    });

    closeimg.addEventListener('click', () => {
        imgpopup.style.display = "none";
    });

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            imgpopup.style.display = "none";
        }
    });
    
});


